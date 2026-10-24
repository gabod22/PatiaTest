"""Presentation and lifecycle of the hardware module; all queries run in a worker."""
from functools import partial
from pathlib import Path
import sys

from PySide6.QtCore import QProcess, QThread, QTimer, Qt
from PySide6.QtWidgets import QHeaderView, QMessageBox, QTableWidgetItem, QWidget

from Jobs.Hardware import HardwareWorker
from ui.hardware_ui import Ui_HardwarePanel
from .formatting import format_field, value
from .models import Field, SensorHistory, Snapshot


LABELS = {
    "name": "Nombre", "model": "Modelo", "manufacturer": "Fabricante", "serial": "Número de serie",
    "manufacture_date": "Fecha de fabricación", "chemistry": "Química", "design_capacity": "Capacidad de diseño",
    "full_capacity": "Capacidad de carga completa", "current_capacity": "Capacidad actual", "health": "Salud",
    "charge": "Carga actual", "cycles": "Ciclos", "voltage": "Voltaje", "rate": "Carga/descarga",
    "temperature": "Temperatura", "remaining_time": "Autonomía estimada", "power_state": "Estado de alimentación",
    "capacity": "Capacidad", "interface": "Interfaz", "volumes": "Volúmenes", "firmware": "Firmware",
    "health_status": "Estado de salud", "life_remaining": "Vida restante estimada", "percentage_used": "Desgaste reportado",
    "host_reads": "Lecturas acumuladas", "host_writes": "Escrituras acumuladas", "power_on_hours": "Horas encendido",
    "power_on_count": "Encendidos", "smart": "Atributos SMART", "life_calculation": "Cálculo de vida restante",
    "cores": "Núcleos", "threads": "Hilos", "socket": "Zócalo", "max_clock": "Frecuencia máxima nominal",
    "configured_clock": "Frecuencia informada por WMI", "nominal_speed": "Velocidad nominal",
    "configured_speed": "Velocidad configurada", "part_number": "Referencia", "slot": "Ranura", "bank": "Banco",
    "dedicated_memory": "Memoria gráfica dedicada", "shared_memory": "Memoria compartida máxima",
    "memory_type": "Tipo de memoria", "driver_version": "Controlador", "driver_date": "Fecha del controlador",
    "pcie_link": "Enlace PCIe", "capabilities": "Capacidades", "release_date": "Fecha", "revision": "Revisión",
    "cpuid_brand_raw": "Modelo (CPUID)", "cpuid_vendor_id_raw": "Fabricante (CPUID)", "cpuid_arch": "Arquitectura (CPUID)",
    "cpuid_bits": "Bits", "cpuid_family": "Familia (CPUID)", "cpuid_model": "Modelo (CPUID)", "cpuid_stepping": "Stepping (CPUID)",
    "cpuid_flags": "Instrucciones", "cpuid_l1_data_cache_size": "Caché L1 de datos", "cpuid_l1_instruction_cache_size": "Caché L1 de instrucciones",
    "cpuid_l2_cache_size": "Caché L2", "cpuid_l3_cache_size": "Caché L3", "timings": "Temporizaciones",
    "data_width": "Ancho de datos", "total_width": "Ancho total", "configured_voltage": "Voltaje configurado",
    "l2_cache": "Caché L2", "l3_cache": "Caché L3", "architecture": "Arquitectura", "version": "Versión",
    "pci_vendor": "Fabricante PCI", "pci_device": "Dispositivo PCI", "pci_subsystem": "Subsistema PCI",
    "pcie_generation": "Generación PCIe actual", "pcie_width": "Ancho PCIe actual", "memory_bus_width": "Bus de memoria",
    "max_gpu_clock": "Frecuencia máxima de GPU", "max_memory_clock": "Frecuencia máxima de memoria",
}


