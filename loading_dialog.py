import re
import pythoncom
import asyncio
from time import sleep
import json

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QThreadPool, QThread
from PySide6.QtGui import QCloseEvent
from modules.helpers import add_data_to_table
from modules.systeminfo import get_system_info

from Jobs.worker import Worker
from Jobs.Jobs import Jobs
from modules.helpers import convert_size
from ui.loading_dialog_ui import Ui_LoadingDialog

from Dialogs import showSuccessDialog, showFailDialog
from Dialogs.CustomDialogs import RegisterComputerDialog, RegisterFormDialog
from modules.backend_connection import get_computer



class LoadingDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.enable_register = False
        self.ui = Ui_LoadingDialog()
        self.ui.setupUi(self)
        self.__thread_jobs = QThread()
        self.threadpool = QThreadPool()
        self.serial_number = ""
        self.system_info = None
        self.this_computer = None
        
        print("Multithreading with maximum %d threads" %
              self.threadpool.maxThreadCount())
        
        # self.start_get_system_info_thread()
        self.start_jobs_thread()

    # SECTION - Jobs Thread
    def __get_thread_jobs(self):
        thread = QThread()
        worker = Jobs()
        worker.moveToThread(thread)

        # this is essential when worker is in local scope!
        pythoncom.CoInitialize()
        thread.worker = worker

        thread.started.connect(worker.run)
        worker.configData.connect(self.setConfigData)
        worker.thisComputer.connect(self.setThisComputerData)
        worker.systemData.connect(self.set_system_info)
        worker.progress.connect(self.ui.PlainTextLog.appendPlainText)
        worker.showDialog.connect(lambda: self.showRegisterComputerdialog())
        worker.error.connect(showFailDialog)
        worker.finished.connect(lambda: self.loading_finished())

        return thread

    

    def setConfigData(self, data):

        self.parent.configData = data
        self.parent.setOptions()
        # print("imprimiendo configuracion", data)

        # print(self.configData)
    def setThisComputerData(self, data):
        self.enable_register = True
        self.parent.ui.TextPixelId.setText(str(data['internal_id']))

    def start_jobs_thread(self):
        if not self.__thread_jobs.isRunning():
            self.__thread_jobs = self.__get_thread_jobs()
            self.__thread_jobs.start()

    def stop_jobs_thread(self):
        if self.__thread_jobs.isRunning():
            self.__thread_jobs.worker.stop()
            self.__thread_jobs.quit()

    # SECTION - Get system info

    def set_system_info(self, info):
        self.system_info = info
        cpu_model = re.search(
            "i\d-\d{4}[A-Z]", info["cpu"]["brand_raw"]).group()
        ram = str(convert_size(info["virtual_memory"]
                  ["total"])) + " " + info["memories"][0]["Tipo"]
        self.parent.systeminfo = info
        self.parent.ui.TextBiosVersion.setText(info["bios"]["Version"])
        self.parent.ui.TextTotalRAM.setText(ram)
        self.parent.ui.TextProcessorName.setText(cpu_model)
        self.parent.ui.TextModel.setText(info["computer_system"]["Model"])
        self.parent.ui.TextServiceNumber.setText(info["bios"]["SerialNumber"])
        # Add all Disks to table
        self.parent.ui.TableStorage.setRowCount(len(info['disks']))
        add_data_to_table(info['disks'],  self.parent.ui.TableStorage)
        # Add all gpus to table
        self.parent.ui.TableGPUs.setRowCount(len(info['gpus']))
        add_data_to_table(info['gpus'],  self.parent.ui.TableGPUs)
        self.serial_number = info["bios"]["SerialNumber"]
        

    def showRegisterComputerdialog(self):
        print('Mostrando dialogo')
        register = RegisterComputerDialog(self)
        result = register.exec_()
        if result:
            self.showRegisterFormDialog()
        else:
            self.loading_finished()
    
    def showRegisterFormDialog(self):
        print('Mostrando form')
        register = RegisterFormDialog(self)
        result = register.exec_()
        print(result)
        if result:
            print("Guardando info")
            self.enable_register = True
            print(self.this_computer)
            self.parent.ui.TextPixelId.setText(self.this_computer['internal_id'])
            self.loading_finished()
        self.loading_finished()
        
    def printMessage(self):
        print("se ha registrado")
        
    def get_computer_done(self):
        print('asdasdads')
    
    
    def loading_finished(self):
        if self.enable_register:
            self.parent.ui.tabReport.setEnabled(True)
        self.parent.show()
        self.hide()
        
    def closeEvent(self, event: QCloseEvent) -> None:
        self.parent.close()
        sleep(1)