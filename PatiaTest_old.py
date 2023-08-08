# -*- coding: latin-1 -*-

# This Python file uses the following encoding: utf-8
from ast import ExceptHandler, Lambda
import sys
from time import sleep
from typing import Sequence
from xml.sax.saxutils import prepare_input_source
import psutil
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QListWidget, QLineEdit, QMenu, QPushButton
from PySide6.QtCore import QThread, Signal, QObject, QThreadPool, QTimer
from PySide6.QtGui import QCloseEvent, QAction, QIcon
from multiprocessing import freeze_support
from functools import partial
from datetime import datetime
import pythoncom
import qrcode
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui.patiatest_ui import Ui_MainWindow
from ui.config_ui import Ui_ConfigDialog

from modules.gspread import *
from function import *
from modules.battery import is_battery_installed
from modules.programs import *
from modules.files_managment import *
from modules.constants import config_file
from modules.powerManager import set_configuration_to_current_scheme, set_brightness, set_default_configuration
from modules.battery import get_battery_info
from modules.wifi import connect, createNewConnection
from modules.constants import config
from modules.DiskInfoParser import DiskInfo
from modules.systeminfo import get_system_info

from Jobs.worker import Worker

from modules.helpers import secs2hours

from multiprocessing import Process, active_children, Pipe
import time
import psutil

DEFAULT_TIME = 60
TOTAL_CPU = psutil.cpu_count(logical=True)
PERCENT = 100



class Jobs(QObject):
    finished = Signal()
    progress = Signal(int)
    online = False

    def run(self):
        """Long-running task."""
        self.online = self.check_online()
        if self.online == False:
            createNewConnection(
                config['WIFI']['SSID'], config['WIFI']['SSID'], config['WIFI']['PASS'])
            createNewConnection(
                config['WIFI']['SSID5G'], config['WIFI']['SSID5G'], config['WIFI']['PASS5G'])
            connect(config['WIFI']['SSID'], config['WIFI']['SSID'])
            connect(config['WIFI']['SSID5G'], config['WIFI']['SSID5G'])
            sleep(1)
        self.online = self.check_online()
        if is_admin() and self.online:
            sync_date_time()
        self.finished.emit()

    def check_online(self):
        return (lambda a: True if 0 == a.system('ping google.com -w 4 > clear') else False)(__import__('os'))


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
        self._stopped = False
        batt_info = get_battery_info()
        if(batt_info["Voltage"] != ""):
            self.batHealth.emit(batt_info["Battery Health"])
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


