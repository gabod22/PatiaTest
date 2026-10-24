import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from modules.load.models import BatteryConfig, BatteryFlow, LoadConfig, QualityTracker
from modules.load.session import LoadSession, ThermalGuard
from modules.load.power import PowerSession
from modules.hardware import Device, Reading, Snapshot, ProviderError


def battery(percent=80, plugged=False):
    return SimpleNamespace(percent=percent, power_plugged=plugged)


class LoadRulesTests(unittest.TestCase):
    def test_configuration_validation(self):
        for target in (-1, 101, float("nan")):
            with self.assertRaises(ValueError):
                LoadConfig(cpu_target=target).validate()
        with self.assertRaises(ValueError):
            LoadConfig(gpu_target=20).validate()
        self.assertEqual(LoadConfig(0, 0).wire()["cpu_target"], 0)

    def test_monotonic_minutes_and_exact_remaining_boundary(self):
        flow = BatteryFlow(BatteryConfig(duration_minutes=2))
        flow.preflight(battery())
        self.assertIsNone(flow.check(battery(20), 119.99))
        self.assertEqual(flow.check(battery(20), 120)[0], "passed")
        self.assertEqual(flow.check(battery(19.99), 120)[0], "failed")

    def test_autonomy_modes_finish_without_battery_approval(self):
        for mode in ("exhaustive", "intensive"):
            flow = BatteryFlow(BatteryConfig(mode=mode, cutoff=10))
            self.assertIsNone(flow.check(battery(11), 200))
            self.assertEqual(flow.check(battery(10), 201)[0], "completed")

    def test_preflight_and_interruptions(self):
        flow = BatteryFlow(BatteryConfig())
        for value in (None, battery(80, True), battery(20), battery(float("nan"))):
            with self.assertRaises(ValueError):
                flow.preflight(value)
        for value in (None, battery(80, True), battery(float("nan"))):
            self.assertEqual(flow.check(value, 1)[0], "interrupted")
        self.assertIsNone(flow.check(battery(), 1, ("a", "b")))
        self.assertEqual(flow.check(battery(), 2, ("b",))[0], "interrupted")

    def test_replacement_in_same_slot_and_late_identity(self):
        flow = BatteryFlow(BatteryConfig())
        self.assertIsNone(flow.check(battery(), 1, ("slot",), {"slot": {}}))
        self.assertIsNone(flow.check(battery(), 2, ("slot",), {"slot": {"serial": "a"}}))
        self.assertIsNone(flow.check(battery(), 3, ("slot",), {"slot": {}}))
        self.assertEqual(flow.check(battery(), 4, ("slot",), {"slot": {"serial": "b"}})[0], "interrupted")

    def test_joint_compliance_warmup_and_missing_samples(self):
        config = LoadConfig(50, 30, gpu_id="1")
        quality = QualityTracker()
        for elapsed in range(1, 16):
            quality.observe(elapsed, {}, config)
        self.assertEqual(quality.result(config)["evaluated_seconds"], 0)
        for elapsed in range(16, 106):
            quality.observe(elapsed, {"cpu_actual": 55, "gpu_actual": 40}, config)
        for elapsed in range(106, 116):
            quality.observe(elapsed, {"cpu_actual": 50, "gpu_actual": None}, config)
        self.assertTrue(quality.result(config)["valid"])
        self.assertEqual(quality.result(config)["compliance_percent"], 90)
        quality.observe(116, {"cpu_actual": 60, "gpu_actual": 30}, config)
        self.assertFalse(quality.result(config)["valid"])

    def test_zero_load_and_unobserved_intervals(self):
        quality = QualityTracker()
        self.assertTrue(quality.result(LoadConfig(0, 0))["valid"])
        quality.observe(15, {}, LoadConfig())
        quality.observe(25, {"cpu_actual": 20}, LoadConfig())
        self.assertFalse(quality.result(LoadConfig())["valid"])

    def test_thermal_guard_uses_fresh_selected_main_sensor_and_sustained_time(self):
        guard = ThermalGuard()
        now = datetime.now(timezone.utc)
        devices = (Device("c", "sensor_cpu", "CPU", {}), Device("g", "sensor_gpu", "Intel", {}), Device("g2", "sensor_gpu", "NVIDIA", {}))
        def frame(stamp, value):
            return Snapshot(devices, (Reading("c1", "c", "CPU Package", value, "°C", "test", stamp),
                                      Reading("g1", "g", "GPU Core", 50, "°C", "test", stamp),
                                      Reading("g2", "g2", "GPU Core", 110, "°C", "test", stamp),
                                      Reading("g3", "g", "GPU Hot Spot", 110, "°C", "test", stamp)))
        values, reason = guard.evaluate(frame(now - timedelta(seconds=8), 100), "Intel", LoadConfig())
        self.assertIsNone(values["cpu_temperature"])
        for offset in (3, 2, 1):
            values, reason = guard.evaluate(frame(now - timedelta(seconds=offset), 96), "Intel", LoadConfig())
            self.assertIsNone(reason)
        values, reason = guard.evaluate(frame(now, 96), "Intel", LoadConfig())
        self.assertIn("CPU", reason)
        self.assertEqual(values["gpu_temperature"], 50)


