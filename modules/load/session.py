from dataclasses import asdict
import threading
import time
import re

import psutil
from PySide6.QtCore import QThread, Signal

from modules.hardware.models import Snapshot
from modules.hardware.presentation import LatestFrame
from .client import LoadClient, LoadError
from .logging import SessionLog
from .models import BatteryFlow, LoadConfig, QualityTracker
from .power import PowerSession


class CapabilityProbe(QThread):
    available = Signal(object)
    def run(self):
        client = LoadClient()
        try:
            self.available.emit(client.request("capabilities"))
        except Exception as error:
            self.available.emit({"error": str(error), "physical_cores": 0, "gpus": []})
        finally:
            client.close()


class ThermalGuard:
    def __init__(self):
        self.hot = {}

    def evaluate(self, snapshot, gpu_name, config):
        devices = {d.id: d for d in snapshot.devices}
        def name(value):
            return re.sub(r"[^a-z0-9]", "", re.sub(r"\((?:r|tm)\)", "", value.casefold()))
        gpu_devices = [d for d in snapshot.devices if d.kind == "sensor_gpu" and name(d.name) == name(gpu_name)]
        gpu_ids = {d.id for d in gpu_devices} if len(gpu_devices) == 1 else set()
        values, reason = {}, None
        for resource, limit in (("cpu", config.cpu_limit), ("gpu", config.gpu_limit)):
            readings = [r for r in snapshot.readings if r.unit == "°C" and r.value is not None and r.availability == "available" and not r.is_stale()
                        and ((resource == "cpu" and devices.get(r.device_id) and devices[r.device_id].kind == "sensor_cpu"
                              and any(s in r.name.casefold() for s in ("package", "tctl", "tdie", "core max")))
                             or (resource == "gpu" and r.device_id in gpu_ids and not any(s in r.name.casefold() for s in ("memory", "hot", "limit"))))]
            reading = max(readings, key=lambda r: r.value) if readings else None
            values[resource + "_temperature"] = reading.value if reading else None
            if reading is None or reading.value < limit:
                self.hot.pop(resource, None)
            else:
                first = self.hot.setdefault(resource, reading.timestamp)
                if (reading.timestamp - first).total_seconds() >= 3:
                    reason = f"Límite térmico de {resource.upper()} alcanzado ({limit} °C)."
        values["thermal_warning"] = "Temperatura no disponible; supervisión térmica parcial." if any(v is None for v in (values["cpu_temperature"], values["gpu_temperature"])) else None
        return values, reason


