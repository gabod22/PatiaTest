from PySide6.QtCore import Signal, QObject
from modules.utils import secs2hours
import psutil
import threading


class Monitor(QObject):
    cpuPercent = Signal(object)
    ramPercent = Signal(object)
    gpuPercent = Signal(object)
    batteryPercent = Signal(object)
    batteryStatus = Signal(object)
    batteryPlugged = Signal(object)
    batteryRemainTime = Signal(object)
    finished = Signal()

    def __init__(self):
        super().__init__()
        self._stop = threading.Event()

    def run(self):
        print('Monitor iniciado')
        
        psutil.cpu_percent(interval=None)
        while not self._stop.is_set():
            cpu = int(psutil.cpu_percent(interval=None))
            ram = int(psutil.virtual_memory().percent)
            battery = psutil.sensors_battery()
            if battery == None:
                battery_percent = "Desconocido"
                battery_status = "Batería no instalada"
                battery_plugged = "No disponible"
                battery_remaining_time = "Indeterminado"
            else:
                battery_percent = round(battery.percent, 2)
                battery_status = ("Descargando" if not battery.power_plugged else
                                  "Cargando" if battery.percent < 100 else "Cargada al máximo")
                battery_plugged = (
                    "Conectada" if battery.power_plugged else "Desconectada")
                battery_remaining_time = secs2hours(battery.secsleft) if battery.secsleft >= 0 else "Indeterminado"

            self.cpuPercent.emit(cpu)
            self.ramPercent.emit(ram)
            self.batteryPercent.emit(battery_percent)
            self.batteryStatus.emit(battery_status)
            self.batteryPlugged.emit(battery_plugged)
            self.batteryRemainTime.emit(battery_remaining_time)
            self._stop.wait(1)
        self.finished.emit()

    def stop(self):
        self._stop.set()
