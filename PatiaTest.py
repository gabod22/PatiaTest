import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtCore import QThreadPool, QThread, QTimer, QSize
from PySide6.QtGui import QCloseEvent, QIcon, QPixmap
from PIL.ImageQt import ImageQt
from ui.mainwindow_ui import Ui_MainWindow
from os import path

from functools import partial
from datetime import datetime

from time import sleep

# from dialogs.SuccessDialog import CustomDialog
from Jobs.Battery import BatteryTest

from Jobs.Monitor import Monitor
from Jobs.CameraCapture import CameraCapture
from config_dialog import ConfigDialog

from Dialogs import showFailDialog

from modules.gspread import *
from function import *
from modules.battery import is_battery_installed
from modules.files_managment import *
from modules.powerManager import set_configuration_to_current_scheme, set_brightness, set_default_configuration
from modules.battery import get_battery_info
from modules.constants import config_file, dirname

from modules.programs import get_all_programs

from loading_dialog import LoadingDialog


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__thread_monitor = QThread()
        self.__thread_battery = QThread()
        self.__thread_CameraCapture = QThread()
        self.video_size = QSize(320, 240)
        self.ui.CameraLabel.setFixedSize(self.video_size)
        self.data = [[]]
        self.notes = []
        self.config_dialog = None
        self.wks = None
        self.config = read_yaml(config_file)
        self.configData = {}
        self.loading_dialog = None
        self.systeminfo = None
        battery_health = ""
        self.start_loading_dialog()
        self.ui.tabReport.setEnabled(False)

        self.threadpool = QThreadPool()

        print("Bateria instalada" if is_battery_installed() else "Sin bateria")
        if is_battery_installed():
            self.ui.BtnStartBatteryTest.setEnabled(True)

        # MenuBar
        for program in get_all_programs():
            pixmap = QPixmap(program['icon'])
            icon = QIcon(pixmap)
            self.ui.menuTools.addAction(
                icon, program["name"], partial(open_program, program["name"]))

        # initial state
        self.ui.BtnStopTestSpeakers.hide()

        self.asingMenuButtonsFunctions()
        self.asingAllButtonsFunctions()
        # self.update_config()
        self.setAllInitialValues()

        batteries = get_battery_info()
        for idx, battery in enumerate(batteries):
            self.ui.TableBatteryInfo.setItem(0, idx, QTableWidgetItem(
                str(battery["Battery Name"])))
            self.ui.TableBatteryInfo.setItem(1, idx, QTableWidgetItem(
                str(battery["Manufacture Name"])))
            self.ui.TableBatteryInfo.setItem(2, idx, QTableWidgetItem(
                str(battery["Manufacture Date"])))
            self.ui.TableBatteryInfo.setItem(3, idx, QTableWidgetItem(
                str(battery["Serial Number"])))
            self.ui.TableBatteryInfo.setItem(4, idx, QTableWidgetItem(
                str(battery["Full Charged Capacity"])))
            self.ui.TableBatteryInfo.setItem(5, idx, QTableWidgetItem(
                str(battery["Designed Capacity"])))
            self.ui.TableBatteryInfo.setItem(6, idx, QTableWidgetItem(
                str(battery["Battery Health"])))
            self.ui.TableBatteryInfo.setItem(7, idx, QTableWidgetItem(
                str(battery["Number of charge/discharge cycles"])))

            if (batteries[idx]["Voltage"] != ""):
                if idx != len(batteries) - 1:
                    battery_health = battery_health + \
                        batteries[idx]["Battery Health"] + ", "
                else:
                    battery_health = battery_health + \
                        batteries[idx]["Battery Health"]
            else:
                battery_health = "Sin bateria"

        self.ui.TextBatteryHealth.setText(battery_health)
        self.ui.TextBatteryHealth_2.setText(battery_health)

        self.start_monitor_thread()

        self.ui.BtnStartBatteryTest.clicked.connect(
            lambda: self.open_battery_test_mode())
        self.ui.BtnStopBatteryTest.clicked.connect(
            lambda: self.stop_battery_test_mode())
        self.ui.BtnSaveToGoogleSheets.clicked.connect(
            lambda: self.start_thread_save_inspection())

        qim = ImageQt(path.join(dirname + "/assets/no_camera.jpg"))
        self.pix = QPixmap.fromImage(qim)
        self.ui.CameraLabel.setPixmap(self.pix)

    def start_loading_dialog(self):
        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.show()

    def asingMenuButtonsFunctions(self):
        # Config Menu
        self.ui.actionConfig.triggered.connect(
            lambda: self.open_config_dialog())
        self.ui.actionSave.triggered.connect(
            lambda: self.start_thread_save_inspection())
        self.ui.actionSaveLocal.triggered.connect(lambda: self.save_local())
        self.ui.actionReconectar_servidor.triggered.connect(
            lambda: self.start_loading_dialog())

    def save_local(self):
        info = {}
        info['PIXELID'] = self.ui.TextPixelId.text()
        info['AESTHETIC'] = self.ui.CboxAesthetics.currentIndex()
        info['BATTERY'] = self.ui.CboxBattery.currentIndex()
        info['ETHERNET'] = self.ui.CboxEthernet.currentIndex()
        info['SUPPLY_PLUG'] = self.ui.CboxPlug.currentIndex()
        info['USB'] = self.ui.CboxUSB.currentIndex()
        info['SCREEN'] = self.ui.CboxScreen.currentIndex()
        info['SPICKERS'] = self.ui.CboxSpikers.currentIndex()
        info['KEYBOARD'] = self.ui.CboxKeyboard.currentIndex()
        info['CAMERA'] = self.ui.CboxCamera.currentIndex()
        info['CONNECTIVITY'] = self.ui.CboxConnectivity.currentIndex()
        info['MICROPHONE'] = self.ui.CboxMicro.currentIndex()
        info['TOUCHPAD'] = self.ui.CboxTouchpad.currentIndex()
        info['TOUCHSCREEN'] = self.ui.CboxTouchscreen.currentIndex()
        info['HINGES'] = self.ui.CboxHinges.currentIndex()

        info['BATTERY_DURATION'] = self.ui.TextBatteryDuration.text()
        info['BATTERY_NOTE'] = self.ui.TextBatteryNote.text()
        info['ETHERNET_NOTE'] = self.ui.TextEthernetNote.text()
        info['SUPPLY_PLUG_NOTE'] = self.ui.TextPlugNote.text()
        info['USB_NOTE'] = self.ui.TextUSBNote.text()
        info['SCREEN_NOTE'] = self.ui.TextScreenNote.text()
        info['SPICKERS_NOTE'] = self.ui.TextSpikersNote.text()
        info['KEYBOARD_NOTE'] = self.ui.TextKeyboardNote.text()
        info['CAMERA_NOTE'] = self.ui.TextCameraNote.text()
        info['CONNECTIVITY_NOTE'] = self.ui.TextCameraNote.text()
        info['MICROPHONE_NOTE'] = self.ui.TextMicroNote.text()
        info['TOUCHPAD_NOTE'] = self.ui.TextTouchpadNote.text()
        info['TOUCHSCREEN_NOTE'] = self.ui.TextTouchscreenNote.text()
        info['HINGES_NOTE'] = self.ui.TextHingesNote.text()
        info['DETAILS'] = self.ui.PlainTextDetails.toPlainText()
        # print(info)
        write_yaml("c:/patiatest_info.yaml", info)

    def setAllInitialValues(self):
        try:
            dataSaved = read_yaml("c:/patiatest_info.yaml")
            self.ui.TextPixelId.setText(dataSaved['PIXELID'])
            self.ui.CboxAesthetics.setCurrentIndex(dataSaved['AESTHETIC'])
            self.ui.CboxEthernet.setCurrentIndex(dataSaved['BATTERY'])
            self.ui.CboxEthernet.setCurrentIndex(dataSaved['ETHERNET'])
            self.ui.CboxPlug.setCurrentIndex(dataSaved['SUPPLY_PLUG'])
            self.ui.CboxUSB.setCurrentIndex(dataSaved['USB'])
            self.ui.CboxScreen.setCurrentIndex(dataSaved['SCREEN'])
            self.ui.CboxSpikers.setCurrentIndex(dataSaved['SPICKERS'])
            self.ui.CboxKeyboard.setCurrentIndex(dataSaved['KEYBOARD'])
            self.ui.CboxCamera.setCurrentIndex(dataSaved['CAMERA'])
            self.ui.CboxMicro.setCurrentIndex(dataSaved['MICROPHONE'])
            self.ui.CboxConnectivity.setCurrentIndex(dataSaved['CONNECTIVITY'])
            self.ui.CboxTouchpad.setCurrentIndex(dataSaved['TOUCHPAD'])
            self.ui.CboxTouchscreen.setCurrentIndex(dataSaved['TOUCHSCREEN'])
            self.ui.CboxHinges.setCurrentIndex(dataSaved['HINGES'])

            self.ui.TextBatteryNote.setText(dataSaved['BATTERY_NOTE'])
            self.ui.TextBatteryDuration.setText(dataSaved['BATTERY_DURATION'])
            self.ui.TextEthernetNote.setText(dataSaved['ETHERNET_NOTE'])
            self.ui.TextPlugNote.setText(dataSaved['SUPPLY_PLUG_NOTE'])
            self.ui.TextUSBNote.setText(dataSaved['USB_NOTE'])
            self.ui.TextScreenNote.setText(dataSaved['SCREEN_NOTE'])
            self.ui.TextSpikersNote.setText(dataSaved['SPICKERS_NOTE'])
            self.ui.TextKeyboardNote.setText(dataSaved['KEYBOARD_NOTE'])
            self.ui.TextCameraNote.setText(dataSaved['CAMERA_NOTE'])
            self.ui.TextMicroNote.setText(dataSaved['MICROPHONE_NOTE'])
            self.ui.TextConnectivityNote.setText(dataSaved['MICROPHONE_NOTE'])
            self.ui.TextTouchpadNote.setText(dataSaved['CONNECTIVITY_NOTE'])
            self.ui.TextTouchscreenNote.setText(dataSaved['TOUCHSCREEN_NOTE'])
            self.ui.TextHingesNote.setText(dataSaved['HINGES_NOTE'])
            self.ui.PlainTextDetails.setPlainText(dataSaved['DETAILS'])

        except Exception as e:
            print("No hay archivo por defecto", e)
            self.ui.CboxEthernet.setCurrentIndex(
                self.config['DEFAULT_VALUES']['BATTERY'])
            self.ui.CboxEthernet.setCurrentIndex(
                self.config['DEFAULT_VALUES']['ETHERNET'])
            self.ui.CboxPlug.setCurrentIndex(
                self.config['DEFAULT_VALUES']['SUPPLY_PLUG'])
            self.ui.CboxUSB.setCurrentIndex(
                self.config['DEFAULT_VALUES']['USB'])
            self.ui.CboxScreen.setCurrentIndex(
                self.config['DEFAULT_VALUES']['SCREEN'])
            self.ui.CboxSpikers.setCurrentIndex(
                self.config['DEFAULT_VALUES']['SPICKERS'])
            self.ui.CboxKeyboard.setCurrentIndex(
                self.config['DEFAULT_VALUES']['KEYBOARD'])
            self.ui.CboxCamera.setCurrentIndex(
                self.config['DEFAULT_VALUES']['CAMERA'])
            self.ui.CboxMicro.setCurrentIndex(
                self.config['DEFAULT_VALUES']['MICROPHONE'])
            self.ui.CboxConnectivity.setCurrentIndex(
                self.config['DEFAULT_VALUES']['CONNECTIVITY'])
            self.ui.CboxTouchpad.setCurrentIndex(
                self.config['DEFAULT_VALUES']['TOUCHPAD'])
            self.ui.CboxTouchscreen.setCurrentIndex(
                self.config['DEFAULT_VALUES']['TOUCHSCREEN'])
            self.ui.CboxHinges.setCurrentIndex(
                self.config['DEFAULT_VALUES']['HINGES'])

    def open_config_dialog(self):
        if self.config_dialog is None:
            self.config_dialog = ConfigDialog(self)
            self.config_dialog.show()
        else:
            self.config_dialog = None

    def update_config(self):
        self.config = read_yaml(config_file)
        self.ui.CboxCheckedBy.setCurrentIndex(self.config['DEFAULT_EMPLOYEE'])
        self.config_dialog = None

    def setOptions(self):
        self.ui.CboxAesthetics.clear()
        self.ui.CboxCheckedBy.clear()
        self.ui.CboxBattery.clear()
        self.ui.CboxEthernet.clear()
        self.ui.CboxPlug.clear()
        self.ui.CboxUSB.clear()
        self.ui.CboxScreen.clear()
        self.ui.CboxSpikers.clear()
        self.ui.CboxKeyboard.clear()
        self.ui.CboxCamera.clear()
        self.ui.CboxConnectivity.clear()
        self.ui.CboxTouchpad.clear()
        self.ui.CboxTouchscreen.clear()
        self.ui.CboxHinges.clear()
        self.ui.CboxMicro.clear()
        for aesthetic in self.configData['aesthetics']:
            self.ui.CboxAesthetics.addItem(aesthetic['slug'])
        for employee in self.configData['technicians']:
            self.ui.CboxCheckedBy.addItem(employee['name'])
        for status in self.configData['component_statuses']:
            self.ui.CboxBattery.addItem(status['slug'])
            self.ui.CboxEthernet.addItem(status['slug'])
            self.ui.CboxPlug.addItem(status['slug'])
            self.ui.CboxUSB.addItem(status['slug'])
            self.ui.CboxScreen.addItem(status['slug'])
            self.ui.CboxSpikers.addItem(status['slug'])
            self.ui.CboxKeyboard.addItem(status['slug'])
            self.ui.CboxCamera.addItem(status['slug'])
            self.ui.CboxConnectivity.addItem(status['slug'])
            self.ui.CboxTouchpad.addItem(status['slug'])
            self.ui.CboxTouchscreen.addItem(status['slug'])
            self.ui.CboxHinges.addItem(status['slug'])
            self.ui.CboxMicro.addItem(status['slug'])

