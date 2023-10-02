import re
import pythoncom
import asyncio

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QThreadPool, QThread

from modules.helpers import add_data_to_table
from modules.systeminfo import get_system_info

from Jobs.worker import Worker
from Jobs.Jobs import Jobs
from modules.helpers import convert_size
from ui.loading_dialog_ui import Ui_LoadingDialog

from Dialogs.SuccessDialog import CustomDialog

from Dialogs import showSuccessDialog, showFailDialog
from modules.backend_connection import get_computer


class LoadingDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_LoadingDialog()
        self.ui.setupUi(self)
        self.__thread_jobs = QThread()
        self.threadpool = QThreadPool()
        self.serial_number = ""
        print("Multithreading with maximum %d threads" %
              self.threadpool.maxThreadCount())
        self.start_jobs_thread()
        self.start_get_system_info_thread()

    # SECTION - Jobs Thread
    def __get_thread_jobs(self):
        thread = QThread()
        worker = Jobs()
        worker.moveToThread(thread)

        # this is essential when worker is in local scope!
        thread.worker = worker

        thread.started.connect(worker.run)
        worker.configData.connect(self.setConfigData)
        worker.progress.connect(self.ui.PlainTextLog.appendPlainText)
        worker.error.connect(showFailDialog)

        return thread

    def loading_finished(self):
        self.parent.show()
        self.close()

    def setConfigData(self, data):

        self.parent.configData = data
        self.parent.setOptions()
        print("imprimiendo configuracion", data)

        # print(self.configData)

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

    def get_system_info_done(self):
        # self.statusBar().showMessage('Información obtenida')
        self.ui.PlainTextLog.appendPlainText('Información obtenida')
        self.start_get_computer_thread()

    def start_get_system_info_thread(self):
        # Pass the function to execute
        # Any other args, kwargs are passed to the run function
        pythoncom.CoInitialize()
        worker = Worker(get_system_info)
        worker.signals.result.connect(self.set_system_info)
        worker.signals.finished.connect(self.get_system_info_done)
        worker.signals.progress.connect(self.ui.PlainTextLog.appendPlainText)

        # Execute
        self.threadpool.start(worker)

    def start_get_computer_thread(self):
        # Pass the function to execute
        # Any other args, kwargs are passed to the run function
        worker = Worker(self.get_computer_from_server)
        # worker.signals.result.connect(self.show_dialog)
        worker.signals.progress.connect(self.ui.PlainTextLog.appendPlainText)
        worker.signals.showDialog.connect(lambda: self.show_dialog())

        # Execute
        self.threadpool.start(worker)

    def get_computer_from_server(self, progress_callback, on_error, show_dialog):

        progress_callback.emit('Obteniendo registro de la computadora')
        try:
            r = asyncio.run(get_computer(serial_number=self.serial_number))
            if r.status != 404:
                progress_callback.emit('La computadora ya está registrada')
            else:
                progress_callback.emit('No hay registro de la computadora')
                show_dialog.emit()
        except Exception as e:
            showFailDialog(self, str(e))

    def show_dialog(self):
        print('Mostrando dialogo')
        showSuccessDialog(self, 'La computadora no está registrada, si desea registrar la computadora, de click en registrar')

    def get_computer_done():
        print('asdasdads')
