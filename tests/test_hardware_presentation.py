from datetime import datetime, timezone
import unittest

from modules.hardware import Device, Field, Reading, Snapshot
from modules.hardware.presentation import FrameBuilder, LatestFrame


class PresentationTests(unittest.TestCase):
    def test_only_useful_metadata_reaches_the_gui(self):
        known = lambda value: Field(value, availability="available")
        disk = Device("disk", "disk", "SSD", {"capacity": known(1000), "health_status": known("Good"),
                       "host_writes": known(120), "smart": known([{"raw": "irrelevant"}] * 1000), "pnp_id": known("internal-id")})
        cpu = Device("cpu", "cpu", "CPU", {"cores": known(8), "threads": known(16), "cpuid_flags": known(["sse"] * 500), "processor_id": known("internal-id")})
        ram = Device("ram", "memory", "DIMM 1", {"capacity": known(16000), "type": known("DDR4"), "nominal_speed": known(3200), "SPD: tCK": known(10)})
        frame = FrameBuilder().build(Snapshot((disk, cpu, ram)))
        fields = {d.id: d.fields for d in frame.snapshot.devices}
        self.assertNotIn("smart", fields["disk"])
        self.assertNotIn("pnp_id", fields["disk"])
        self.assertNotIn("cpuid_flags", fields["cpu"])
        self.assertNotIn("SPD: tCK", fields["ram"])
        self.assertEqual(fields["ram"]["nominal_speed"].value, 3200)
        self.assertNotIn("configured_speed", fields["ram"])
        self.assertEqual(fields["disk"]["health_status"].value, "Good")
        self.assertEqual(fields["disk"]["host_writes"].value, 120)
        self.assertLess(len(frame.details[1]), 13)
        self.assertLess(len(frame.details[2]), 10)

    def test_overall_cpu_values_replace_individual_threads(self):
        now = datetime.now(timezone.utc)
        device = Device("cpu", "sensor_cpu", "CPU", {})
        def reading(id, name, value, unit):
            return Reading(id, "cpu", name, value, unit, "test", now)
        readings = (reading("thread1", "CPU Core #1 Thread #1", 10, "%"), reading("total", "CPU Total", 40, "%"),
                    reading("core-temp", "CPU Core #1", 45, "°C"), reading("package", "CPU Package", 50, "°C"),
                    reading("clk1", "CPU Core #1", 3000, "MHz"), reading("clk2", "CPU Core #2", 4000, "MHz"))
        frame = FrameBuilder().build(Snapshot((device,), readings))
        ids = {r.id for r in frame.snapshot.readings}
        self.assertNotIn("thread1", ids)
        self.assertNotIn("core-temp", ids)
        self.assertIn("total", ids)
        self.assertIn("package", ids)
        self.assertEqual(next(r.value for r in frame.snapshot.readings if r.id.endswith("average_clock")), 3500)

    def test_mailbox_keeps_only_newest_frame(self):
        mailbox = LatestFrame()
        for value in range(100):
            mailbox.publish(value)
        self.assertEqual(mailbox.take(), 99)
        self.assertIsNone(mailbox.take())


if __name__ == "__main__":
    unittest.main()