# SECTION - Tests
    def asingAllButtonsFunctions(self):
        self.ui.BtnOpenPrograms.clicked.connect(lambda: self.open_all_tests())
        self.ui.BtnTestSpeakers.clicked.connect(lambda: self.playSound())
        self.ui.BtnStopTestSpeakers.clicked.connect(lambda: self.stopSound())
        self.ui.BtnTestKeyboard.clicked.connect(
            lambda: open_program('keyboard_test.exe'))
        self.ui.BtnTestScreen.clicked.connect(
            lambda: open_program('DPT.exe'))
        self.ui.BtnTestTouchscreen.clicked.connect(
            lambda: open_program('touch_test.exe'))
        self.ui.BtnTestCamera.clicked.connect(
            lambda: run_powershell_command('start microsoft.windows.camera:'))

        self.ui.BtnStopCameraCapture.clicked.connect(
            self.stop_feed)
        self.ui.BtnStartCameraCapture.clicked.connect(
            self.start_feed)
        # self.ui.BtnConnectToWifi.clicked.connect(
        #     lambda: self.start_jobs_thread())
        # self.ui.BtnCmd.clicked.connect(lambda: self.executeCommand())

    def playSound(self):
        play_speaker_test_sound()
        self.ui.BtnTestSpeakers.hide()
        self.ui.BtnStopTestSpeakers.show()

    def stopSound(self):
        stop_speaker_test_sound()
        self.ui.BtnTestSpeakers.show()
        self.ui.BtnStopTestSpeakers.hide()

    def open_all_tests(self):
        for program in self.config['SELECTED_PROGRAMS']:
            open_program(program)


