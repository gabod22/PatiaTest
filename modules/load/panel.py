from pathlib import Path

from PySide6.QtCore import QTimer, Qt, Signal, Slot, QUrl
from PySide6.QtGui import QDesktopServices, QIntValidator
from PySide6.QtWidgets import QWidget, QMessageBox

from ui.load_controls_ui import Ui_LoadControls
from ui.load_panel_ui import Ui_LoadPanel
from .models import LoadConfig, BatteryConfig
from .session import CapabilityProbe, LoadSession
from .logging import log_root


class LoadControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LoadControls()
        self.ui.setupUi(self)
        self.ui.Profile.addItems(("Básico · CPU 20 / GPU 0", "Intermedio · CPU 50 / GPU 30", "Exigente · CPU 100 / GPU 100", "Personalizado"))
        for combo in (self.ui.CpuTarget, self.ui.GpuTarget):
            combo.addItems([str(i) for i in range(0, 101, 10)])
            combo.lineEdit().setValidator(QIntValidator(0, 100, combo))
            combo.lineEdit().textEdited.connect(lambda: self.ui.Profile.setCurrentIndex(3))
            combo.activated.connect(lambda: self.ui.Profile.setCurrentIndex(3))
        self.ui.Cores.addItem("Automático", 0)
        self.ui.Profile.currentIndexChanged.connect(self.profile_changed)
        self.profile_changed(0)

    @Slot(int)
    def profile_changed(self, index):
        if index < 3:
            cpu, gpu = ((20, 0), (50, 30), (100, 100))[index]
            self.ui.CpuTarget.setCurrentText(str(cpu))
            self.ui.GpuTarget.setCurrentText(str(gpu))
            if not getattr(self, "gpu_available", True) and gpu:
                self.ui.GpuTarget.setCurrentText("0")
                self.ui.Profile.setCurrentIndex(3)

    def capabilities(self, cap):
        old_cores, old_gpu = self.ui.Cores.currentData(), self.ui.Adapter.currentData()
        self.ui.Cores.clear(); self.ui.Cores.addItem("Automático", 0)
        for count in range(1, cap.get("physical_cores", 0) + 1):
            self.ui.Cores.addItem(f"{count} físicos (ampliables)", count)
        self.ui.Cores.setCurrentIndex(max(0, self.ui.Cores.findData(old_cores)))
        self.ui.Adapter.clear()
        for gpu in sorted(cap.get("gpus", []), key=lambda g: g["dedicated_memory"], reverse=True):
            self.ui.Adapter.addItem(gpu["name"], gpu["id"])
        if self.ui.Adapter.findData(old_gpu) >= 0:
            self.ui.Adapter.setCurrentIndex(self.ui.Adapter.findData(old_gpu))
        self.ui.Adapter.setToolTip("La carga gráfica requiere Direct3D 11 y contadores válidos de Windows; se comprueban al iniciar.")
        self.gpu_available = bool(cap.get("gpu_counter") and cap.get("gpus"))
        self.ui.GpuTarget.setEnabled(self.gpu_available)
        self.ui.Adapter.setEnabled(self.gpu_available)
        if not self.gpu_available:
            self.ui.GpuTarget.setToolTip(cap.get("gpu_error") or "GPU deshabilitada: no hay adaptador o contadores compatibles. Usa un objetivo GPU de 0 %.")
            self.ui.GpuTarget.setCurrentText("0")
            self.ui.Profile.setCurrentIndex(3)

    def config(self):
        try:
            return LoadConfig(int(self.ui.CpuTarget.currentText()), int(self.ui.GpuTarget.currentText()), self.ui.Cores.currentData() or 0,
                              self.ui.Adapter.currentData(), self.ui.CpuLimit.value(), self.ui.GpuLimit.value()).validate()
        except ValueError as error:
            raise ValueError("Revisa los porcentajes de carga. " + str(error)) from error