class SessionTests(unittest.TestCase):
    def execute(self, config=None, battery_config=None, batteries=None, statuses=None, gap=1, cancel=False, failure=False, hardware=None):
        events, results = [], []
        clock = [100.0]
        class Event:
            stopped = cancel
            def is_set(self): return self.stopped
            def set(self): self.stopped = True
            def wait(self, seconds): clock[0] += gap
        class Client:
            def request(self, operation, config=None):
                events.append(operation)
                if operation == "capabilities": return {"gpus": []}
                if operation == "status":
                    if failure: raise RuntimeError("helper failed")
                    return statuses() if statuses else {"cpu_actual": 20, "gpu_actual": None}
                return {}
            def close(self): events.append("closed")
        class Log:
            folder = Path("build/test-session")
            def __init__(self, *args): pass
            def event(self, *args, **kwargs): pass
            def finish(self, result): events.append("logged")
        class Power:
            warning = None
            def __init__(self, *args): pass
            def __enter__(self): events.append("power_enter")
            def __exit__(self): events.append("power_restored")
        session = LoadSession(config or LoadConfig(0, 0), battery_config or BatteryConfig(duration_minutes=1), hardware=hardware, client_factory=Client, log_factory=Log)
        session._stop = Event()
        session.result.connect(lambda result: (events.append("result"), results.append(result)))
        with patch("modules.load.session.time.monotonic", side_effect=lambda: clock[0]), \
             patch("modules.load.session.psutil.sensors_battery", side_effect=batteries or (lambda: battery())), \
             patch("modules.load.session.PowerSession", Power):
            session.run()
        self.assertEqual(len(results), 1)
        if "start" in events:
            self.assertLess(events.index("stop"), events.index("result"))
            self.assertLess(events.index("closed"), events.index("result"))
        if "power_enter" in events:
            self.assertLess(events.index("power_restored"), events.index("result"))
        return results[0], events

    def test_timed_session_duration_and_single_result_after_cleanup(self):
        result, events = self.execute()
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["elapsed_seconds"], 60)
        self.assertEqual(events.count("stop"), 1)

    def test_no_load_is_started_with_mains_or_missing_battery(self):
        for initial in (None, battery(80, True)):
            result, events = self.execute(batteries=lambda: initial)
            self.assertEqual(result["status"], "error")
            self.assertNotIn("start", events)

    def test_charger_removal_cancel_suspend_and_helper_failure(self):
        for values in ([battery(), battery(70, True)], [battery(), None]):
            result, _ = self.execute(batteries=iter(values).__next__)
            self.assertEqual(result["status"], "interrupted")
        self.assertEqual(self.execute(cancel=True)[0]["status"], "cancelled")
        self.assertEqual(self.execute(gap=6)[0]["status"], "interrupted")
        self.assertEqual(self.execute(failure=True)[0]["status"], "error")

    def test_invalid_profile_and_measurement_loss(self):
        result, _ = self.execute(LoadConfig(50), statuses=lambda: {"cpu_actual": 20})
        self.assertEqual(result["status"], "invalid_profile")
        result, _ = self.execute(LoadConfig(50), statuses=lambda: {})
        self.assertEqual(result["status"], "interrupted")

    def test_active_battery_configuration_is_locked(self):
        session = LoadSession(LoadConfig(), BatteryConfig())
        with self.assertRaises(RuntimeError):
            session.update_config(LoadConfig(50))

    def test_sustained_battery_inventory_error_interrupts_aggregate_battery(self):
        raw = Snapshot(errors=(ProviderError("battery", "query_failed", "slot unavailable"),))
        result, _ = self.execute(hardware=lambda: raw)
        self.assertEqual(result["status"], "interrupted")
        self.assertEqual(result["elapsed_seconds"], 5)


class PowerRestorationTests(unittest.TestCase):
    def test_original_brightness_and_sleep_state_are_restored(self):
        levels, states = [], []
        method = SimpleNamespace(InstanceName="panel", WmiSetBrightness=lambda **kw: levels.append(kw["Brightness"]))
        connection = SimpleNamespace(WmiMonitorBrightness=lambda: [SimpleNamespace(Active=True, InstanceName="panel", CurrentBrightness=44)],
                                     WmiMonitorBrightnessMethods=lambda: [method])
        kernel = SimpleNamespace(SetThreadExecutionState=lambda state: (states.append(state) or 1))
        with patch("modules.load.power.ctypes.windll", SimpleNamespace(kernel32=kernel)), patch.dict("sys.modules", {"wmi": SimpleNamespace(WMI=lambda **kw: connection)}):
            with PowerSession(100) as power:
                self.assertEqual(levels, [100])
        self.assertEqual(levels, [100, 44])
        self.assertEqual(states, [0x80000003, 0x80000000])
        self.assertEqual(power.previous, [])

    def test_failed_brightness_change_still_preserves_restoration(self):
        levels = []
        def set_level(**kw):
            levels.append(kw["Brightness"])
            if kw["Brightness"] == 100:
                raise OSError("brightness error")
        method = SimpleNamespace(InstanceName="panel", WmiSetBrightness=set_level)
        connection = SimpleNamespace(WmiMonitorBrightness=lambda: [SimpleNamespace(Active=True, InstanceName="panel", CurrentBrightness=44)],
                                     WmiMonitorBrightnessMethods=lambda: [method])
        kernel = SimpleNamespace(SetThreadExecutionState=lambda state: 1)
        with patch("modules.load.power.ctypes.windll", SimpleNamespace(kernel32=kernel)), patch.dict("sys.modules", {"wmi": SimpleNamespace(WMI=lambda **kw: connection)}):
            with PowerSession(100) as power:
                self.assertIsNotNone(power.warning)
        self.assertEqual(levels, [100, 44])


if __name__ == "__main__":
    unittest.main()
