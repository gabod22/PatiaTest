from PySide6.QtCore import Signal, QObject
import psutil
from modules.helpers import secs2hours
from time import sleep
from modules.helpers import open_program
from modules.constants import config


from datetime import datetime

TOTAL_CPU = psutil.cpu_count(logical=True)
PERCENT = 100
DEFAULT_TIME = 60
DEFAULT_MINUTES_TIME_TEST = config['BATTERY_TEST']['DEFAULT_TIME_TO_TEST']
PATH_TO_BATTERY_LOG = "c:/battery_test.txt"
WAIT_TIME = 1 #Seconds

MIN_PERCENT_TO_STOP = 10 # (%)

class BatteryTest(QObject):

    fullChargedRemainingTimeSginal = Signal(str)
    playSoundSignal = Signal(str)
    timeElapsedSignal = Signal(str)
    batterySignal = Signal(str, str)
    errorSignal = Signal(str)
    finishedSignal = Signal()
    resultDialogTestSignal = Signal(str,str)

    def __init__(self, parent=None, time_to_test = DEFAULT_MINUTES_TIME_TEST):
        super().__init__(parent)
        self._stopped = False
        self.WRITE_TIME = 60  # seconds
        self.HOURS_CONVERSION_CONSTANT = 3600 / WAIT_TIME
        self.seconds_elapsed = 0
        self.seconds_left = time_to_test * 60
        self.battery_percent_accepted = config['BATTERY_TEST']['MINIMUM_LEFTOVER']
        self.time_to_test = time_to_test
        
    def exhaustive(self):
        self.write_start_line_to_txt('INTENSIVA')
        
        while not self._stopped:
            battery = psutil.sensors_battery()
            if battery == None :
                self._stopped = True
                self.finishedSignal.emit()
            
            self.timeElapsed.emit(secs2hours(self.seconds_elapsed))
            print(secs2hours(self.seconds_elapsed))
            sleep(WAIT_TIME)

            d, r = divmod(self.seconds_elapsed, self.WRITE_TIME)
            if r == 0:
                self.batterySignal.emit(str(battery.percent), str(battery.power_plugged))
                self.saveToTxt(battery)
                    
            if battery.percent < self.MIN_PERCENT:
                self._stopped = True
                self.finishedSignal.emit()

            self.seconds_elapsed += 1

    def bytime(self):
        # Se escribe la primera linea del test
        self.write_start_line_to_txt('POR TIEMPO')
        

        while not self._stopped and self.seconds_left > 0:
            battery = psutil.sensors_battery()
            if battery == None :
                self._stopped = True
            if (
                battery.percent <= self.battery_percent_accepted
                and self.seconds_left > 0
            ):
                self.playSoundSignal.emit("fail")
                sleep(5)
                self.errorSignal.emit(
                    "No alcanzó el rendimiento minimo deseado de {0} horas y con un remanente minimo de {1}%".format(secs2hours(self.time_to_test), str(self.battery_percent_accepted)),
                )
                self._stopped = True
                self.finishedSignal.emit()
                
            self.timeElapsedSignal.emit(secs2hours(self.seconds_left))
            print(secs2hours(self.seconds_left))
            
            sleep(WAIT_TIME)

            d, r = divmod(self.seconds_left, self.WRITE_TIME)
            if r == 0:
                self.batterySignal.emit(str(battery.percent), str(battery.power_plugged))
                self.saveToTxt(battery)

            self.seconds_left -= 1

        if self._stopped == False:
            self.finishedSignal.emit()
            self.playSoundSignal.emit("success")
            self.resultDialogTestSignal.emit("success",
                "La prueba fue exitosa, duró más de {0} horas y tuvo un remanente de {1}%".format(secs2hours(self.time_to_test), str(battery.percent))
            )

    def intensive(self):
        open_program('power_max.exe')
        self.intensive()
        
    
    def stop(self):
        self.finishedSignal.emit()
        self._stopped = True
    
    
    def write_start_line_to_txt(self, type_of_test):
        """Escribe la primera linea del registro del test de la batería,
        incluye la fecha y el tipo de prueba
        
        Args:
            type_of_test (str): Es un texto que indica el tipo de prueba realizada
        """
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        try:
            with open(PATH_TO_BATTERY_LOG, "a") as f:
                f.write("Inicio de prueba de batería {0} el {1}".format(type_of_test, date_time) )
                f.write("\n")
                f.close()
        except Exception as e:
            print("No se pudo guardar", e)
    
    def write_final_line_to_txt(self, type_of_test):
        """Escribe la línea final del test, indica el tiempo que duró la prueba y el tipo de test realizado

        Args:
            type_of_test (str): Es un texto que indica el tipo de prueba realizada
        """
        try:
            with open(PATH_TO_BATTERY_LOG, "a") as f:
                f.write(
                    "El equipo duró {0}".format(
                        secs2hours(self.seconds_elapsed)
                    )
                )
                f.write("\n")
                f.write("Fin de prueba {}".format(type_of_test))
                f.write("\n")
                f.close()
                
        except Exception as e:
            print("No se pudo guardar", e)
    
    
    def write_to_txt(self, battery):
        """Escribe en un archvo de texto, una linea con el estado de la batería,
        que incluye el tiempo de prueba, el estatus del cargador y el porcentaje de la batería
        """
        try:
            with open(PATH_TO_BATTERY_LOG, "a") as f:
                f.write(secs2hours(self.seconds_left))
                f.write("\t")
                f.write("Cargando" if battery.power_plugged else "Deconectado")
                f.write("\t")
                f.write(str(battery.percent))
                f.write("\n")
                f.close()
        except Exception as e:
            print("No se pudo guardar", e)