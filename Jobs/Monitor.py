from PySide6.QtCore import Signal, QObject
from modules.battery import get_battery_info
from modules.helpers import secs2hours
import psutil


class Monitor(QObject):
    cpuPercent = Signal(int)
    ramPercent = Signal(int)
    gpuPercent = Signal(int)
    batPercent = Signal(int)
    batStatus = Signal(str)
    batPlugged = Signal(str)
    batRemainTime = Signal(str)
    batHealth = Signal(str)
    finished = Signal()

    def run(self):
        print('Monitor iniciado')
        self._stopped = False
        batt_info = get_battery_info()
        if(batt_info[0]["Voltage"] != ""):
            self.batHealth.emit(batt_info[0]["Battery Health"])
        else:
            self.batHealth.emit("Sin bateria")
        while not self._stopped:
            cpu = int(psutil.cpu_percent(interval=0.5))
            ram = int(psutil.virtual_memory().percent)
            batt = psutil.sensors_battery()
            if batt == None:
                bat_percent = "Desconocido"
                bat_status = "Batería no instalada"
                bat_plugged = "Conectada"
                bat_remaining_time = "Indeterminado"
            else:
                bat_percent = round(batt.percent, 2)
                bat_status = ("Cargando" if batt.percent <
                              100 else "Cargada al máximo")
                bat_plugged = (
                    "Conectada" if batt.power_plugged else "Desconectada")
                bat_remaining_time = secs2hours(batt.secsleft)

            self.cpuPercent.emit(cpu)
            self.ramPercent.emit(ram)
            self.batPercent.emit(bat_percent)
            self.batStatus.emit(bat_status)
            self.batPlugged.emit(bat_plugged)
            self.batRemainTime.emit(bat_remaining_time)
        self.finished.emit()

    def stop(self):
        self._stopped = True