# SECTION - Save inspectión

    def start_thread_save_inspection(self):
        pass


# SECTION - register computer

    def start_thread_register_computer(self):
        pass

#!SECTION
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
            self.__thread_CameraCapture.running = True
            self.__thread_CameraCapture.start()

    def stop_feed(self):
        if self.__thread_CameraCapture.isRunning():

            self.__thread_CameraCapture.worker.camera.release()
            self.__thread_CameraCapture.worker.running = False
            print("feed was asked to stop")

    def worker_done(self):
        print("worker finished")
        self.__thread_CameraCapture.worker.camera.release()
        self.__thread_CameraCapture.quit()

    def thread_done(self):
        print("thread finished")
        self.ui.CameraLabel.setPixmap(self.pix)

    def set_new_img(self, Image):
        print("it received the signal")
        print(Image)
        self.ui.CameraLabel.setPixmap(QPixmap.fromImage(Image))

    # def start_camera_capture_tread(self):
    #     if not self.__thread_CameraCapture.isRunning():
    #         self.__thread_CameraCapture = self.__get_thread_camera_capure()
    #         self.__thread_CameraCapture.start()


# SECTION - Battery Test Thread


    def __get_thread_battery_test(self):
        thread = QThread()
        worker = BatteryTest()
        worker.moveToThread(thread)

        # this is essential when worker is in local scope!
        thread.worker = worker
        thread.started.connect(worker.run)
        worker.timeElapsed.connect(self.set_time_elapsed)
        worker.battery.connect(self.add_entry_to_battey_log)

        worker.finished.connect(lambda: self.end_battery_test())

        return thread

    def add_entry_to_battey_log(self, percent, plugged):
        timestamp = str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        rowPosition = self.ui.TableBatteryLog.rowCount()
        self.ui.TableBatteryLog.insertRow(rowPosition)
        self.ui.TableBatteryLog.setItem(
            rowPosition, 0, QTableWidgetItem(str(timestamp)))
        self.ui.TableBatteryLog.setItem(
            rowPosition, 1, QTableWidgetItem(str(percent)+"%"))
        self.ui.TableBatteryLog.setItem(
            rowPosition, 2, QTableWidgetItem(str(plugged)))
        self.ui.TableBatteryLog.setItem(rowPosition, 3, QTableWidgetItem(
            str(self.ui.BarCPUPercentage.value())))
        print(str(timestamp), str(percent), str(plugged))

    def open_battery_test_mode(self):
        open_program('power_max.exe')
        set_configuration_to_current_scheme()
        set_brightness('100')
        self.ui.BtnStopBatteryTest.setEnabled(True)
        self.ui.BtnStartBatteryTest.setEnabled(False)
        if not self.__thread_battery.isRunning():
            self.__thread_battery = self.__get_thread_battery_test()
            self.__thread_battery.start()

    def stop_battery_test_mode(self):
        self.ui.BtnStopBatteryTest.setEnabled(False)
        self.ui.BtnStartBatteryTest.setEnabled(True)
        set_brightness('50')
        set_default_configuration()
        kill_process_by_name('power_max.exe')
        if self.__thread_battery.isRunning():
            self.__thread_battery.worker.stop()
            self.__thread_battery.quit()

    def end_battery_test(self):
        if self.ui.ChkBoxSaveAtEnd.isChecked():
            print("Guardando despues de prueba bateria")
            self.start_thread_save_to_google_sheets()

    def set_time_elapsed(self, time):
        self.ui.LBTimeElapsed.setText(time)
        self.ui.TextBatteryDuration.setText(time)
#!SECTION

# SECTION Monitor Thread

    def __get_thread_monitor(self):
        thread = QThread()
        worker = Monitor()
        worker.moveToThread(thread)

        # this is essential when worker is in local scope!
        thread.worker = worker

        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)

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

#!SECTION

    def closeEvent(self, event: QCloseEvent) -> None:
        self.stop_battery_test_mode()
        self.stop_monitor_thread()
        sleep(1)


if __name__ == "__main__":
    freeze_support()
    app = QApplication(sys.argv)

    mainwindow = MainWindow()

    sys.exit(app.exec())