class BatteryTest(QObject):
    
    

    #full_charged_remaining_time = Signal(str)
    percentage = Signal(str)
    timeElapsed = Signal(str)
    plugged = Signal(str)
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hora_inicio = datetime.now()
        self._stopped = False
        self._stopStressTest = False
        #self.batteries = batteries
        self.WAIT_TIME = 60  # seconds
        #self.HOURS_CONVERSION_CONSTANT= 3600/self.WAIT_TIME
        self.proc_num = TOTAL_CPU

        self.procs = []
        self.conns = []

    def get_time_elapsed(self):
        segundos_transcurridos = (
            datetime.now() - self.hora_inicio).total_seconds()
        return secs2hours(int(segundos_transcurridos))

    def run(self):

        while not self._stopped:
            battery = psutil.sensors_battery()
            if battery == None or battery.percent < 10:
                self._stopped = True
                self.stop_stress_test()
                break
            print('bateria', battery)
            self.start_stress_test()
            self.percentage.emit(battery.percent)
            self.plugged.emit(battery.power_plugged)
            self.timeElapsed.emit(self.get_time_elapsed())
            sleep(self.WAIT_TIME)
            with open('c:/battery_test.txt', 'a') as f:
                f.write(self.get_time_elapsed())
                f.write('\t')
                f.write(str(battery.power_plugged))
                f.write('\t')
                f.write(str(battery.percent))
                f.write('\n')

        self.stop_stress_test()
        self.finished.emit()

    def stop(self):
        self._stopped = True
    
    def loop(self, conn, affinity, check):
        '''
        Function to stress cores to run at 100%

        Arguments:
            conn    : child connection which is an object of Pipe()
            affinity: list of cores to assign affinity for the process
            check   : conditional flag to enable real time calibration
        '''
        proc = psutil.Process()
        proc_info = proc.pid
        msg = "Process ID: "+str(proc_info)+" CPU: "+str(affinity[0])   #Create a message string of PID and core number
        conn.send(msg)                                                  #Send message to parent
        conn.close()
        proc.cpu_affinity(affinity)                         #Assigns a core to process
        while True:
            '''
            Conditional check for calibration
            '''
            if(check and psutil.cpu_percent()>PERCENT):
                time.sleep(0.05)            #Change the time for finetuning
            1*1

    def last_core_loop(self, conn, affinity, percent):
        '''
        Function to stress the last core at fractional percentage.
        e.g. core 5 at 45% Usage

        Arguments:
            conn    : child connection which is an object of Pipe()
            affinity: list of cores to assign affinity for the process
            percent   : fractional percentage to run the core at
        '''
        proc = psutil.Process()
        proc_info = proc.pid
        msg = "Process ID: "+str(proc_info)+" CPU: "+str(affinity[0])   #Create a message string of PID and core number
        conn.send(msg)                                                  #Send message to parent
        conn.close()
        proc.cpu_affinity(affinity)                         #Assigns a core to process
        while True:
            '''
            Conditional check for core calibration
            '''
            if(psutil.cpu_percent(percpu=True)[affinity[0]] > percent):
                time.sleep(0.1)            #Change the time for finetuning
            1*1

    def start_stress_test(self):
        '''
        CPU Stress logic:
        '''

        print("Stressing %f cores:"%(self.proc_num))
        actual_cores = int(self.proc_num)
        last_core_usage = round((self.proc_num-actual_cores),2)*100
        self.proc_num = actual_cores

        #Run the required cores at 100% except one
        for i in range(self.proc_num-1):
            parent_conn, child_conn = Pipe()
            p = Process(target=self.loop, args=(child_conn,[i], False))
            p.start()
            self.procs.append(p)
            self.conns.append(parent_conn)

        #Run the last core out of the required cores to balance total output by actively calibrating realtime usage
        parent_conn, child_conn = Pipe()
        p = Process(target=self.loop, args=(child_conn,[self.proc_num-1], True))
        p.start()
        self.procs.append(p)
        self.conns.append(parent_conn)

        #If CPU usage is not 100%, run the fractional part of the last core
        if(self.proc_num!=TOTAL_CPU):
            last_core = self.proc_num
            parent_conn, child_conn = Pipe()
            p = Process(target=self.last_core_loop, args=(child_conn, [last_core], last_core_usage))
            p.start()
            self.procs.append(p)
            self.conns.append(parent_conn)

        #Print PID and core messages sent by the children
        for conn in self.conns:
            try:
                print(conn.recv())
            except EOFError:
                continue           
        

    def stop_stress_test(self):
        for p in self.procs:
            p.terminate() 



class ConfigDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.info = dict()
        self.ui = Ui_ConfigDialog()
        self.ui.setupUi(self)
        self.config = read_yaml(config_file)

        self.ui.BtnAdd.clicked.connect(lambda: self.add_item_to_list(
            self.ui.TextItemName, self.ui.ListEmployees))
        self.ui.BtnDelete.clicked.connect(
            lambda: self.del_selected_item_from_list(self.ui.ListEmployees))

        self.ui.BtnAddToSelectedPrograms.clicked.connect(lambda: self.move_item_to_list(
            self.ui.ListAllPrograms, self.ui.ListSelectedProgrms))
        self.ui.BtnDeleteFromSelectedPrograms.clicked.connect(
            lambda: self.del_selected_item_from_list(self.ui.ListSelectedProgrms))

        # Get Config info
        self.accepted.connect(lambda: self.save_config())
        self.rejected.connect(lambda: self.parent.update_config())
        self.set_config_info()

    def save_config(self):
        self.config['SPREAD_CONFIG']['DOCUMENT_NAME'] = self.ui.TextDocumentName.text()
        self.config['SPREAD_CONFIG']['WORKSHEET_NAME'] = self.ui.TextSheetName.text()
        self.config['DEFAULT_EMPLOYEE'] = self.ui.CboxDefaultEmployee.currentIndex()

        self.config['DEFAULT_VALUES']['ETHERNET'] = self.ui.CboxEthernet.currentIndex()
        self.config['DEFAULT_VALUES']['SUPPLY_PLUG'] = self.ui.CboxPlug.currentIndex()
        self.config['DEFAULT_VALUES']['USB'] = self.ui.CboxUSB.currentIndex()
        self.config['DEFAULT_VALUES']['SCREEN'] = self.ui.CboxScreen.currentIndex()
        self.config['DEFAULT_VALUES']['SPICKERS'] = self.ui.CboxSpikers.currentIndex()
        self.config['DEFAULT_VALUES']['KEYBOARD'] = self.ui.CboxKeyboard.currentIndex()
        self.config['DEFAULT_VALUES']['CAMERA'] = self.ui.CboxCamera.currentIndex()
        self.config['DEFAULT_VALUES']['MICROPHONE'] = self.ui.CboxMicro.currentIndex()
        self.config['DEFAULT_VALUES']['TOUCHPAD'] = self.ui.CboxTouchpad.currentIndex()
        self.config['DEFAULT_VALUES']['TOUCHSCREEN'] = self.ui.CboxTouchscreen.currentIndex()
        self.config['DEFAULT_VALUES']['HINGES'] = self.ui.CboxHinges.currentIndex()

        self.config['WIFI']['SSID5G'] = self.ui.TextSSID5G.text()
        self.config['WIFI']['PASS5G'] = self.ui.TextPass5G.text()
        self.config['WIFI']['SSID'] = self.ui.TextSSID.text()
        self.config['WIFI']['PASS'] = self.ui.TextPass.text()
        items = []
        for x in range(self.ui.ListEmployees.count()):
            items.append(self.ui.ListEmployees.item(x).text())
        self.config['EMPLOYEES'] = items
        items = []
        for x in range(self.ui.ListSelectedProgrms.count()):
            items.append(self.ui.ListSelectedProgrms.item(x).text())
        self.config['SELECTED_PROGRAMS'] = items

        try:
            write_yaml(config_file, self.config)
            self.parent.update_config()
            self.showSuccessDialog('Se cambio la configuracion correctamente')
            self.parent.update_config()
        except Exception as e:
            self.showFailDialog(
                'No se guardo la configuracion, pruebe manualmente')
            print(e)

    # Preferences
    def add_item_to_list(self, item: QLineEdit, list: QListWidget):
        if(item.text() != ""):
            list.addItem(item.text())
            self.ui.CboxDefaultEmployee.addItem(item.text())
            item.setText("")

    def del_selected_item_from_list(self, list: QListWidget):
        listItems = list.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.ui.CboxDefaultEmployee.removeItem(list.row(item))
            list.takeItem(list.row(item))

    def get_all_items_from_list(self, list: QListWidget):
        items = []
        for x in range(list.count()):
            items.append(list.item(x).text())
            print(list.item(x).text())
        return items

    def move_item_to_list(self, from_list: QListWidget, to_list: QListWidget):
        item = from_list.currentItem()
        for x in range(to_list.count()):
            if to_list.item(x).text() == item.text():
                return
        to_list.addItem(item.text())

    def set_config_info(self):
        self.ui.TextDocumentName.setText(
            self.config['SPREAD_CONFIG']['DOCUMENT_NAME'])
        self.ui.TextSheetName.setText(
            self.config['SPREAD_CONFIG']['WORKSHEET_NAME'])
        self.ui.CboxDefaultEmployee.addItems(self.config['EMPLOYEES'])
        self.ui.CboxDefaultEmployee.setCurrentIndex(
            self.config['DEFAULT_EMPLOYEE'])
        self.ui.ListEmployees.addItems(self.config['EMPLOYEES'])
        self.ui.ListAllPrograms.addItems(programs)

        if self.config['SELECTED_PROGRAMS']:
            self.ui.ListSelectedProgrms.addItems(
                self.config['SELECTED_PROGRAMS'])

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

        self.ui.TextPass5G.setText(self.config['WIFI']['PASS5G'])
        self.ui.TextSSID5G.setText(self.config['WIFI']['SSID5G'])
        self.ui.TextSSID.setText(self.config['WIFI']['SSID'])
        self.ui.TextPass.setText(self.config['WIFI']['PASS'])

    def showSuccessDialog(self, message='Todo bien'):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle("Todo correcto")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    def showFailDialog(self, message='todo mal :c'):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText(message)
        msgBox.setWindowTitle("Algo malo paso")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    def closeEvent(self, event: QCloseEvent) -> None:
        self.parent.update_config()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        print(dirname)
        super(MainWindow, self).__init__(*args, **kwargs)
        self.__thread_monitor = QThread()
        self.__thread_battery = QThread()
        self.__thread_jobs = QThread()
        self.data = [[]]
        self.notes = []
        self.config_dialog = None
        self.wks = None
        self.getDisksInfo()
        

        self.config = read_yaml(config_file)
        array_disks = get_disks_info()
        array_gpus = getGPUs()
        # get_batteries_info()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        if is_battery_installed():
            self.ui.BtnTestBattery.setEnabled(True)

        # MenuBar
        for program in programs:
            self.ui.menuTools.addAction(
                program, partial(open_program, program))

        # initial state
        self.ui.BtnStopSound.hide()
        self.asingMenuButtonsFunctions()
        self.update_config()
        self.asingAllButtonsFunctions()
        self.setAllInitialValues()
        self.start_threads()

        # Add all Disks to table
        self.ui.TableStorage.setRowCount(len(array_disks))
        self.add_data_to_table(array_disks, self.ui.TableStorage)

        # self.ui.TableBatteries.setRowCount(len(array_batteries))
        # self.add_data_to_table(array_batteries, self.ui.TableBatteries)

        # Add all gpus to table
        self.ui.TableVideoCards.setRowCount(len(array_gpus))
        self.add_data_to_table(array_gpus, self.ui.TableVideoCards)

        # Taks

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        
        self.start_thread_get_system_info()

        # self.threadpool.start()

    def save_to_google_sheets(self, progress_callback):
        status = ""
        self.data[0][1] = self.ui.TextModel.text()
        self.data[0].append(self.ui.TextModel.text())
        self.data[0].append(self.ui.CboxCheckedBy.currentText())
        self.data[0].append(self.ui.TextServiceNumber.text())
        self.data[0].append(self.ui.CboxGeneralState.currentText())
        self.data[0].append(self.ui.CboxAesthetics.currentText())
        self.data[0].append("")
        self.data[0].append(self.ui.TextBatteryHelath.text())
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
        self.data[0].append(self.ui.TextStorage.text())
        self.data[0].append(self.ui.PlainTextDetails.toPlainText())

        self.notes.append(self.ui.TextBatteryNote.text())
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
        self.notes.append(self.ui.TextStorageNote.text())
        print('Estoy guardando')
        self.ui.bntSaveTest.setEnabled(False)
        try:
            progress_callback.emit('Obteniendo worksheet')
            wks = get_worksheet()
            print(wks)
        except Exception as e:
                
            progress_callback.emit('Error al obtener el worksheet')
            print(e)
            return "No se guardó"

        try:
            progress_callback.emit('Guardando...')
            save_data_to_sheet(self.data, self.notes, wks)
            print('La info fue guardada correctamente')
        except Exception as e:
            # self.showFailDialog('La información no fue guardada.')
            progress_callback.emit('No se guardó...')
            print('La info no fue guardad :C %s' % e)
            print(e)
        finally:
            self.data = [[]]
            self.notes = []

            return "Finalizado"

    def fnDiskInfo(self):
        return DiskInfo()

    def getDisksInfo(self):
        worker = Worker(self.fnDiskInfo)
        worker.signals.result.connect(self.printDiksInfo)
        worker.signals.finished.connect(self.DiskInfoDone)
        worker.signals.progress.connect(self.statusBar().showMessage(
            'Obteniendo información de los discos'))

    def printDiksInfo(info):
        print('llegue aqui')
        print(info)

    def DiskInfoDone():
        print('Información de discos obtenida')

    def thread_complete(self):
        self.ui.bntSaveTest.setEnabled(True)
        print("THREAD COMPLETE!")
    
    def print_output(self, output):
        
        print(output)
        self.generateQrCode(output['computer_system']['Model'])

    def start_thread_save_to_google_sheets(self):
        # Pass the function to execute
        # Any other args, kwargs are passed to the run function
        worker = Worker(self.save_to_google_sheets)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.statusBar().showMessage)

        # Execute
        self.threadpool.start(worker)
    
    def get_system_info_done(self):
        self.statusBar().showMessage('Información obtenida')
        print("Info obteida")
        
    def start_thread_get_system_info(self):
        # Pass the function to execute
        # Any other args, kwargs are passed to the run function
        pythoncom.CoInitialize()
        worker = Worker(get_system_info)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.get_system_info_done)
        worker.signals.progress.connect(self.statusBar().showMessage)

        # Execute
        self.threadpool.start(worker)

    def open_config_dialog(self):
        if self.config_dialog is None:
            self.config_dialog = ConfigDialog(self)
            self.config_dialog.show()
        else:
            self.config_dialog = None

    def start_jobs_thread(self):
        if not self.__thread_jobs.isRunning():
            self.__thread_jobs = self.__get_thread_jobs()
            self.__thread_jobs.start()

    def start_threads(self):
        self.start_jobs_thread()
        if not self.__thread_monitor.isRunning():
            self.__thread_monitor = self.__get_thread_monitor()
            self.__thread_monitor.start()

    def stop_threads(self):
        if self.__thread_monitor.isRunning():
            self.__thread_monitor.quit()

        if self.__thread_battery.isRunning():
            self.__thread_battery.quit()

    def __get_thread_battery_test(self):
        thread = QThread()
        worker = BatteryTest()
        worker.moveToThread(thread)

        # this is essential when worker is in local scope!
        thread.worker = worker

        thread.started.connect(worker.run)
        worker.timeElapsed.connect(self.ui.LbBatteryTimeElapsed.setText)
        # worker.finished.connect(self.start_thread_save_to_google_sheets())
        # worker.finished.connect(lambda: kill_process_by_name('power_max.exe'))
        worker.finished.connect(thread.quit)

        # worker.percentage.connect()
        # worker.remaining_time.connect()
        # worker.plugged.connect()

        return thread

    def __get_thread_jobs(self):
        thread = QThread()
        worker = Jobs()
        worker.moveToThread(thread)

        # this is essential when worker is in local scope!
        thread.worker = worker

        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)

        return thread

    def __get_thread_monitor(self):
        thread = QThread()
        worker = Monitor()
        worker.moveToThread(thread)

        # this is essential when worker is in local scope!
        thread.worker = worker

        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)

        worker.cpuPercent.connect(self.ui.BarCPUPercentage.setValue)
        worker.ramPercent.connect(self.ui.BarRAMPercentage.setValue)
        worker.batPercent.connect(self.ui.BarBateryPercentage.setValue)
        worker.batStatus.connect(self.ui.LbBatteryStatus.setText)
        worker.batPlugged.connect(self.ui.LbPluggedIn.setText)
        worker.batRemainTime.connect(self.ui.LbBatteryRemain.setText)
        worker.batHealth.connect(self.ui.TextBatteryHelath.setText)

        return thread



    def update_config(self):
        self.config = read_yaml(config_file)
        self.ui.CboxCheckedBy.clear()
        self.ui.CboxCheckedBy.addItems(self.config['EMPLOYEES'])
        self.ui.CboxCheckedBy.setCurrentIndex(self.config['DEFAULT_EMPLOYEE'])
        # self.ui.CboxEthernet.setCurrentIndex(
        #     self.config['DEFAULT_VALUES']['ETHERNET'])
        # self.ui.CboxPlug.setCurrentIndex(
        #     self.config['DEFAULT_VALUES']['SUPPLY_PLUG'])
        # self.ui.CboxUSB.setCurrentIndex(self.config['DEFAULT_VALUES']['USB'])
        # self.ui.CboxScreen.setCurrentIndex(
        #     self.config['DEFAULT_VALUES']['SCREEN'])
        # self.ui.CboxSpikers.setCurrentIndex(
        #     self.config['DEFAULT_VALUES']['SPICKERS'])
        # self.ui.CboxKeyboard.setCurrentIndex(
        #     self.config['DEFAULT_VALUES']['KEYBOARD'])
        # self.ui.CboxCamera.setCurrentIndex(
        #     self.config['DEFAULT_VALUES']['CAMERA'])
        # self.ui.CboxMicro.setCurrentIndex(
        #     self.config['DEFAULT_VALUES']['MICROPHONE'])
        # self.ui.CboxTouchpad.setCurrentIndex(
        #     self.config['DEFAULT_VALUES']['TOUCHPAD'])
        # self.ui.CboxTouchscreen.setCurrentIndex(
        #     self.config['DEFAULT_VALUES']['TOUCHSCREEN'])
        # self.ui.CboxHinges.setCurrentIndex(
        #     self.config['DEFAULT_VALUES']['HINGES'])
        self.config_dialog = None

    def setAllInitialValues(self):
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

    def executeCommand(self):
        p = subprocess.Popen('cmd.cmd', stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        print("Command output : ", output.decode())
        print("Command exit status/return code : ", p_status)
        self.ui.CmdOutput.setPlainText(str(output.decode()))

    def asingAllButtonsFunctions(self):
        self.ui.BtnOpenAll.clicked.connect(lambda: self.open_all_tests())
        self.ui.BtnPlaySound.clicked.connect(lambda: self.playSound())
        self.ui.BtnStopSound.clicked.connect(lambda: self.stopSound())
        self.ui.BtnTestKeyboard.clicked.connect(
            lambda: open_program('keyboard_test.exe'))
        self.ui.BtnTestTouchscreen.clicked.connect(
            lambda: open_program('touch_test.exe'))
        self.ui.BtnOpenCamera.clicked.connect(
            lambda: run_powershell_command('start microsoft.windows.camera:'))
        self.ui.bntSaveTest.clicked.connect(
            lambda: self.start_thread_save_to_google_sheets())

        self.ui.BtnTestBattery.clicked.connect(
            lambda: self.open_battery_test_mode())
        self.ui.btnStopBatteryTest.clicked.connect(
            lambda: self.stop_battery_test_mode())
        self.ui.BtnConnectToWifi.clicked.connect(
            lambda: self.start_jobs_thread())
        self.ui.BtnCmd.clicked.connect(lambda: self.executeCommand())
        
    def generateQrCode(self, data):
        print(len(str(data)))
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=8
            )
        qr.add_data(str(data), 0)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save('Dieta.png')

    def asingMenuButtonsFunctions(self):
        # Config Menu
        self.ui.actionPreferencias.triggered.connect(
            lambda: self.open_config_dialog())


    def open_battery_test_mode(self):
        # open_program('battery_info.exe')
        open_program('power_max.exe')
        set_configuration_to_current_scheme()
        set_brightness('100')
        self.ui.btnStopBatteryTest.setEnabled(True)
        if not self.__thread_battery.isRunning():
            self.__thread_battery = self.__get_thread_battery_test()
            self.__thread_battery.start()

    def stop_battery_test_mode(self):
        self.ui.btnStopBatteryTest.setEnabled(False)
        set_brightness('50')
        set_default_configuration()
        # kill_process_by_name('battery_info.exe')
        kill_process_by_name('power_max.exe')
        if self.__thread_battery.isRunning():
            self.__thread_battery.worker.stop()

    def playSound(self):
        play_spiker_test_sound()
        self.ui.BtnPlaySound.hide()
        self.ui.BtnStopSound.show()

    def stopSound(self):
        stop_spiker_test_sound()
        self.ui.BtnPlaySound.show()
        self.ui.BtnStopSound.hide()
    def open_all_tests(self):

        for program in self.config['SELECTED_PROGRAMS']:
            open_program(program)

    def add_data_to_table(self, array, table):
        for row in range(len(array)):
            for column in range(len(array[row])):
                table.setItem(
                    row, column, QTableWidgetItem(array[row][column]))

    # Events
    def closeEvent(self, event: QCloseEvent) -> None:
        self.stop_threads()
        set_default_configuration()

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
    widget = MainWindow()
    widget.show()
    # widget.get_worksheet_fun()
    sys.exit(app.exec())
