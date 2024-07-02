from PySide6.QtCore import Signal, QObject
import psutil
from modules.helpers import secs2hours
from time import sleep
from function import play_lologro_sound, play_cansado_sound

from datetime import datetime

DEFAULT_TIME = 60
TOTAL_CPU = psutil.cpu_count(logical=True)
PERCENT = 100
DEFAULT_MINUTES_TIME_TEST = 120


class BatteryTest(QObject):

    full_charged_remaining_time = Signal(str)
    sound = Signal(str)
    timeElapsed = Signal(str)
    battery = Signal(str, str)
    error = Signal(str)
    finished = Signal()
    aproved = Signal(str)

    def __init__(self, parent=None, time_to_test = DEFAULT_MINUTES_TIME_TEST):
        super().__init__(parent)
        self._stopped = False
        self.WAIT_TIME = 1  # seconds
        self.WRITE_TIME = 60  # seconds
        self.MIN_PERCENT = 10
        self.HOURS_CONVERSION_CONSTANT = 3600 / self.WAIT_TIME
        self.seconds_elapsed = 0
        self.seconds_left = time_to_test * 60
        self.battery_percet_accepted = 30
        self.time_to_test = time_to_test
        
    def intensive(self):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        try:
            with open("c:/battery_test.txt", "a") as f:
                f.write("Inicio de prueba de batería INTENSIVA el " + date_time)
                f.write("\n")
                f.close()
        except Exception as e:
            print("No se pudo guardar", e)

        while not self._stopped:
            battery = psutil.sensors_battery()
            if battery == None :
                self._stopped = True
            
            self.timeElapsed.emit(secs2hours(self.seconds_elapsed))
            print(secs2hours(self.seconds_elapsed))
            sleep(self.WAIT_TIME)

            d, r = divmod(self.seconds_elapsed, self.WRITE_TIME)
            if r == 0:
                self.battery.emit(str(battery.percent), str(battery.power_plugged))
                try:
                    with open("c:/battery_test.txt", "a") as f:
                        f.write(secs2hours(self.seconds_elapsed))
                        f.write("\t")
                        f.write("Cargando" if battery.power_plugged else "Deconectado")
                        f.write("\t")
                        f.write(str(battery.percent))
                        f.write("\n")
                        f.close()
                except Exception as e:
                    print("No se pudo guardar", e)
                    
            if battery.percent < self.MIN_PERCENT:
                self._stopped = True

            self.seconds_elapsed += 1

        try:
            with open("c:/battery_test.txt", "a") as f:

                f.write(
                    "El equipo duró {}".format(
                        secs2hours(self.seconds_elapsed)
                    )
                )
                f.write("\n")
                f.write("Fin de prueba INTENSIVA")
                f.write("\n")
                f.close()
        except Exception as e:
            print("No se pudo guardar", e)
        
    def bytime(self):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        try:
            with open("c:/battery_test.txt", "a") as f:
                f.write("Inicio de prueba de batería POR TIEMPO el " + date_time)
                f.write("\n")
                f.close()
        except Exception as e:
            print("No se pudo guardar", e)

        while not self._stopped and self.seconds_left > 0:
            battery = psutil.sensors_battery()
            if battery == None :
                self._stopped = True
            if (
                battery.percent <= self.battery_percet_accepted
                and self.seconds_left > 0
            ):
                self.sound.emit("fail")
                sleep(5)
                self.error.emit(
                    "No alcanzó el rendimiento minimo deseado de 2:00 horas y con un remanente minimo de 30%",
                )
                self._stopped = True
            self.timeElapsed.emit(secs2hours(self.seconds_left))
            print(secs2hours(self.seconds_left))
            sleep(self.WAIT_TIME)

            d, r = divmod(self.seconds_left, self.WRITE_TIME)
            if r == 0:
                self.battery.emit(str(battery.percent), str(battery.power_plugged))
                try:
                    with open("c:/battery_test.txt", "a") as f:
                        f.write(secs2hours(self.seconds_left))
                        f.write("\t")
                        f.write("Cargando" if battery.power_plugged else "Deconectado")
                        f.write("\t")
                        f.write(str(battery.percent))
                        f.write("\n")
                        f.close()
                except Exception as e:
                    print("No se pudo guardar", e)

            self.seconds_left -= 1

        if self._stopped == False:
            self.sound.emit("success")
            self.aproved.emit(
                "La prueba fue exitosa, duró más de 2 horas y tuvo un remanente de "
                + str(battery.percent)
                + "%"
            )

        try:
            with open("c:/battery_test.txt", "a") as f:

                f.write(
                    "El equipo duró {} y con un remanente de {}%".format(
                        secs2hours(self.seconds_elapsed), battery.percent
                    )
                )
                f.write("\n")
                f.write("Fin de prueba")
                f.write("\n")
                f.close()
        except Exception as e:
            print("No se pudo guardar", e)

    
    
    def stop(self):
        self.finished.emit()
        self._stopped = True
