import threading
import time
from dataclasses import replace
from datetime import datetime, timezone

from PySide6.QtCore import QThread
import psutil
from modules.hardware import client, HardwareError, Field, ProviderError, Snapshot, Reading
from modules.hardware.presentation import FrameBuilder, LatestFrame


class HardwareWorker(QThread):
    """Dedicated polling/formatting thread. It never accesses a Qt widget."""
    def __init__(self, parent=None, hardware_client=None, interval=1):
        super().__init__(parent)
        self.setObjectName("PatiaHardwareMonitor")
        self.client = hardware_client if hardware_client is not None else client
        self.interval = interval
        self.frames = LatestFrame()
        self.builder = FrameBuilder()
        self._stop = threading.Event()
        self._refresh = threading.Event()
        self._restart = threading.Event()
        self._reset_history = threading.Event()

    def stop(self):
        self._stop.set()

    def refresh(self):
        self._refresh.set()

    def restart(self):
        self._restart.set()

    def reset_history(self):
        self._reset_history.set()

    def run(self):
        previous_io = {}
        previous_time = time.monotonic()
        operation = "inventory"
        failures = {}
        last = Snapshot()
        try:
            while not self._stop.is_set():
                iteration_start = time.monotonic()
                if self._restart.is_set():
                    self._restart.clear()
                    self.client.restart()
                    operation = "inventory"
                if self._refresh.is_set():
                    self._refresh.clear()
                    operation = "refresh_devices"
                try:
                    current = self.client.request(operation)
                    operation = "sample"
                    for provider in ("battery", "storage", "sensors", "gpu", "inventory", "disk_inventory"):
                        timed_out = any(e.provider == provider and e.code == "timeout" for e in current.errors)
                        failures[provider] = failures.get(provider, 0) + 1 if timed_out else 0
                    if any(count >= 10 for count in failures.values()):
                        self.client.restart()
                        failures.clear()
                    last = current
                except HardwareError as ex:
                    # Preserve inventory but make old measurements expire by their original timestamps.
                    expired = tuple(replace(d, fields={k: replace(f, availability="stale", reason="El componente no está disponible; dato anterior.")
                                                       for k, f in d.fields.items()}) for d in last.devices)
                    current = replace(last, devices=expired, errors=last.errors + (ProviderError("host", "unavailable", str(ex)),))
                devices = list(current.devices)
                now = datetime.now(timezone.utc)
                readings = list(current.readings)
                try:
                    counters = psutil.disk_io_counters(perdisk=True) or {}
                    tick = time.monotonic()
                    elapsed = tick - previous_time
                    for device in devices:
                        if device.kind != "disk":
                            continue
                        number = device.fields.get("drive_number", Field()).value
                        name = f"PhysicalDrive{number}"
                        counter = counters.get(name)
                        old = previous_io.get(device.id)
                        if counter and old and elapsed > 0:
                            for key in ("read_bytes", "write_bytes"):
                                delta = getattr(counter, key) - getattr(old, key)
                                if delta >= 0:
                                    readings.append(Reading(device.id + ":" + key, device.id,
                                                            "Lectura actual" if key == "read_bytes" else "Escritura actual",
                                                            delta / elapsed, "B/s", "psutil/Windows", now))
                        if counter:
                            previous_io[device.id] = counter
                    previous_io = {k: v for k, v in previous_io.items() if any(d.id == k for d in devices)}
                    previous_time = tick
                except (OSError, RuntimeError):
                    pass
                if self._reset_history.is_set():
                    self._reset_history.clear()
                    self.builder.history.reset()
                self.frames.publish(self.builder.build(Snapshot(tuple(devices), tuple(readings), current.errors)))
                self._stop.wait(max(0, self.interval - (time.monotonic() - iteration_start)))
        finally:
            self.client.close()
