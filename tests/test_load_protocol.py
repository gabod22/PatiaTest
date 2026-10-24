from pathlib import Path
import sys
import time
import unittest

from modules.load.client import LoadClient, LoadError


class LoadProtocolTests(unittest.TestCase):
    def client(self, mode):
        client = LoadClient([sys.executable, "-u", str(Path(__file__).with_name("fake_load_host.py")), mode])
        self.addCleanup(client.close)
        return client

    def test_persistent_process_and_owned_cleanup(self):
        client = self.client("normal")
        client.request("capabilities")
        process = client.process
        client.request("status")
        self.assertIs(client.process, process)
        client.close()
        self.assertIsNotNone(process.poll())
        self.assertIsNone(client.job)
        self.assertIsNone(client.reader)

    def test_bad_protocol_crash_and_provider_failure(self):
        for mode in ("bad_version", "bad_id", "crash", "error"):
            with self.subTest(mode=mode):
                client = self.client(mode)
                with self.assertRaises(LoadError):
                    client.request("status")
                process = client.process
                client.close()
                self.assertIsNotNone(process.poll())

    def test_timeout_can_be_closed_without_orphan(self):
        client = self.client("hang")
        start = time.monotonic()
        with self.assertRaises(LoadError):
            client.request("status")
        process = client.process
        client.close()
        self.assertLess(time.monotonic() - start, 6)
        self.assertIsNotNone(process.poll())


if __name__ == "__main__":
    unittest.main()
