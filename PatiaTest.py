# -*- coding: latin-1 -*-

from chunk import Chunk
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtCore import QThreadPool, QThread, QTimer, QSize,QEvent
from PySide6.QtGui import QCloseEvent, QIcon, QPixmap
from PIL.ImageQt import ImageQt
from ui.mainwindow_ui import Ui_MainWindow
from os import path

from datetime import datetime

from Jobs.worker import Worker

from time import sleep

# from dialogs.SuccessDialog import CustomDialog
from Jobs.Battery import BatteryTest

from Jobs.Monitor import Monitor
from Jobs.CameraCapture import CameraCapture
from config_dialog import ConfigDialog

from dialogs import showFailDialog, showSuccessDialog

from function import *
from modules.files_managment import *
from modules.powerManager import (
    set_configuration_to_current_scheme,
    set_brightness,
    set_default_configuration,
    set_showroom_configuration
)
from modules.constants import config_file, dirname


import pyaudio
import wave
from loading_dialog import LoadingDialog

extDataDir = os.getcwd()
if getattr(sys, "frozen", False):
    extDataDir = sys._MEIPASS


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """
            Dialogos iniciales
        """
        self.config_dialog = None
        self.loading_dialog = None

        """
            Agrega el icono a la ventana
        """
        icon = QIcon()
        icon.addFile(
            os.path.join(dirname, "assets/logo_min.ico"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.setWindowIcon(icon)

        """
            Crea una instancia de los Threads que se utilizan
        """
        self.__thread_monitor = QThread()
        self.__thread_battery = QThread()
        self.__thread_CameraCapture = QThread()

        """
            Configuración inicial de la captura de video
        """
        self.current_camera = 0
        self.video_size = QSize(320, 240)
        self.ui.CameraLabel.setFixedSize(self.video_size)
        self.ui.BtnStopCameraCapture.setVisible(False)
        
        self.ui.BtnSwitchCamera.setVisible(False)

        self.config = read_yaml(config_file)

        # initial state
        self.configData = {}
        self.systeminfo = None
        self.threadpool = QThreadPool()
        self.ui.BtnStopTestSpeakers.hide()
        self.ui.tabBatteryTest.setEnabled(False)

        self.asing_menu_buttons_functions()
        self.asing_all_buttons_functions()

        qim = ImageQt(path.join(dirname + "/assets/no_camera.jpg"))
        self.pix = QPixmap.fromImage(qim)
        self.ui.CameraLabel.setPixmap(self.pix)
        self.start_loading_dialog()
        self.start_monitor_thread()
        set_showroom_configuration()
        set_brightness("100")

    def start_loading_dialog(self):
        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.show()

    def asing_all_buttons_functions(self):
        self.ui.BtnOpenPrograms.clicked.connect(lambda: self.open_all_tests())
        self.ui.BtnTestSpeakers.clicked.connect(lambda: self.playSound())
        self.ui.BtnStopTestSpeakers.clicked.connect(lambda: self.stopSound())
        
        self.ui.BtnTestKeyboard.clicked.connect(
            lambda: open_program("keyboard_test.exe")
        )
        self.ui.BtnTestScreen.clicked.connect(lambda: open_program("DPT.exe"))
        self.ui.BtnTestTouchscreen.clicked.connect(
            lambda: open_program("touch_test.exe")
        )
        self.ui.BtnTestCamera.clicked.connect(
            lambda: run_powershell_command("start microsoft.windows.camera:")
        )

        self.ui.BtnStopCameraCapture.clicked.connect(self.stop_feed)
        self.ui.BtnStartCameraCapture.clicked.connect(self.start_feed)
        self.ui.BtnSwitchCamera.clicked.connect(self.switch_camera)
        self.ui.BtnTestMicrophone.clicked.connect(open_record_config)
        self.ui.BtnRecordAudio.clicked.connect(self.thread_record_audio)
        self.ui.BtnPlayAudio.clicked.connect(self.play_recorded_audio)
        self.ui.BtnStopAudio.clicked.connect(self.stop_recorded_audio)
        
        self.ui.CbxBetteryTestType.currentTextChanged.connect(self.on_battery_test_mode_change)

    def on_battery_test_mode_change(self):
        if self.ui.CbxBetteryTestType.currentText() != "Por tiempo":
            self.ui.lbMinutestime.hide()
            self.ui.SpinTimeToTest.hide()
        else:
            self.ui.SpinTimeToTest.show()
            self.ui.lbMinutestime.hide()
    
    def asing_menu_buttons_functions(self):
        # Config Menu
        self.ui.actionConfig.triggered.connect(lambda: self.open_config_dialog())
        self.ui.actionSave.triggered.connect(
            lambda: self.start_thread_save_inspection()
        )
        self.ui.actionSaveLocal.triggered.connect(lambda: self.save_local())
        self.ui.actionReconectar_servidor.triggered.connect(
            lambda: self.start_loading_dialog()
        )

        self.ui.BtnStartBatteryTest.clicked.connect(
            lambda: self.open_battery_test_mode()
        )
        
        self.ui.BtnStopBatteryTest.clicked.connect(
            lambda: self.stop_battery_test_mode()
        )
        

    def open_config_dialog(self):
        if self.config_dialog is None:
            self.config_dialog = ConfigDialog(self)
            self.config_dialog.show()
        else:
            self.config_dialog = None
            
    def update_config(self):
        self.config = read_yaml(config_file)
        self.config_dialog = None


    # SECTION - Tests

    def playSound(self):
        play_speaker_test_sound()
        self.ui.BtnTestSpeakers.hide()
        self.ui.BtnStopTestSpeakers.show()

    def stopSound(self):
        stop_speaker_test_sound()
        self.ui.BtnTestSpeakers.show()
        self.ui.BtnStopTestSpeakers.hide()

    def open_all_tests(self):
        for program in self.config["SELECTED_PROGRAMS"]:
            open_program(program)

    # SECTION - Recod Audio

    def thread_record_audio(self):
        worker = Worker(self.record_audio)
        # worker.signals.result.connect(self.printDiksInfo)
        # worker.signals.finished.connect(self.DiskInfoDone)
        worker.signals.progress.connect(self.statusBar().showMessage)
        self.threadpool.start(worker)

    def play_recorded_audio(self):
        if path.exists(path.join(dirname, "output.wav")):
            play_recorded_audio_test()
        else:
            showFailDialog(self, "No hay ninguna grabación")

    def stop_recorded_audio(self):
        stop_recorded_audio_test()

    def record_audio(self, progress_callback, on_error, show_dialog):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        p = pyaudio.PyAudio()

        frames = []
        seconds = 5
        # progress_callback('Inicando la grabacion')
        print("inicializando la grabacion")
        self.ui.LbRecordAudio.setText("Grabando...")
        try:
            recorder = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
            )
            for i in range(0, int(RATE / CHUNK * seconds)):
                data = recorder.read(CHUNK)
                frames.append(data)

            print("Grabacion detenida")
            self.ui.LbRecordAudio.setText("")
        except Exception as e:
            print(e)
        finally:
            recorder.stop_stream()
            recorder.close()
            p.terminate()

        try:
            wf = wave.open(path.join(dirname, "output.wav"), "wb")
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(frames))
            wf.close()
        except Exception as e:
            print(e)

    # SECTION - Camera capture

    def __get_thread_camera_capure(self):
        thread = QThread()
        
        worker = CameraCapture()
        
        worker.moveToThread(thread)
        thread.worker = worker

        thread.started.connect(worker.run)

        worker.imageUpdate.connect(self.set_new_img)
        worker.onError.connect(lambda message: showFailDialog(self, message))

        worker.finished.connect(self.worker_done)
        thread.finished.connect(self.thread_done)
        

        return thread

    def start_feed(self):
        if not self.__thread_CameraCapture.isRunning():
            self.__thread_CameraCapture = self.__get_thread_camera_capure()
            self.__thread_CameraCapture.worker.setCamera(self.current_camera)
            self.ui.BtnStopCameraCapture.setVisible(True)
            self.ui.BtnStopCameraCapture.setEnabled(True)
            self.ui.BtnStartCameraCapture.setVisible(False)
            self.ui.BtnStartCameraCapture.setEnabled(False)
            self.__thread_CameraCapture.start()

    def stop_feed(self):
        if self.__thread_CameraCapture.isRunning():
            self.ui.BtnStopCameraCapture.setEnabled(False)
            self.__thread_CameraCapture.worker.running = False
            print("feed was asked to stop")

    def worker_done(self):
        print("worker finished")
        self.__thread_CameraCapture.quit()

    def thread_done(self):
        print("thread finished")
        self.ui.BtnStopCameraCapture.setVisible(False)
        self.ui.BtnStopCameraCapture.setEnabled(False)
        self.ui.BtnStartCameraCapture.setVisible(True)
        self.ui.BtnStartCameraCapture.setEnabled(True)
        self.ui.CameraLabel.setPixmap(self.pix)
        
    def set_new_img(self, Image):
        self.ui.CameraLabel.setPixmap(QPixmap.fromImage(Image))
        
    def switch_camera(self):
        
        self.current_camera += 1
        if self.current_camera >= len(self.systeminfo['cameras']):
            self.current_camera = 0
            
        print(self.current_camera)
        

    # SECTION - Battery Test Thread

    def __get_thread_battery_test(self):
        minutes = self.ui.SpinTimeToTest.value()
                
        thread = QThread()
        worker = BatteryTest(time_to_test=minutes)
        worker.moveToThread(thread)
        
        
        
        thread.worker = worker
        if self.ui.CbxBetteryTestType.currentText() == "Por tiempo":
            thread.started.connect(worker.bytime)
        elif self.ui.CbxBetteryTestType.currentText() == "Intensiva":
            thread.started.connect(worker.intensive)
        elif self.ui.CbxBetteryTestType.currentText() == "Exaustiva":
            thread.started.connect(worker.exausitive)
            
        # this is essential when worker is in local scope!
        
        
        worker.timeElapsed.connect(self.set_time_elapsed)
        worker.battery.connect(self.add_entry_to_battey_log)
        worker.error.connect(lambda message: showFailDialog(self, message))
        worker.aproved.connect(lambda message: showSuccessDialog(self, message))
        worker.sound.connect(lambda x: play_lologro_sound() if x == 'success' else play_cansado_sound())
        worker.finished.connect(lambda: self.end_battery_test())

        return thread
    
    def end_battery_test(self):
        print('Fin de prueba de batería')
        self.ui.BtnStartBatteryTest.setEnabled(True)
        self.ui.BtnStopBatteryTest.setEnabled(False)

    def add_entry_to_battey_log(self, percent, plugged):
        timestamp = str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        rowPosition = self.ui.TableBatteryLog.rowCount()
        self.ui.TableBatteryLog.insertRow(rowPosition)
        self.ui.TableBatteryLog.setItem(
            rowPosition, 0, QTableWidgetItem(str(timestamp))
        )
        self.ui.TableBatteryLog.setItem(
            rowPosition, 1, QTableWidgetItem(str(percent) + "%")
        )
        self.ui.TableBatteryLog.setItem(rowPosition, 2, QTableWidgetItem(str(plugged)))
        self.ui.TableBatteryLog.setItem(
            rowPosition, 3, QTableWidgetItem(str(self.ui.BarCPUPercentage.value()))
        )
        # print(str(timestamp), str(percent), str(plugged))

    def open_battery_test_mode(self):
        # open_program("power_max.exe")
        set_configuration_to_current_scheme()
        set_brightness("100")
        self.ui.BtnStopBatteryTest.setEnabled(True)
        self.ui.BtnStartBatteryTest.setEnabled(False)
        if not self.__thread_battery.isRunning():
            self.__thread_battery = self.__get_thread_battery_test()
            self.__thread_battery.start()

    def stop_battery_test_mode(self):
        self.ui.BtnStopBatteryTest.setEnabled(False)
        self.ui.BtnStartBatteryTest.setEnabled(True)
        # set_brightness("50")
        # if self.ui.ChkRestoreEnergyConfig.isChecked():
        #     set_default_configuration()
        # kill_process_by_name("power_max.exe")
        set_showroom_configuration()
        if self.__thread_battery.isRunning():
            self.__thread_battery.worker.stop()
            self.__thread_battery.quit()

    def set_time_elapsed(self, time):
        self.ui.LBTimeElapsed.setText(time)
        

    # SECTION Monitor Thread

    def __get_thread_monitor(self):
        thread = QThread()
        worker = Monitor()
        worker.moveToThread(thread)

        # this is essential when worker is in local scope!
        thread.worker = worker

        thread.started.connect(worker.run)
        worker.finished.connect(lambda: thread.quit())

        worker.cpuPercent.connect(self.ui.BarCPUPercentage.setValue)
        worker.cpuPercent.connect(self.ui.BarCPUPercentage_2.setValue)
        worker.ramPercent.connect(self.ui.BarRAMPercentage.setValue)
        worker.batteryPercent.connect(self.ui.BarBatteryPercentage_2.setValue)
        worker.batteryPercent.connect(self.ui.BarBatteryPercentage.setValue)
        worker.batteryStatus.connect(self.ui.LbBatteryStatus.setText)
        worker.batteryPlugged.connect(self.ui.LbPluggedIn.setText)
        worker.batteryRemainTime.connect(self.ui.LbBatteryRemain.setText)

        return thread

    def start_monitor_thread(self):
        if not self.__thread_monitor.isRunning():
            self.__thread_monitor = self.__get_thread_monitor()
            self.__thread_monitor.start()

    def stop_monitor_thread(self):
        if self.__thread_monitor.isRunning():
            self.__thread_monitor.worker.stop()
            self.__thread_monitor.quit()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.hide()
        if self.__thread_battery.isRunning():
            self.stop_battery_test_mode()
        self.stop_monitor_thread()
        self.stop_feed()
        set_showroom_configuration()

        """ Elimina los archivos creados
        """

        if path.exists(path.join(dirname, "output.wav")):
            os.remove(path.join(dirname, "output.wav"))
        if path.exists(path.join(dirname, "battery.csv")):
            os.remove(path.join(dirname, "battery.csv"))
        if path.exists(path.join(dirname, "programs/gpuz.xml")):
            os.remove(path.join(dirname, "programs/gpuz.xml"))
        sleep(2)


if __name__ == "__main__":
    # freeze_support()
    app = QApplication(sys.argv)

    mainwindow = MainWindow()

    sys.exit(app.exec())
