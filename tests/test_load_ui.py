import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from pathlib import Path
from types import SimpleNamespace
import threading
import time
import unittest
from unittest.mock import patch

from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QMainWindow
from ui.mainwindow_ui import Ui_MainWindow
from modules.hardware import Snapshot
from modules.load.models import LoadConfig
from modules.load.panel import LoadPanel
from modules.load.session import LoadSession


class LoadUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.window = QMainWindow()
        self.window.ui = Ui_MainWindow(); self.window.ui.setupUi(self.window)
        self.window.config = {"BATTERY_TEST": {"DEFAULT_TIME_TO_TEST": 55, "MINIMUM_LEFTOVER": 22}}
        self.window.hardware_panel = SimpleNamespace(worker=SimpleNamespace(latest_snapshot=Snapshot))
        self.panel = LoadPanel(self.window, probe=False)
        self.panel.on_capabilities({"physical_cores": 6, "logical_cpus": 12, "gpu_counter": True,
                                    "gpus": [{"id": "a", "name": "Intel", "dedicated_memory": 128},
                                             {"id": "b", "name": "NVIDIA", "dedicated_memory": 8 * 1024**3}]})
        self.addCleanup(self.window.close)
        self.addCleanup(self.panel.timer.stop)

    def test_profiles_physical_cores_and_selected_gpu(self):
        controls = self.panel.controls
        controls.ui.Profile.setCurrentIndex(1)
        controls.ui.Cores.setCurrentIndex(2)
        config = controls.config()
        self.assertEqual((config.cpu_target, config.gpu_target, config.initial_cores, config.gpu_id), (50, 30, 2, "b"))
        self.assertEqual(controls.ui.Cores.count(), 7)

    def test_live_battery_preferences_and_default_modes(self):
        self.assertEqual(self.window.ui.SpinTimeToTest.value(), 55)
        self.window.ui.CbxBetteryTestType.setCurrentText("Intensiva")
        self.assertTrue(self.window.ui.EnableBatteryLoad.isChecked())
        self.assertEqual(self.panel.battery_controls.config().cpu_target, 100)
        self.window.ui.CbxBetteryTestType.setCurrentText("Exhaustiva")
        self.assertFalse(self.window.ui.EnableBatteryLoad.isChecked())
        self.window.config["BATTERY_TEST"]["DEFAULT_TIME_TO_TEST"] = 75
        self.panel.refresh_preferences()
        self.assertEqual(self.window.ui.SpinTimeToTest.value(), 75)

    def test_single_session_and_locked_battery_controls(self):
        self.panel.session = SimpleNamespace()
        self.panel.owner = "battery"
        self.panel.update_buttons()
        self.assertFalse(self.panel.controls.isEnabled())
        self.assertFalse(self.window.ui.BatteryLoadOptions.isEnabled())
        self.assertFalse(self.window.ui.BtnStartBatteryTest.isEnabled())
        with self.assertRaises(ValueError):
            self.panel.start_session(LoadConfig())
        self.panel.session = None

    def test_slow_helper_runs_off_gui_thread_and_shutdown_is_asynchronous(self):
        calls, heartbeats = [], []
        main_thread = threading.get_ident()
        class Client:
            def request(self, operation, config=None):
                calls.append(threading.get_ident())
                time.sleep(.15)
                return {"gpus": []} if operation == "capabilities" else {"cpu_actual": 20}
            def close(self): pass
        class Log:
            folder = Path("build/test-session")
            def __init__(self, *args): pass
            def event(self, *args, **kwargs): pass
            def finish(self, result): pass
        class Power:
            warning = None
            def __init__(self, *args): pass
            def __enter__(self): pass
            def __exit__(self): pass
        worker = LoadSession(LoadConfig(0, 0), client_factory=Client, log_factory=Log)
        timer = QTimer(); timer.setInterval(10); timer.timeout.connect(lambda: heartbeats.append(True))
        with patch("modules.load.session.PowerSession", Power), patch("modules.load.session.psutil.sensors_battery", return_value=None):
            timer.start(); worker.start()
            QTest.qWait(650)
            self.panel.session = worker
            begin = time.monotonic()
            self.assertFalse(self.panel.close_module())
            self.assertLess(time.monotonic() - begin, .05)
            QTest.qWait(700)
            worker.wait(1000)
            timer.stop()
        self.panel.session = None
        self.assertFalse(worker.isRunning())
        self.assertGreater(len(heartbeats), 25)
        self.assertTrue(calls)
        self.assertTrue(all(thread != main_thread for thread in calls))


if __name__ == "__main__":
    unittest.main()
