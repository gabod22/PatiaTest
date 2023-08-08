from PySide6.QtCore import Signal, QObject
import psutil
from modules.helpers import secs2hours
from time import sleep

DEFAULT_TIME = 60
TOTAL_CPU = psutil.cpu_count(logical=True)
PERCENT = 100


class BatteryTest(QObject):

    full_charged_remaining_time = Signal(str)
    timeElapsed = Signal(str)
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stopped = False
        self.WAIT_TIME = 1  # seconds
        self.WRITE_TIME = 60 # seconds
        self.HOURS_CONVERSION_CONSTANT= 3600/self.WAIT_TIME
        self.seconds_elapsed = 0

    def run(self):
        try:
            with open('c:/battery_test.txt', 'a') as f:
                f.write("Inicio de prueba de batería")
                f.write("\n")
                f.close()
        except Exception as e:
            print("No se pudo guardar", e)
            
        while not self._stopped:
            battery = psutil.sensors_battery()
            if battery == None or battery.percent < 10:
                self.timeElapsed.emit(self.seconds_elapsed)
                self._stopped = True
            self.timeElapsed.emit(secs2hours(self.seconds_elapsed))
            print(secs2hours(self.seconds_elapsed))
            sleep(self.WAIT_TIME)
            
            d, r = divmod(self.seconds_elapsed, self.WRITE_TIME)
            if r == 0:
                try:
                    with open('c:/battery_test.txt', 'a') as f:
                        f.write(secs2hours(self.seconds_elapsed))
                        f.write('\t')
                        f.write(str(battery.power_plugged))
                        f.write('\t')
                        f.write(str(battery.percent))
                        f.write('\n')
                        f.close()
                except Exception as e:
                    print("No se pudo guardar", e)
            
            self.seconds_elapsed += 1
            
        try:
            with open('c:/battery_test.txt', 'a') as f:
                f.write("Fin de prueba")
                f.write('\n')
                f.close()
        except Exception as e:
            print("No se pudo guardar", e)
        

    def stop(self):
        self.finished.emit()
        self._stopped = True

    