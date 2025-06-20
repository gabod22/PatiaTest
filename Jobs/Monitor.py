from PySide6.QtCore import Signal, QObject
from modules.utils import secs2hours
import psutil


class Monitor(QObject):
    cpuPercent = Signal(int)
    ramPercent = Signal(int)
    gpuPercent = Signal(int)
    batteryPercent = Signal(int)
    batteryStatus = Signal(str)
    batteryPlugged = Signal(str)
    batteryRemainTime = Signal(str)
    finished = Signal()

    def run(self):
        print('Monitor iniciado')
        self._stopped = False
        
        while not self._stopped:
            cpu = int(psutil.cpu_percent(interval=0.5))
            ram = int(psutil.virtual_memory().percent)
            battery = psutil.sensors_battery()
            if battery == None:
                battery_percent = "Desconocido"
                battery_status = "Batería no instalada"
                battery_plugged = "Conectada"
                battery_remaining_time = "Indeterminado"
            else:
                battery_percent = round(battery.percent, 2)
                battery_status = ("Cargando" if battery.percent <
                              100 else "Cargada al máximo")
                battery_plugged = (
                    "Conectada" if battery.power_plugged else "Desconectada")
                battery_remaining_time = secs2hours(battery.secsleft)

            self.cpuPercent.emit(cpu)
            self.ramPercent.emit(ram)
            self.batteryPercent.emit(battery_percent)
            self.batteryStatus.emit(battery_status)
            self.batteryPlugged.emit(battery_plugged)
            self.batteryRemainTime.emit(battery_remaining_time)
        self.finished.emit()

    def stop(self):
        self._stopped = True
