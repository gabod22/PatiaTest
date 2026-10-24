"""Opt-in lifecycle checks of the real helper, without generated CPU/GPU load."""
import os
import unittest
from modules.load.client import LoadClient
from modules.load.models import LoadConfig


@unittest.skipUnless(os.environ.get("PIXELTEST_NATIVE_TESTS") == "1", "Set PIXELTEST_NATIVE_TESTS=1 after building")
class NativeLoadLifecycleTests(unittest.TestCase):
    def test_update_stop_shutdown_share_one_helper(self):
        client = LoadClient()
        self.addCleanup(client.close)
        client.request("capabilities")
        process = client.process
        client.request("start", LoadConfig(0, 0))
        client.request("update", LoadConfig(0, 0, initial_cores=1))
        status = client.request("status")
        self.assertEqual(status["active_cores"], 0)
        self.assertEqual(status["cpu_duty"], 0)
        self.assertIs(client.process, process)
        client.request("stop")
        self.assertEqual(client.request("status")["state"], "stopped")
        client.request("shutdown")
        self.assertEqual(process.wait(timeout=3), 0)

    def test_watchdog_exits_without_orphan(self):
        client = LoadClient()
        self.addCleanup(client.close)
        client.request("start", LoadConfig(0, 0))
        self.assertEqual(client.process.wait(timeout=8), 3)

    def test_job_kills_only_its_helper(self):
        client = LoadClient()
        self.addCleanup(client.close)
        cap = client.request("capabilities")
        self.assertGreater(cap["physical_cores"], 0)
        process = client.process
        client.job.Close()
        client.job = None
        self.assertIsNotNone(process.wait(timeout=3))


if __name__ == "__main__":
    unittest.main()
