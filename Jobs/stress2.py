import sys
import time
import threading
from PySide6.QtCore import QObject, Slot

class StressCPU(QObject):
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.num_threads = 1
        self.stress_time = 5  # en segundos

    def set_threads(self, num_threads):
        self.num_threads = num_threads

    def set_stress_time(self, stress_time):
        self.stress_time = stress_time

    @Slot()
    def start_stress(self):
        self.is_running = True
        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self._stress_worker)
            threads.append(thread)
            thread.start()

        time.sleep(self.stress_time)
        self.is_running = False

        for thread in threads:
            thread.join()

    def _stress_worker(self):
        while self.is_running:
            # Perform a heavy computation to stress the CPU
            sum([i * i for i in range(10 ** 6)])

    @Slot()
    def stop_stress(self):
        self.is_running = False