import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import patch

from PySide6.QtWidgets import QApplication, QMainWindow
from ui.mainwindow_ui import Ui_MainWindow
from modules.hardware import Device, Field, Reading, Snapshot
from modules.hardware.panel import HardwarePanel


class HardwareUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.window = QMainWindow()
        self.window.ui = Ui_MainWindow()
        self.window.ui.setupUi(self.window)
        with patch("Jobs.Hardware.HardwareWorker.run", lambda worker: None):
            self.panel = HardwarePanel(self.window)
        self.addCleanup(self.window.close)
        self.addCleanup(self.panel.close_module)

    def test_dynamic_tables_and_unavailable_fields(self):
        devices = []
        for kind in ("battery", "disk", "gpu"):
            for i in range(7):
                devices.append(Device(f"{kind}:{i}", kind, f"{kind} {i}", {"name": Field(f"{kind} {i}", availability="available")}))
        self.panel.update_snapshot(Snapshot(tuple(devices)))
        self.assertEqual(self.window.ui.TableBatteryInfo.columnCount(), 7)
        self.assertEqual(self.window.ui.TableStorage.columnCount(), 7)
        self.assertEqual(self.window.ui.TableGPUs.rowCount(), 7)
        self.assertEqual(self.window.ui.TableStorage.item(2, 0).text(), "No disponible")
        self.panel.open_details(4)
        self.assertIs(self.window.ui.tabWidget.currentWidget(), self.window.ui.tabHardware)
        self.assertEqual(self.panel.ui.HardwareTabs.currentIndex(), 4)

    def test_stale_sensor_is_not_shown_as_current(self):
        reading = Reading("temperature", "cpu", "CPU", 50, "°C", "test", datetime.now(timezone.utc) - timedelta(seconds=20))
        self.panel.update_snapshot(Snapshot(readings=(reading,)))
        self.assertEqual(self.panel.ui.SensorReadings.item(0, 2).text(), "—")
        self.assertEqual(self.panel.ui.SensorReadings.item(0, 7).text(), "Caducada")
        self.assertEqual(self.panel.history.extrema, {})


if __name__ == "__main__":
    unittest.main()