class HardwarePanel(QWidget):
    def __init__(self, window):
        super().__init__(window.ui.tabHardware)
        self.window = window
        self.ui = Ui_HardwarePanel()
        self.ui.setupUi(self)
        window.ui.hardwareContainer.addWidget(self)
        self.history = SensorHistory()
        self.current = Snapshot()
        self._details = None
        self._closing = False
        self._setup = None
        self._qr_health = None
        for table in (self.ui.BatteryDetails, self.ui.DiskDetails, self.ui.CpuDetails, self.ui.GpuDetails):
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["Dispositivo", "Dato", "Valor", "Fuente", "Disponibilidad / motivo"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            table.horizontalHeader().setStretchLastSection(True)
            table.setWordWrap(False)
        self.ui.SensorReadings.setColumnCount(9)
        self.ui.SensorReadings.setHorizontalHeaderLabels(["Dispositivo", "Sensor", "Actual", "Mínimo", "Máximo", "Unidad", "Fuente", "Estado", "Última lectura"])
        self.ui.SensorReadings.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.SensorReadings.setWordWrap(False)
        self.worker = HardwareWorker()
        self.thread = QThread(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.snapshot.connect(self.update_snapshot)
        self.worker.finished.connect(self.thread.quit, Qt.DirectConnection)
        self.thread.finished.connect(self.worker.deleteLater)
        self.ui.RefreshHardware.clicked.connect(lambda: self.worker.refresh())
        self.ui.ResetSensorHistory.clicked.connect(self.reset_history)
        self.ui.PrepareSensors.clicked.connect(self.prepare_sensors)
        self.expiry = QTimer(self)
        self.expiry.setInterval(1000)
        self.expiry.timeout.connect(self.render_sensors)
        self.expiry.start()
        for title, index in (("Baterías", 0), ("Discos", 1), ("CPU / RAM / placa", 2), ("GPU", 3), ("Sensores", 4)):
            action = window.ui.menuTools.addAction(title)
            action.triggered.connect(partial(self.open_details, index))
        window.ui.menuTools.addSeparator()
        self.thread.start()

    def open_details(self, index, checked=False):
        self.window.ui.tabWidget.setCurrentWidget(self.window.ui.tabHardware)
        self.ui.HardwareTabs.setCurrentIndex(index)

    @staticmethod
    def fill(table, rows):
        scroll = table.verticalScrollBar().value()
        table.setUpdatesEnabled(False)
        try:
            table.setRowCount(len(rows))
            for row, cells in enumerate(rows):
                for column, text in enumerate(cells):
                    item = QTableWidgetItem(str(text))
                    item.setToolTip(str(text))
                    table.setItem(row, column, item)
        finally:
            table.setUpdatesEnabled(True)
            table.verticalScrollBar().setValue(scroll)

    def update_snapshot(self, snapshot):
        if self._closing:
            return
        self.current = snapshot
        self.history.update(snapshot.readings)
        errors = list(dict.fromkeys(e.message for e in snapshot.errors))
        summary = errors[:2] + ([f"{len(errors) - 2} avisos adicionales (ver detalle al pasar el cursor)."] if len(errors) > 2 else [])
        self.ui.HardwareStatus.setText(" · ".join(summary) if summary else f"{len(snapshot.devices)} componentes consultados. Monitoreo activo.")
        self.ui.HardwareStatus.setToolTip("\n".join(f"{e.provider}: {e.code}: {e.message}" for e in snapshot.errors))
        if self._details != snapshot.devices:
            self._details = snapshot.devices
            groups = [(self.ui.BatteryDetails, {"battery"}), (self.ui.DiskDetails, {"disk"}),
                      (self.ui.CpuDetails, {"cpu", "memory", "board", "bios", "sensor_cpu", "sensor_memory", "sensor_board"}),
                      (self.ui.GpuDetails, {"gpu", "gpu_vendor", "sensor_gpu"})]
            for table, kinds in groups:
                rows = []
                for device in snapshot.devices:
                    if device.kind not in kinds:
                        continue
                    for key, field in device.fields.items():
                        availability = field.reason or ("Disponible" if field.availability == "available" else "No disponible")
                        if key == "smart" and isinstance(field.value, list) and field.availability == "available":
                            for attribute in field.value:
                                label = f"SMART {attribute.get('id', '')}: {attribute.get('type', '')}"
                                text = "; ".join(f"{name}: {attribute[k]}" for k, name in (("current", "Actual"), ("worst", "Peor"), ("threshold", "Umbral"), ("raw_decimal", "Raw"), ("raw_hex", "Hex (bytes originales)")) if attribute.get(k) is not None)
                                rows.append((device.name, label, text, field.source, availability))
                        else:
                            text = ", ".join(map(str, field.value)) if isinstance(field.value, list) and field.availability == "available" else format_field(field)
                            rows.append((device.name, LABELS.get(key, key), text, field.source, availability))
                self.fill(table, rows)
            self.render_summary()
        self.render_sensors()

    def render_summary(self):
        ui = self.window.ui
        batteries = [d for d in self.current.devices if d.kind == "battery"]
        disks = [d for d in self.current.devices if d.kind == "disk"]
        gpus = [d for d in self.current.devices if d.kind == "gpu"]
        for table, devices, keys in (
            (ui.TableBatteryInfo, batteries, ("name", "manufacturer", "manufacture_date", "serial", "full_capacity", "design_capacity", "health", "cycles")),
            (ui.TableStorage, disks, ("model", "capacity", "health_status", "interface", "host_reads", "host_writes", "power_on_count", "power_on_hours"))):
            table.clearContents()
            table.setColumnCount(len(devices))
            table.setHorizontalHeaderLabels([d.name for d in devices])
            for column, device in enumerate(devices):
                for row, key in enumerate(keys):
                    field = device.fields.get(key, Field())
                    item = QTableWidgetItem(format_field(field))
                    item.setToolTip(field.reason or field.source)
                    table.setItem(row, column, item)
        self.fill(ui.TableGPUs, [(d.name, value(d, "manufacturer"), value(d, "dedicated_memory"), value(d, "memory_type")) for d in gpus])
        health = ", ".join(value(d, "health") for d in batteries)
        if not batteries:
            health = "No disponible" if any(e.provider in {"battery", "host"} for e in self.current.errors) else "Sin batería"
        ui.TextBatteryHealth.setText(health)
        if self._qr_health != health and getattr(self.window, "systeminfo", None):
            import qrcode
            from PIL.ImageQt import ImageQt
            from PySide6.QtGui import QPixmap
            image = qrcode.make({"model": ui.TextModel.text(), "serial": ui.TextServiceNumber.text(), "battery": health,
                                 "cpu": ui.TextProcessorName.text(), "ram": ui.TextTotalRAM.text()})
            ui.LBQrCode.setPixmap(QPixmap.fromImage(ImageQt(image.get_image())))
            self._qr_health = health
        for widget in (ui.TextBatteryHealth, ui.label_6):
            widget.show()
        if batteries:
            ui.tabBatteryTest.setEnabled(True)

    def render_sensors(self):
        if self._closing:
            return
        names = {d.id: d.name for d in self.current.devices}
        rows = []
        for reading in self.current.readings:
            stale = reading.is_stale()
            lo, hi = self.history.extrema.get(reading.id, (None, None))
            number = lambda value: "—" if value is None else f"{value:.2f}"
            rows.append((names.get(reading.device_id, reading.device_id), reading.name,
                         "—" if stale or reading.availability != "available" else number(reading.value),
                         number(lo), number(hi), reading.unit, reading.source,
                         "Caducada" if stale else reading.reason or ("Disponible" if reading.availability == "available" else "No disponible"),
                         reading.timestamp.astimezone().strftime("%H:%M:%S")))
        # Explain absent temperature sensors instead of inventing a zero.
        for device in self.current.devices:
            if device.kind not in {"cpu", "memory", "gpu", "disk", "sensor_cpu", "sensor_gpu", "sensor_memory", "sensor_board"}:
                continue
            if device.kind in {"cpu", "memory", "gpu"} and any(d.kind == "sensor_" + device.kind for d in self.current.devices):
                continue
            if not any(r.device_id == device.id and r.unit == "°C" for r in self.current.readings):
                rows.append((device.name, "Temperatura", "—", "—", "—", "°C", "", "No disponible: sensor no expuesto o acceso no preparado", ""))
        self.fill(self.ui.SensorReadings, rows)

    def reset_history(self):
        self.history.reset()
        self.history.update(self.current.readings)
        self.render_sensors()

    def prepare_sensors(self):
        if self._setup is not None:
            return
        root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
        script = root / "scripts/prepare-sensors.ps1"
        if not script.is_file():
            QMessageBox.warning(self, "Preparación de sensores", "No se encontró el preparador de sensores en este paquete.")
            return
        self._setup = QProcess(self)
        self._setup.setProgram("powershell.exe")
        self._setup.setArguments(["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), "-PackageRoot", str(root)])
        self._setup.finished.connect(self._setup_finished)
        self._setup.errorOccurred.connect(self._setup_error)
        self.ui.PrepareSensors.setEnabled(False)
        self._setup.start()

    def _setup_error(self, error):
        if self._setup is not None:
            self._setup_finished(-1)

    def _setup_finished(self, code, status=None):
        process, self._setup = self._setup, None
        if process is None:
            return
        output = bytes(process.readAllStandardError()).decode("utf-8", errors="replace")
        process.deleteLater()
        self.ui.PrepareSensors.setEnabled(True)
        if code == 0:
            self.worker.restart()
            QMessageBox.information(self, "Sensores", "Preparación completada. Se volverán a consultar los sensores.")
        else:
            QMessageBox.warning(self, "Sensores", "No se completó la preparación.\n" + output[-2000:])

    def close_module(self):
        self._closing = True
        self.expiry.stop()
        self.worker.stop()
        # The native client has a bounded request timeout and owns its child.
        self.thread.quit()
        self.thread.wait(10000)
