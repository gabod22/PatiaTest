import sys
import re
import asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QThreadPool, QThread
from PySide6.QtGui import QCloseEvent, QIcon, QPixmap
from ui.mainwindow_ui import Ui_MainWindow

from functools import partial
from datetime import datetime
import pythoncom
from time import sleep

# from dialogs.SuccessDialog import CustomDialog
from Jobs.Battery import BatteryTest
from Jobs.worker import Worker
from Jobs.Monitor import Monitor
from Jobs.Jobs import Jobs

from config_dialog import ConfigDialog

from modules.systeminfo import get_system_info
from modules.helpers import convert_size
from modules.gspread import *
from function import *
from modules.battery import is_battery_installed
from modules.files_managment import *
from modules.powerManager import set_configuration_to_current_scheme, set_brightness, set_default_configuration
from modules.battery import get_battery_info
from modules.constants import config_file
from modules.constants import config
from modules.systeminfo import get_system_info
from modules.programs import get_all_programs

from modules.backend_connection import get_computer, save_computer


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__thread_monitor = QThread()
        self.__thread_battery = QThread()
        self.__thread_jobs = QThread()
        self.__thread_stress = QThread()

        self.data = [[]]
        self.notes = []
        self.config_dialog = None
        self.wks = None
        self.config = read_yaml(config_file)
        self.configData = {}

        self.systeminfo = None
        self.array_disks = get_disks_info()
        self.array_gpus = getGPUs()
        battery_health = ""

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
        self.setOptions()
        self.asingMenuButtonsFunctions()
        self.asingAllButtonsFunctions()
        self.update_config()
        self.setAllInitialValues()

        # Add all Disks to table
        self.ui.TableStorage.setRowCount(len(self.array_disks))
        add_data_to_table(self.array_disks, self.ui.TableStorage)

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

        # Add all gpus to table
        self.ui.TableGPUs.setRowCount(len(self.array_gpus))
        add_data_to_table(self.array_gpus, self.ui.TableGPUs)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" %
              self.threadpool.maxThreadCount())

        self.start_jobs_thread()
        self.start_get_system_info_thread()
        self.start_monitor_thread()

        self.ui.BtnStartBatteryTest.clicked.connect(
            lambda: self.open_battery_test_mode())
        self.ui.BtnStopBatteryTest.clicked.connect(
            lambda: self.stop_battery_test_mode())
        self.ui.BtnSaveToGoogleSheets.clicked.connect(
            lambda: self.start_thread_save_inspection())

    def asingMenuButtonsFunctions(self):
        # Config Menu
        self.ui.actionConfig.triggered.connect(
            lambda: self.open_config_dialog())
        self.ui.actionSave.triggered.connect(
            lambda: self.start_thread_save_inspection())
        self.ui.actionSaveLocal.triggered.connect(lambda: self.save_local())

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
        self.ui.CboxCheckedBy.clear()
        self.ui.CboxCheckedBy.addItems(self.config['EMPLOYEES'])
        self.ui.CboxCheckedBy.setCurrentIndex(self.config['DEFAULT_EMPLOYEE'])
        self.config_dialog = None

    def setOptions(self):
        self.ui.CboxAesthetics.addItems(config["AESTHETICS"])
        self.ui.CboxCheckedBy.addItems(config["EMPLOYEES"])
        self.ui.CboxBattery.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxEthernet.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxPlug.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxUSB.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxScreen.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxSpikers.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxKeyboard.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxCamera.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxConnectivity.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxTouchpad.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxTouchscreen.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxHinges.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxMicro.addItems(config["STATUS_OPTIONS"])

# SECTION - Tests
    def asingAllButtonsFunctions(self):
        self.ui.BtnOpenPrograms.clicked.connect(lambda: self.open_all_tests())
        self.ui.BtnTestSpeakers.clicked.connect(lambda: self.playSound())
        self.ui.BtnStopTestSpeakers.clicked.connect(lambda: self.stopSound())
        self.ui.BtnTestKeyboard.clicked.connect(
            lambda: open_program('keyboard_test.exe'))
        self.ui.BtnTestTouchscreen.clicked.connect(
            lambda: open_program('touch_test.exe'))
        self.ui.BtnTestCamera.clicked.connect(
            lambda: run_powershell_command('start microsoft.windows.camera:'))
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
# SECTION - Get system info

    def set_system_info(self, info):
        cpu_model = re.search("i\d-\d{4}[A-Z]", info["cpu"]["brand_raw"]).group()
        ram = str(convert_size(info["virtual_memory"]["total"])) + " " + info["memories"][0]["Tipo"]
        self.systeminfo = info
        self.ui.TextBiosVersion.setText(info["bios"]["Version"])
        self.ui.TextTotalRAM.setText(ram)
        self.ui.TextProcessorName.setText(cpu_model)
        self.ui.TextModel.setText(info["computer_system"]["Model"])
        self.ui.TextServiceNumber.setText(info["bios"]["SerialNumber"])

    def get_system_info_done(self):
        self.statusBar().showMessage('Información obtenida')

    def start_get_system_info_thread(self):
        # Pass the function to execute
        # Any other args, kwargs are passed to the run function
        pythoncom.CoInitialize()
        worker = Worker(get_system_info)
        worker.signals.result.connect(self.set_system_info)
        worker.signals.finished.connect(self.get_system_info_done)
        worker.signals.progress.connect(self.statusBar().showMessage)

        # Execute
        self.threadpool.start(worker)

