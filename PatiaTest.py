import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThreadPool, QThread
from PySide6.QtGui import QCloseEvent, QImage, QIcon, QPixmap
from ui.mainwindow_ui import Ui_MainWindow


from multiprocessing import freeze_support
from functools import partial
from datetime import datetime
import pythoncom
from time import sleep

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
# from modules.programs import *
from modules.files_managment import *
from modules.constants import config_file
from modules.powerManager import set_configuration_to_current_scheme, set_brightness, set_default_configuration
from modules.battery import get_battery_info
from modules.wifi import connect, createNewConnection
from modules.constants import config
from modules.DiskInfoParser import DiskInfo
from modules.systeminfo import get_system_info
from modules.programs import get_all_programs


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.systeminfo = None
        self.__thread_monitor = QThread()
        self.__thread_battery = QThread()
        self.__thread_jobs = QThread()

        self.data = [[]]
        self.notes = []
        self.config_dialog = None
        self.wks = None

        self.config = read_yaml(config_file)
        array_disks = get_disks_info()
        array_gpus = getGPUs()
        # System info

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
        self.ui.TableStorage.setRowCount(len(array_disks))
        add_data_to_table(array_disks, self.ui.TableStorage)

        batteries = get_battery_info()
        for column in range(len(batteries)):
            self.ui.TableBatteryInfo.setItem(0, column, QTableWidgetItem(
                str(batteries[column]["Battery Name"])))
            self.ui.TableBatteryInfo.setItem(1, column, QTableWidgetItem(
                str(batteries[column]["Manufacture Name"])))
            self.ui.TableBatteryInfo.setItem(2, column, QTableWidgetItem(
                str(batteries[column]["Manufacture Date"])))
            self.ui.TableBatteryInfo.setItem(3, column, QTableWidgetItem(
                str(batteries[column]["Serial Number"])))
            self.ui.TableBatteryInfo.setItem(4, column, QTableWidgetItem(
                str(batteries[column]["Full Charged Capacity"])))
            self.ui.TableBatteryInfo.setItem(5, column, QTableWidgetItem(
                str(batteries[column]["Designed Capacity"])))
            self.ui.TableBatteryInfo.setItem(6, column, QTableWidgetItem(
                str(batteries[column]["Battery Health"])))
            self.ui.TableBatteryInfo.setItem(7, column, QTableWidgetItem(
                str(batteries[column]["Number of charge/discharge cycles"])))

        # Add all gpus to table
        self.ui.TableGPUs.setRowCount(len(array_gpus))
        add_data_to_table(array_gpus, self.ui.TableGPUs)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" %
              self.threadpool.maxThreadCount())

        self.start_get_system_info_thread()
        self.start_monitor_thread()

        self.ui.BtnStartBatteryTest.clicked.connect(
            lambda: self.open_battery_test_mode())
        self.ui.BtnStopBatteryTest.clicked.connect(
            lambda: self.stop_battery_test_mode())
        self.ui.BtnSaveToGoogleSheets.clicked.connect(
            lambda: self.start_thread_save_to_google_sheets())

    def asingMenuButtonsFunctions(self):
        # Config Menu
        self.ui.actionConfig.triggered.connect(
            lambda: self.open_config_dialog())
        self.ui.actionSave.triggered.connect(
            lambda: self.save_to_google_sheets())
        self.ui.actionSaveLocal.triggered.connect(lambda: self.save_local())

    def save_local(self):
        info = {}
        info['ETHERNET'] = self.ui.CboxEthernet.currentIndex()
        info['SUPPLY_PLUG'] = self.ui.CboxPlug.currentIndex()
        info['USB'] = self.ui.CboxUSB.currentIndex()
        info['SCREEN'] = self.ui.CboxScreen.currentIndex()
        info['SPICKERS'] = self.ui.CboxSpikers.currentIndex()
        info['KEYBOARD'] = self.ui.CboxKeyboard.currentIndex()
        info['CAMERA'] = self.ui.CboxCamera.currentIndex()
        info['MICROPHONE'] = self.ui.CboxMicro.currentIndex()
        info['TOUCHPAD'] = self.ui.CboxTouchpad.currentIndex()
        info['TOUCHSCREEN'] = self.ui.CboxTouchscreen.currentIndex()
        info['HINGES'] = self.ui.CboxHinges.currentIndex()
        # print(info)
        write_yaml("c:/patiatest_info.yaml", info)

    def setAllInitialValues(self):
        try:
            dataSaved = read_yaml("c:/patiatest_info.yaml")
            print(dataSaved)
            self.ui.CboxEthernet.setCurrentIndex(dataSaved['ETHERNET'])
            self.ui.CboxPlug.setCurrentIndex(dataSaved['SUPPLY_PLUG'])
            self.ui.CboxUSB.setCurrentIndex(dataSaved['USB'])
            self.ui.CboxScreen.setCurrentIndex(dataSaved['SCREEN'])
            self.ui.CboxSpikers.setCurrentIndex(dataSaved['SPICKERS'])
            self.ui.CboxKeyboard.setCurrentIndex(dataSaved['KEYBOARD'])
            self.ui.CboxCamera.setCurrentIndex(dataSaved['CAMERA'])
            self.ui.CboxMicro.setCurrentIndex(dataSaved['MICROPHONE'])
            self.ui.CboxTouchpad.setCurrentIndex(dataSaved['TOUCHPAD'])
            self.ui.CboxTouchscreen.setCurrentIndex(dataSaved['TOUCHSCREEN'])
            self.ui.CboxHinges.setCurrentIndex(dataSaved['HINGES'])

        except Exception as e:
            print(e)
            self.ui.CboxEthernet.setCurrentIndex(
                self.config['DEFAULT_VALUES']['ETHERNET'])
            self.ui.CboxPlug.setCurrentIndex(
                self.config['DEFAULT_VALUES']['SUPPLY_PLUG'])
            self.ui.CboxUSB.setCurrentIndex(self.config['DEFAULT_VALUES']['USB'])
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
        self.ui.CboxEthernet.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxPlug.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxUSB.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxScreen.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxSpikers.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxKeyboard.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxCamera.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxTouchpad.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxTouchscreen.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxHinges.addItems(config["STATUS_OPTIONS"])
        self.ui.CboxMicro.addItems(config["STATUS_OPTIONS"])

