import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from datetime import datetime, timedelta, timezone
import unittest
import threading
import time

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, Qt
from PySide6.QtTest import QTest
from ui.mainwindow_ui import Ui_MainWindow
from modules.hardware import Device, Field, Reading, Snapshot
from modules.hardware.panel import HardwarePanel
from modules.hardware.presentation import FrameBuilder, DisplayRow
from modules.hardware.table_model import HardwareTableModel


class HardwareUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.window = QMainWindow()
        self.window.ui = Ui_MainWindow()
        self.window.ui.setupUi(self.window)
        self.panel = HardwarePanel(self.window, start=False)
        self.addCleanup(self.window.close)
        self.addCleanup(self.panel.close_module)

    def test_dynamic_tables_and_unavailable_fields(self):
        devices = []
        for kind in ("battery", "disk", "gpu"):
            for i in range(7):
                devices.append(Device(f"{kind}:{i}", kind, f"{kind} {i}", {"name": Field(f"{kind} {i}", availability="available")}))
        self.panel.update_frame(FrameBuilder().build(Snapshot(tuple(devices))))
        self.assertEqual(self.window.ui.TableBatteryInfo.columnCount(), 7)
        self.assertEqual(self.window.ui.TableStorage.columnCount(), 7)
        self.assertEqual(self.window.ui.TableGPUs.rowCount(), 7)
        self.assertEqual(self.window.ui.TableStorage.item(2, 0).text(), "No disponible")
        self.panel.open_details(4)
        self.assertIs(self.window.ui.tabWidget.currentWidget(), self.window.ui.tabHardware)
        self.assertEqual(self.panel.ui.HardwareTabs.currentIndex(), 4)

    def test_stale_sensor_is_not_shown_as_current(self):
        reading = Reading("temperature", "cpu", "CPU", 50, "°C", "test", datetime.now(timezone.utc) - timedelta(seconds=20))
        self.panel.open_details(4)
        self.panel.update_frame(FrameBuilder().build(Snapshot(readings=(reading,))))
        model = self.panel.ui.SensorReadings.model()
        self.assertEqual(model.data(model.index(0, 2)), "—")
        self.assertEqual(model.data(model.index(0, 6)), "Caducada")

    def test_stream_changes_values_without_rebuilding_model(self):
        model = HardwareTableModel(("Dispositivo", "Dato", "Valor"))
        resets, changes = [], []
        model.modelReset.connect(lambda: resets.append(True))
        model.dataChanged.connect(lambda *args: changes.append(True))
        model.set_rows((DisplayRow("temp", ("CPU", "Temperatura", "40")),))
        model.set_rows((DisplayRow("temp", ("CPU", "Temperatura", "45")),))
        model.set_rows((DisplayRow("temp", ("CPU", "Temperatura", "45")),))
        self.assertEqual(len(resets), 1)
        self.assertEqual(len(changes), 1)
        self.assertEqual(model.data(model.index(0, 2)), "45")

    def test_readings_expire_even_if_provider_stops_delivering_frames(self):
        reading = Reading("temp", "cpu", "CPU", 50, "°C", "test", datetime.now(timezone.utc))
        self.panel.open_details(4)
        self.panel.update_frame(FrameBuilder().build(Snapshot(readings=(reading,))))
        self.panel.sensor_model.expire(reading.timestamp + timedelta(seconds=6))
        model = self.panel.sensor_model
        self.assertEqual(model.data(model.index(0, 2)), "—")
        self.assertEqual(model.data(model.index(0, 6)), "Caducada")

    def test_slow_polling_and_large_sensor_payload_leave_gui_responsive(self):
        main_thread = threading.get_ident()
        query_threads, paint_threads, heartbeats = [], [], []
        device = Device("cpu", "sensor_cpu", "CPU", {})
        class SlowClient:
            def request(self, operation):
                query_threads.append(threading.get_ident())
                time.sleep(0.35)
                now = datetime.now(timezone.utc)
                readings = [Reading(f"core:{i}", "cpu", f"CPU Core #{i} Thread #1", 30, "%", "test", now) for i in range(2000)]
                readings += [Reading("total", "cpu", "CPU Total", len(query_threads) * 10, "%", "test", now)]
                return Snapshot((device,), tuple(readings))
            def close(self):
                pass
        self.panel.worker.client = SlowClient()
        self.panel.worker.interval = 0.05
        self.panel.open_details(4)
        self.panel.sensor_model.modelReset.connect(lambda: paint_threads.append(threading.get_ident()), Qt.DirectConnection)
        self.panel.sensor_model.dataChanged.connect(lambda *args: paint_threads.append(threading.get_ident()), Qt.DirectConnection)
        timer = QTimer()
        timer.setInterval(10)
        timer.timeout.connect(lambda: heartbeats.append(time.monotonic()))
        timer.start()
        try:
            self.panel.worker.start()
            QTest.qWait(1200)
        finally:
            timer.stop()
        self.assertGreaterEqual(len(query_threads), 2)
        self.assertTrue(all(thread != main_thread for thread in query_threads))
        self.assertTrue(paint_threads)
        self.assertTrue(all(thread == main_thread for thread in paint_threads))
        self.assertGreater(len(heartbeats), 20)
        self.assertLess(max(b - a for a, b in zip(heartbeats, heartbeats[1:])), 0.25)
        self.assertLess(self.panel.sensor_model.rowCount(), 5)
        started = time.monotonic()
        self.panel.close_module(wait=False)
        self.assertLess(time.monotonic() - started, 0.1)
        QTest.qWait(450)
        self.assertFalse(self.panel.thread.isRunning())


if __name__ == "__main__":
    unittest.main()
