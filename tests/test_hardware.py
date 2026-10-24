from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

from modules.hardware import Field, Reading, SensorHistory, Snapshot
from modules.hardware.client import HardwareClient, HardwareError
from modules.hardware.formatting import format_field
from modules.hardware.models import timestamp


class ProtocolTests(unittest.TestCase):
    def client(self, mode, timeout=1):
        client = HardwareClient([sys.executable, "-u", str(Path(__file__).with_name("fake_hardware_host.py")), mode], timeout)
        self.addCleanup(client.close)
        return client

    def test_persistent_child_and_partial_results(self):
        client = self.client("partial")
        first = client.request("inventory")
        pid = client._process.pid
        second = client.request("sample")
        self.assertEqual(client._process.pid, pid)
        self.assertEqual(first.devices, second.devices)
        self.assertIsNone(first.devices[0].fields["health_status"].value)
        self.assertEqual(first.errors[0].provider, "storage")
        child = client._process
        client.close()
        self.assertIsNotNone(child.poll())

    def test_bad_framing_and_crashes_are_recoverable(self):
        for mode in ("bad_id", "bad_version", "malformed", "crash"):
            with self.subTest(mode=mode):
                client = self.client(mode)
                with self.assertRaises(HardwareError):
                    client.request("sample")
                self.assertIsNone(client._process)
                client.command[-1] = "partial"
                client.restart()
                self.assertEqual(len(client.request("inventory").devices), 1)

    def test_timeout_kills_only_owned_child(self):
        client = self.client("hang", timeout=0.2)
        started = time.monotonic()
        with self.assertRaises(HardwareError):
            client.request("sample")
        self.assertLess(time.monotonic() - started, 3)
        self.assertIsNone(client._process)


class ModelTests(unittest.TestCase):
    def test_dotnet_timestamps_on_python310(self):
        for fraction in ("1", "123", "12345", "1234567"):
            result = timestamp("2026-10-23T10:00:00." + fraction + "+00:00")
            self.assertEqual(result.tzinfo, timezone.utc)
        with self.assertRaises(ValueError):
            timestamp("2026-10-23T10:00:00")

    def test_unknown_fields_do_not_overwrite_known_inventory(self):
        def device(id, path, fields):
            return dict(id=id, kind="disk", name="Disk", fields={"path": dict(value=path, availability="available"), **fields})
        data = {"devices": [device("wmi", "PhysicalDrive0", {"serial": dict(value="serial", availability="available")}),
                            device("smart", "physicaldrive0", {"serial": dict(value=None, availability="unavailable"),
                                   "health_status": dict(value="Caution", availability="available")})], "readings": [], "errors": []}
        snapshot = Snapshot.from_response(data)
        self.assertEqual(len(snapshot.devices), 1)
        self.assertEqual(snapshot.devices[0].fields["serial"].value, "serial")
        self.assertEqual(snapshot.devices[0].fields["health_status"].value, "Caution")

    def test_history_ignores_stale_and_missing_values_and_reset(self):
        history = SensorHistory()
        now = datetime.now(timezone.utc)
        reading = Reading("cpu-temp", "cpu", "CPU", 40, "°C", "sensor", now)
        history.update([reading, replace(reading, value=90, timestamp=now - timedelta(seconds=20))])
        history.update([replace(reading, value=50, timestamp=now + timedelta(milliseconds=10)),
                        replace(reading, value=None, availability="unavailable")])
        self.assertEqual(history.extrema["cpu-temp"], (40, 50))
        self.assertTrue(replace(reading, timestamp=now - timedelta(seconds=6)).is_stale())
        self.assertFalse(replace(reading, source="SMART", timestamp=now - timedelta(seconds=31)).is_stale())
        history.reset()
        self.assertEqual(history.extrema, {})

    def test_values_are_not_fabricated_or_clamped(self):
        counter = 2**100 * 512000
        self.assertEqual(Field.from_dict(dict(value=str(counter), source="NVMe SMART", availability="available")).value, counter)
        self.assertEqual(format_field(Field(120, "%", availability="available")), "120 %")
        self.assertEqual(format_field(Field(0, "%", availability="available")), "0 %")
        self.assertEqual(format_field(Field()), "No disponible")
        self.assertEqual(format_field(Field(100, "%", availability="stale")), "No disponible")
        self.assertEqual(format_field(Field(8 * 1024**3, "B", availability="available")), "8.00 GiB")
        with self.assertRaises(ValueError):
            Reading.from_dict(dict(id="x", device_id="x", name="x", value=float("nan"), unit="°C", source="x", timestamp="2026-10-23T10:00:00Z"))


class BatteryTests(unittest.TestCase):
    def test_battery_removal_finishes_both_existing_test_modes(self):
        from Jobs.BatteryTest import BatteryTest
        for mode in ("battery_test", "bytime"):
            worker = BatteryTest()
            errors, finished = [], []
            worker.errorSignal.connect(errors.append)
            worker.finishedSignal.connect(lambda: finished.append(True))
            with patch("Jobs.BatteryTest.psutil.sensors_battery", return_value=None), patch.object(worker, "write_start_line_to_txt"):
                getattr(worker, mode)()
            self.assertEqual(len(errors), 1)
            self.assertEqual(len(finished), 1)


if __name__ == "__main__":
    unittest.main()