class LoadSession(QThread):
    result = Signal(object)
    def __init__(self, config, battery=None, hardware=None, parent=None, client_factory=LoadClient, log_factory=SessionLog):
        super().__init__(parent)
        self.config = config.validate()
        self.battery = battery.validate() if battery else None
        self.hardware = hardware or (lambda: Snapshot())
        self.client_factory = client_factory
        self.log_factory = log_factory
        self.frames = LatestFrame()
        self._stop = threading.Event()
        self._updates = LatestFrame()
        self._interruption = None

    def stop(self):
        self._stop.set()

    def interrupt(self, reason):
        self._interruption = reason
        self._stop.set()

    def update_config(self, config):
        if self.battery:
            raise LoadError("Los parámetros están bloqueados durante la prueba de batería.")
        self._updates.publish(config.validate())

    def run(self):
        import pythoncom
        pythoncom.CoInitialize()
        client, log, power = None, None, None
        quality = QualityTracker()
        thermal = ThermalGuard()
        started = None
        quality_started = None
        elapsed = 0.0
        status, reason = "error", "No se pudo iniciar la sesión."
        sample = {}
        try:
            log = self.log_factory(self.config, self.battery)
            flow = BatteryFlow(self.battery) if self.battery else None
            if flow:
                flow.preflight(psutil.sensors_battery())
            power = PowerSession(self.battery.brightness if self.battery else None)
            power.__enter__()
            if power.warning:
                log.event("warning", message=power.warning)
            self.frames.publish({"state": "preparing", "message": "Preparando mediciones y carga…", "log_folder": str(log.folder)})
            client = self.client_factory()
            capabilities = client.request("capabilities")
            gpu_name = next((gpu["name"] for gpu in capabilities.get("gpus", []) if gpu["id"] == self.config.gpu_id), "")
            client.request("start", self.config)
            started = quality_started = previous = time.monotonic()
            missing_since = None
            battery_missing_since = None
            while not self._stop.is_set():
                tick = time.monotonic()
                elapsed = tick - started
                if tick - previous > 4:
                    status, reason = "interrupted", "Suspensión o intervalo sin medición detectado."
                    break
                previous = tick
                update = self._updates.take()
                if update:
                    client.request("update", update)
                    self.config = update
                    quality = QualityTracker()
                    quality_started = time.monotonic()
                    log.event("configuration_changed", load=asdict(update))
                    gpu_name = next((gpu["name"] for gpu in capabilities.get("gpus", []) if gpu["id"] == update.gpu_id), "")
                    previous = time.monotonic()
                sample = client.request("status")
                elapsed = time.monotonic() - started
                quality.observe(time.monotonic() - quality_started, sample, self.config)
                missing = ((self.config.cpu_target and sample.get("cpu_actual") is None) or
                           (self.config.gpu_target and sample.get("gpu_actual") is None))
                if missing:
                    missing_since = missing_since if missing_since is not None else tick
                    if tick - missing_since >= 5:
                        status, reason = "interrupted", "Se perdió la medición necesaria para regular la carga."
                        break
                else:
                    missing_since = None
                raw = self.hardware()
                uncertain_batteries = self.battery and any(error.provider in {"battery", "host"} for error in raw.errors)
                if uncertain_batteries:
                    battery_missing_since = battery_missing_since if battery_missing_since is not None else tick
                    if tick - battery_missing_since >= 5:
                        status, reason = "interrupted", "No se puede verificar el conjunto de baterías instaladas."
                        break
                else:
                    battery_missing_since = None
                temperatures, hot = thermal.evaluate(raw, gpu_name, self.config)
                battery = psutil.sensors_battery()
                ids = tuple(sorted(d.id for d in raw.devices if d.kind == "battery"))
                if not ids and flow and flow.ids is None:
                    ids = None  # Inventory may still be loading; psutil remains mandatory.
                identities = {d.id: {key: str(field.value) for key, field in d.fields.items() if key in {"unique_id", "serial"}
                                    and field.availability == "available" and field.value not in (None, "")}
                              for d in raw.devices if d.kind == "battery"}
                frame = {**sample, **temperatures, "elapsed": elapsed, "state": "running", "quality": quality.result(self.config),
                         "battery_percent": battery.percent if battery else None, "power_plugged": battery.power_plugged if battery else None,
                         "battery_devices": identities,
                         "log_folder": str(log.folder), "power_warning": power.warning}
                self.frames.publish(frame)
                log.event("sample", **frame)
                if hot:
                    status, reason = "interrupted", hot
                    break
                if flow:
                    ending = flow.check(battery, elapsed, ids, identities)
                    if ending:
                        status, reason = ending
                        break
                self._stop.wait(max(0, 1 - (time.monotonic() - tick)))
            else:
                status, reason = ("interrupted", self._interruption) if self._interruption else ("cancelled", "Sesión detenida por el usuario.")
        except Exception as error:
            status, reason = "error", str(error)
        finally:
            if started is not None:
                elapsed = max(elapsed, time.monotonic() - started)
            self.frames.publish({"state": "stopping", "message": "Liberando la carga y restaurando los ajustes…"})
            if client:
                try:
                    client.request("stop")
                except Exception as error:
                    if status in {"passed", "completed"}:
                        status, reason = "error", "La carga se cerró de forma forzada: " + str(error)
                finally:
                    try:
                        client.close()
                    except Exception as error:
                        status, reason = "error", "No se pudo cerrar el auxiliar: " + str(error)
            if power:
                try:
                    power.__exit__()
                except Exception as error:
                    status, reason = "error", "No se pudieron restaurar los ajustes: " + str(error)
            validity = quality.result(self.config)
            battery_outcome = status if self.battery else None
            if status in {"passed", "completed"} and not validity["valid"]:
                status, reason = "invalid_profile", "Medición terminada, pero la carga no cumplió el perfil solicitado."
            result = {"status": status, "reason": reason, "battery_outcome": battery_outcome, "elapsed_seconds": elapsed, "quality": validity,
                      "last_sample": sample, "load_config": asdict(self.config), "battery_config": asdict(self.battery) if self.battery else None,
                      "power_warning": power.warning if power else None, "log_folder": str(log.folder) if log else None}
            try:
                if log:
                    log.finish(result)
            except Exception as error:
                result["status"] = "error"
                result["reason"] = "No se pudo guardar el resultado: " + str(error)
            finally:
                try:
                    pythoncom.CoUninitialize()
                finally:
                    self.result.emit(result)