#SECTION - Tests
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
        self.systeminfo = info
        print(info['bios'])
        self.ui.TextBiosVersion.setText(info["bios"]["Version"])
        self.ui.TextRAMType.setText(info["memories"][0]["Tipo"])
        self.ui.TextTotalRAM.setText(
            str(convert_size(info["virtual_memory"]["total"])))
        self.ui.TextProcessorName.setText(info["cpu"]["brand_raw"])
        self.ui.TextModel.setText(info["computer_system"]["Model"])
        self.ui.TextServiceNumber.setText(info["bios"]["SerialNumber"])

    def get_system_info_done(self):
        self.statusBar().showMessage('Información obtenida')
        print("Info obteida")

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

#!SECTION
# SECTION - Google sheet Thread
    def start_thread_save_to_google_sheets(self):
        # Any other args, kwargs are passed to the run function
        worker = Worker(self.save_to_google_sheets)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.statusBar().showMessage)

        # Execute
        self.threadpool.start(worker)

    def save_to_google_sheets(self, progress_callback):
        self.ui.BtnSaveToGoogleSheets.setEnabled(False)
        try:
            progress_callback.emit('Obteniendo worksheet')
            wks = get_worksheet()
            print(wks)
        except Exception as e:
            progress_callback.emit('Error al obtener el worksheet')
            print(e)
            self.data = [[]]
            self.notes = []
            return

        next_row = get_already_tested_row(
            self.ui.TextServiceNumber.text(), 5, wks)
        if next_row < 0:
            next_row = next_available_row(wks)

        try:
            progress_callback.emit('Guardando...')
            write_cell(self.ui.TextPixelId.text(), "", wks, next_row, 1)
            write_cell(self.ui.TextModel.text(), "", wks, next_row, 4)
            write_cell(self.ui.TextServiceNumber.text(), "", wks, next_row, 5)
            self.data = [[]]
            self.data[0].append(self.ui.CboxCheckedBy.currentText())
            self.data[0].append(self.ui.CboxAesthetics.currentText())
            self.data[0].append(p2f(self.ui.TextBatteryHealth.text()))
            self.data[0].append(self.ui.TextBatteryNote.text())
            write_range(self.data, self.notes, wks, next_row, "G")
            self.data = [[]]
            self.data[0].append(self.ui.CboxPlug.currentText())
            self.data[0].append(self.ui.CboxEthernet.currentText())
            self.data[0].append(self.ui.CboxUSB.currentText())
            self.data[0].append(self.ui.CboxHinges.currentText())
            self.data[0].append(self.ui.CboxScreen.currentText())
            self.data[0].append(self.ui.CboxTouchscreen.currentText())
            self.data[0].append(self.ui.CboxKeyboard.currentText())
            self.data[0].append(self.ui.CboxTouchpad.currentText())
            self.data[0].append(self.ui.CboxSpikers.currentText())
            self.data[0].append(self.ui.CboxCamera.currentText())
            self.data[0].append(self.ui.CboxMicro.currentText())
            self.data[0].append(self.ui.PlainTextDetails.toPlainText())

            self.notes.append(self.ui.TextPlugNote.text())
            self.notes.append(self.ui.TextEthernetNote.text())
            self.notes.append(self.ui.TextUSBNote.text())
            self.notes.append(self.ui.TextHingesNote.text())
            self.notes.append(self.ui.TextScreenNote.text())
            self.notes.append(self.ui.TextTouchscreenNote.text())
            self.notes.append(self.ui.TextKeyboardNote.text())
            self.notes.append(self.ui.TextTouchpadNote.text())
            self.notes.append(self.ui.TextSpikersNote.text())
            self.notes.append(self.ui.TextCameraNote.text())
            self.notes.append(self.ui.TextMicroNote.text())
            
            write_range(self.data, self.notes, wks, next_row, "N")
            print("guarde todo menos la hora")
            sleep(0.1)
            write_cell(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),"",wks,next_row,26)
            print('La info fue guardada correctamente')
            progress_callback.emit('Guardado correctamente')
        except Exception as e:
            # self.showFailDialog('La información no fue guardada.')
            progress_callback.emit('Error al guardar el Google')
            print('La info no fue guardada :C %s' % e)
        finally:
            self.data = [[]]
            self.notes = []
            wks.client.session.close()

    def thread_complete(self):
        self.ui.BtnSaveToGoogleSheets.setEnabled(True)
        print("THREAD COMPLETE!")

    def print_output(self, output):
        print(output)
        # self.generateQrCode(output['computer_system']['Model'])
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

        worker.finished.connect(self.end_battery_test)

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
        self.ui.TextBatteryNote.setText(time)
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
        worker.batPercent.connect(self.ui.BarBatteryPercentage_2.setValue)
        worker.batPercent.connect(self.ui.BarBatteryPercentage.setValue)
        worker.batStatus.connect(self.ui.LbBatteryStatus.setText)
        worker.batPlugged.connect(self.ui.LbPluggedIn.setText)
        worker.batRemainTime.connect(self.ui.LbBatteryRemain.setText)
        worker.batHealth.connect(self.ui.TextBatteryHealth.setText)
        worker.batHealth.connect(self.ui.TextBatteryHealth_2.setText)

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
        worker.batteryInfo.connect()
        worker.finished.connect(thread.quit)

        return thread

    def start_jobs_thread(self):
        if not self.__thread_jobs.isRunning():
            self.__thread_jobs = self.__get_thread_jobs()
            self.__thread_jobs.start()
#!SECTION

    def closeEvent(self, event: QCloseEvent) -> None:
        self.stop_battery_test_mode()
        self.stop_monitor_thread()
        sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec())