# #SECTION - Stresss
#     def __get_thread_stress_CPU(self):
#         thread = QThread()
#         stress_cpu = StressCPU()
#         stress_cpu.moveToThread(thread)
#         thread.started.connect(stress_cpu.start_stress)
#         return thread

#     def start_stress_thread(self):
#         if not self.__thread_stress.isRunning():
#             self.__thread_stress = self.__get_thread_stress_CPU()
#             self.__thread_stress.start()

#     def stop_stress_thread(self):
#         if self.__thread_stress.isRunning():
#             self.__thread_stress.worker.stop_stress()
#             self.__thread_stress.quit()

#!SECTION
# SECTION - Save inspectión

    def start_thread_save_inspection(self):
        r = asyncio.run(get_computer(
            serial_number=self.systeminfo['bios']['SerialNumber']))
        gpu_model = ""
        gpu_ram = ""
        if (r.status == 404):
            print(r.status)
            if self.array_gpus != []:
                gpu_model = self.array_gpus[0][0]
                gpu_ram = self.array_gpus[0][1]
            else:
                gpu_model = "Sin grafica"
                gpu_ram = ""

            computer = {
                "service_tag": self.systeminfo['bios']['SerialNumber'],
                "internal_id": self.ui.TextPixelId.text(),
                "product_id": 1,
                "processor": re.search("i\d-\d{4}[A-Z]", self.systeminfo["cpu"]["brand_raw"]),
                "ram_size": str(convert_size(self.systeminfo["virtual_memory"]["total"])),
                "ram_type": self.systeminfo["memories"][0]["Tipo"],
                "storage_size": self.array_disks[0][2],
                "storage_type": self.array_disks[0][1],
                "graphics_card_model": gpu_model,
                "graphics_ram_size": gpu_ram,
                "computer_status_id": 1,
                "aesthetic_id": 1,
            }
            asyncio.run(save_computer(computer))


#!SECTION

# SECTION - Battery Test Thread


    def __get_thread_battery_test(self):
        thread = QThread()
        worker = BatteryTest()
        worker.moveToThread(thread)

        # this is essential when worker is in local scope!
        thread.worker = worker
        thread.started.connect(worker.run)
        worker.timeElapsed.connect(self.set_time_elapsed)

        worker.finished.connect(lambda: self.end_battery_test())

        return thread

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

# SECTION - Initial Jobs


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

# SECTION - Jobs Thread
    def __get_thread_jobs(self):
        thread = QThread()
        worker = Jobs()
        worker.moveToThread(thread)

        # this is essential when worker is in local scope!
        thread.worker = worker

        thread.started.connect(worker.run)
        worker.configData.connect(self.setConfigData)
        worker.finished.connect(thread.quit)
        worker.error.connect(lambda: self.showFailDialog('No hay internet'))

        return thread

    def setConfigData(self, data):
        self.configData = data
        print(self.configData)

    def start_jobs_thread(self):
        if not self.__thread_jobs.isRunning():
            self.__thread_jobs = self.__get_thread_jobs()
            self.__thread_jobs.start()

    def stop_jobs_thread(self):
        if self.__thread_jobs.isRunning():
            self.__thread_jobs.worker.stop()
            self.__thread_jobs.quit()
#!SECTION

    def closeEvent(self, event: QCloseEvent) -> None:
        self.stop_battery_test_mode()
        self.stop_monitor_thread()
        sleep(1)

        # dialogs
    def showSuccessDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle('Todo correcto')
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    def showFailDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText(message)
        msgBox.setWindowTitle('Error')
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')


if __name__ == "__main__":
    freeze_support()
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec())
