"""GUI adapter for already prepared monitoring frames. No hardware queries here."""
from functools import partial
from pathlib import Path
import sys

from PySide6.QtCore import QProcess, QTimer, Qt, Signal, Slot
from PySide6.QtWidgets import QHeaderView, QMessageBox, QTableWidgetItem, QWidget

from Jobs.Hardware import HardwareWorker
from ui.hardware_ui import Ui_HardwarePanel
from .formatting import format_field, value
from .models import Field, Snapshot
from .table_model import HardwareTableModel


class HardwarePanel(QWidget):
    stopped = Signal()

    def __init__(self, window, start=True):
        super().__init__(window.ui.tabHardware)
        self.window = window
        self.ui = Ui_HardwarePanel()
        self.ui.setupUi(self)
        window.ui.hardwareContainer.addWidget(self)
        self.current = Snapshot()
        self._frame = None
        self._summary_devices = None
        self._closing = False
        self._setup = None
        self._qr_health = None
        self.detail_models = []
        for table in (self.ui.BatteryDetails, self.ui.DiskDetails, self.ui.CpuDetails, self.ui.GpuDetails):
            model = HardwareTableModel(("Dispositivo", "Dato", "Valor"), table)
            table.setModel(model)
            self.detail_models.append(model)
            self.configure_table(table, (190, 215, 250))
        self.sensor_model = HardwareTableModel(("Dispositivo", "Sensor", "Actual", "Mínimo", "Máximo", "Unidad", "Estado"), self.ui.SensorReadings)
        self.ui.SensorReadings.setModel(self.sensor_model)
        self.configure_table(self.ui.SensorReadings, (170, 220, 75, 75, 75, 60, 130))
        self.worker = HardwareWorker(self)
        self.thread = self.worker  # Public lifecycle handle retained for the main window.
        self.worker.finished.connect(self._worker_finished, Qt.QueuedConnection)
        self.ui.RefreshHardware.clicked.connect(lambda: self.worker.refresh())
        self.ui.ResetSensorHistory.clicked.connect(self.reset_history)
        self.ui.PrepareSensors.clicked.connect(self.prepare_sensors)
        self.ui.HardwareTabs.currentChanged.connect(self.render_current_tab)
        window.ui.tabWidget.currentChanged.connect(self.render_current_tab)
        # Pull only the latest frame: slow rendering cannot queue old measurements.
        self.expiry = QTimer(self)
        self.expiry.setInterval(250)
        self.expiry.timeout.connect(self.poll_frame)
        self.expiry.start()
        for title, index in (("Baterías", 0), ("Discos", 1), ("CPU / RAM / placa", 2), ("GPU", 3), ("Sensores", 4)):
            action = window.ui.menuTools.addAction(title)
            action.triggered.connect(partial(self.open_details, index))
        window.ui.menuTools.addSeparator()
        if start:
            self.worker.start()

    @staticmethod
    def configure_table(table, widths):
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        for column, width in enumerate(widths):
            table.setColumnWidth(column, width)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(26)
        table.setWordWrap(False)
        table.setAlternatingRowColors(True)

    def open_details(self, index, checked=False):
        self.window.ui.tabWidget.setCurrentWidget(self.window.ui.tabHardware)
        self.ui.HardwareTabs.setCurrentIndex(index)
        self.render_current_tab()

    @Slot()
    def poll_frame(self):
        if self._closing:
            return
        frame = self.worker.frames.take()
        if frame is not None:
            self.update_frame(frame)
        self.sensor_model.expire()

    @Slot(object)
    def update_frame(self, frame):
        if self._closing:
            return
        self._frame = frame
        self.current = frame.snapshot
        if self.ui.HardwareStatus.text() != frame.status:
            self.ui.HardwareStatus.setText(frame.status)
            self.ui.HardwareStatus.setToolTip(frame.status_tooltip)
        if self._summary_devices != frame.snapshot.devices:
            self._summary_devices = frame.snapshot.devices
            self.render_summary()
        self.render_current_tab()

    @Slot()
    @Slot(int)
    def render_current_tab(self, index=None):
        if self._closing or self._frame is None or self.window.ui.tabWidget.currentWidget() is not self.window.ui.tabHardware:
            return
        index = self.ui.HardwareTabs.currentIndex()
        if index == 4:
            self.sensor_model.set_rows(self._frame.sensors)
        else:
            self.detail_models[index].set_rows(self._frame.details[index])

    @staticmethod
    def fill(table, rows):
        """Incremental updates for the small legacy summary tables."""
        table.setUpdatesEnabled(False)
        try:
            if table.rowCount() != len(rows):
                table.setRowCount(len(rows))
            for row, cells in enumerate(rows):
                for column, text in enumerate(cells):
                    text = str(text)
                    item = table.item(row, column)
                    if item is None:
                        table.setItem(row, column, QTableWidgetItem(text))
                    elif item.text() != text:
                        item.setText(text)
        finally:
            table.setUpdatesEnabled(True)

    def render_summary(self):
        ui = self.window.ui
        batteries = [d for d in self.current.devices if d.kind == "battery"]
        disks = [d for d in self.current.devices if d.kind == "disk"]
        gpus = [d for d in self.current.devices if d.kind == "gpu"]
        for table, devices, keys, labels in (
            (ui.TableBatteryInfo, batteries, ("name", "manufacturer", "serial", "full_capacity", "design_capacity", "health", "cycles"),
             ("Modelo", "Fabricante", "Serie", "Capacidad completa", "Capacidad de diseño", "Salud", "Ciclos")),
            (ui.TableStorage, disks, ("model", "capacity", "health_status", "interface", "host_reads", "host_writes", "power_on_count", "power_on_hours"),
             ("Modelo", "Capacidad", "Salud", "Interfaz", "Lecturas acumuladas", "Escrituras acumuladas", "Encendidos", "Horas encendido"))):
            names = [d.name for d in devices]
            if table.columnCount() != len(devices):
                table.setColumnCount(len(devices))
            if table.rowCount() != len(keys):
                table.setRowCount(len(keys))
            if [table.horizontalHeaderItem(i).text() if table.horizontalHeaderItem(i) else "" for i in range(len(names))] != names:
                table.setHorizontalHeaderLabels(names)
            table.setVerticalHeaderLabels(labels)
            rows = [tuple(format_field(device.fields.get(key, Field())) for device in devices) for key in keys]
            self.fill(table, rows)
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

    @Slot()
    def reset_history(self):
        self.worker.reset_history()

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

    @Slot()
    def _worker_finished(self):
        if self._closing:
            self.stopped.emit()

    def close_module(self, wait=True):
        self._closing = True
        self.expiry.stop()
        self.worker.stop()
        if wait:
            self.worker.wait(10000)
        return not self.worker.isRunning()