class LoadPanel(QWidget):
    stopped = Signal()
    def __init__(self, window, probe=True):
        super().__init__(window.ui.tabLoad)
        self.window = window
        self.ui = Ui_LoadPanel(); self.ui.setupUi(self)
        window.ui.loadContainer.addWidget(self)
        self.controls = LoadControls(self)
        self.ui.ControlsLayout.addWidget(self.controls)
        self.battery_controls = LoadControls(window.ui.BatteryLoadHolder)
        window.ui.BatteryLoadControlsLayout.addWidget(self.battery_controls)
        self.session = None
        self.owner = None
        self.last_result = None
        self._closing = False
        self._last_log_minute = -1
        self.ui.Start.clicked.connect(self.start_standalone)
        self.ui.Apply.clicked.connect(self.apply_changes)
        self.ui.Stop.clicked.connect(self.stop_standalone)
        self.ui.OpenLogs.clicked.connect(self.open_logs)
        window.ui.EnableBatteryLoad.toggled.connect(self.battery_controls.setEnabled)
        window.ui.CbxBetteryTestType.currentTextChanged.connect(self.battery_mode_changed)
        window.ui.menuTools.addAction("Carga CPU/GPU", lambda: window.ui.tabWidget.setCurrentWidget(window.ui.tabLoad))
        self.timer = QTimer(self); self.timer.setInterval(250); self.timer.timeout.connect(self.poll); self.timer.start()
        self.probe = CapabilityProbe(self)
        self.probe.available.connect(self.on_capabilities, Qt.QueuedConnection)
        self.probe.finished.connect(self.probe_finished, Qt.QueuedConnection)
        self.refresh_preferences()
        self.battery_mode_changed(window.ui.CbxBetteryTestType.currentText())
        self.update_buttons()
        if probe:
            self.probe.start()

    def refresh_preferences(self):
        values = self.window.config.get("BATTERY_TEST", {})
        self.window.ui.SpinTimeToTest.setValue(values.get("DEFAULT_TIME_TO_TEST", 120))
        self.window.ui.BatteryCutoff.setValue(values.get("DISCHARGE_CUTOFF", 10))

    @Slot(str)
    def battery_mode_changed(self, text):
        intensive = text == "Intensiva"
        self.window.ui.EnableBatteryLoad.setChecked(intensive)
        self.battery_controls.ui.Profile.setCurrentIndex(2 if intensive else 0)
        self.battery_controls.setEnabled(intensive)
        timed = text == "Por tiempo"
        self.window.ui.SpinTimeToTest.setVisible(timed)
        self.window.ui.lbMinutestime.setVisible(timed)
        self.window.ui.BatteryCutoff.setEnabled(not timed)

    @Slot(object)
    def on_capabilities(self, cap):
        self.controls.capabilities(cap); self.battery_controls.capabilities(cap)
        self.ui.State.setText(cap.get("error") or f"{cap['physical_cores']} núcleos físicos / {cap.get('logical_cpus', 0)} hilos. Preparado.")

    def start_session(self, config, battery=None):
        if self.session is not None:
            raise ValueError("Ya existe una sesión activa. Detén esa sesión antes de iniciar otra.")
        self.last_result = None
        self.owner = "battery" if battery else "standalone"
        hardware = self.window.hardware_panel.worker.latest_snapshot
        self.session = LoadSession(config, battery, hardware, self)
        self.session.result.connect(self.on_result, Qt.QueuedConnection)
        self.session.finished.connect(self.session_finished, Qt.QueuedConnection)
        self._last_log_minute = -1
        if battery:
            self.window.ui.TableBatteryLog.setRowCount(0)
        self.session.start()
        self.update_buttons()

    @Slot()
    def start_standalone(self):
        try:
            self.start_session(self.controls.config())
        except ValueError as error:
            QMessageBox.warning(self, "Carga CPU/GPU", str(error))

    def start_battery(self):
        try:
            mode = {"Por tiempo": "timed", "Intensiva": "intensive", "Exhaustiva": "exhaustive", "Exaustiva": "exhaustive"}[self.window.ui.CbxBetteryTestType.currentText()]
            settings = self.window.config.get("BATTERY_TEST", {})
            config = self.battery_controls.config() if self.window.ui.EnableBatteryLoad.isChecked() else LoadConfig(0, 0)
            if mode == "intensive" and not (config.cpu_target or config.gpu_target):
                raise ValueError("Intensiva requiere una carga mayor que cero; usa Exhaustiva para medir sin carga.")
            battery = BatteryConfig(mode, self.window.ui.SpinTimeToTest.value(), settings.get("MINIMUM_LEFTOVER", 20),
                                    self.window.ui.BatteryCutoff.value(), settings.get("BRIGHTNESS_PERCENT", 100))
            self.start_session(config, battery)
        except (ValueError, KeyError) as error:
            QMessageBox.warning(self, "Prueba de batería", str(error))

    @Slot()
    def apply_changes(self):
        if self.session and self.owner == "standalone":
            try:
                self.session.update_config(self.controls.config())
            except ValueError as error:
                QMessageBox.warning(self, "Carga CPU/GPU", str(error))

    @Slot()
    def stop_standalone(self):
        if self.session and self.owner == "standalone":
            self.session.stop()

    def stop_battery(self):
        if self.session and self.owner == "battery":
            self.session.stop()

    def interrupt(self, reason):
        if self.session:
            self.session.interrupt(reason)

    def update_buttons(self):
        active = self.session is not None
        self.ui.Start.setEnabled(not active and not self._closing)
        self.ui.Stop.setEnabled(active and self.owner == "standalone" and not self._closing)
        self.ui.Apply.setEnabled(active and self.owner == "standalone" and not self._closing)
        self.controls.setEnabled(not active or self.owner == "standalone")
        self.window.ui.BtnStartBatteryTest.setEnabled(not active and not self._closing)
        self.window.ui.BtnStopBatteryTest.setEnabled(active and self.owner == "battery" and not self._closing)
        self.window.ui.BatteryLoadOptions.setEnabled(not active)
        self.window.ui.CbxBetteryTestType.setEnabled(not active)
        self.window.ui.SpinTimeToTest.setEnabled(not active)

    @Slot()
    def poll(self):
        if self.session is None:
            return
        frame = self.session.frames.take()
        if frame is None:
            return
        if frame.get("state") != "running":
            text = frame.get("message", frame.get("state", ""))
        else:
            def n(value):
                return "No disponible" if value is None else f"{value:.1f}"
            quality = frame.get("quality", {}).get("compliance_percent")
            text = (f"CPU: {n(frame.get('cpu_actual'))} % / objetivo {frame.get('cpu_target', 0)} % · "
                    f"GPU: {n(frame.get('gpu_actual'))} % / objetivo {frame.get('gpu_target', 0)} %\n"
                    f"Núcleos activos: {frame.get('active_cores', 0)} · Cumplimiento: {n(quality)} %\n"
                    f"Temperatura CPU / GPU: {n(frame.get('cpu_temperature'))} / {n(frame.get('gpu_temperature'))} °C\n"
                    + (frame.get("limitation") or frame.get("thermal_warning") or "Regulación activa."))
            if frame.get("power_warning"):
                text += "\n" + frame["power_warning"]
            self.ui.Metrics.setText(text)
            self.ui.State.setText("Sesión de batería" if self.owner == "battery" else "Carga independiente activa")
            elapsed = frame.get("elapsed", 0)
            from modules.utils import secs2hours
            if self.owner == "battery":
                self.window.ui.LBTimeElapsed.setText(secs2hours(elapsed))
                minute = int(elapsed // 60)
                if minute != self._last_log_minute:
                    self._last_log_minute = minute
                    self.add_battery_row(frame)
        self.window.ui.BatteryLoadStatus.setText(text if self.owner == "battery" else "Carga independiente activa." )

    def add_battery_row(self, frame):
        from PySide6.QtWidgets import QTableWidgetItem
        from modules.utils import secs2hours
        table = self.window.ui.TableBatteryLog
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(("Tiempo", "Batería", "Alimentación", "CPU real/objetivo", "GPU real/objetivo"))
        row = table.rowCount(); table.insertRow(row)
        def metric(name):
            value = frame.get(name + "_actual")
            return f"{value:.1f} / {frame.get(name + '_target', 0)} %" if value is not None else "No disponible"
        for column, value in enumerate((secs2hours(frame["elapsed"]), str(frame.get("battery_percent")) + " %", "Conectada" if frame.get("power_plugged") else "En batería", metric("cpu"), metric("gpu"))):
            table.setItem(row, column, QTableWidgetItem(value))

    @Slot(object)
    def on_result(self, result):
        self.last_result = result
        names = {"passed": "Aprobada", "completed": "Autonomía medida", "failed": "Criterio de batería incumplido",
                 "cancelled": "Cancelada", "interrupted": "Interrumpida", "invalid_profile": "Perfil no válido", "error": "Error"}
        text = f"{names.get(result['status'], result['status'])}: {result['reason']} · {result['elapsed_seconds']:.1f} s"
        quality = result.get("quality", {})
        if quality.get("applicable"):
            text += " · Perfil válido" if quality.get("valid") else " · Perfil no válido"
        else:
            text += " · Sin perfil de carga"
        if result.get("power_warning"):
            text += " · " + result["power_warning"]
        self.ui.State.setText(text)
        if self.owner == "battery":
            self.window.ui.BatteryLoadStatus.setText(text)
            from modules.utils import secs2hours
            self.window.ui.LBTimeElapsed.setText(secs2hours(result["elapsed_seconds"]))
        self.window.statusBar().showMessage(text, 20000)

    @Slot()
    def session_finished(self):
        session, self.session = self.session, None
        if session:
            session.deleteLater()
        self.owner = None
        self.update_buttons()
        if self._closing and not self.probe.isRunning():
            self.stopped.emit()

    @Slot()
    def probe_finished(self):
        if self._closing and self.session is None:
            self.stopped.emit()

    @Slot()
    def open_logs(self):
        folder = Path(self.last_result["log_folder"]) if self.last_result and self.last_result.get("log_folder") else log_root()
        folder.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    def close_module(self):
        self._closing = True
        if self.session:
            self.session.stop()
        return self.session is None and not self.probe.isRunning()
