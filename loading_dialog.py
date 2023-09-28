from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QThreadPool, QThread

from Jobs.worker import Worker
from Jobs.Jobs import Jobs

from ui.loading_dialog_ui import Ui_LoadingDialog

class LoadingDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_LoadingDialog()
        self.ui.setupUi(self)
        self.threadpool = QThreadPool()
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
        worker.finished.connect(thread.quit)
        worker.error.connect(self.showFailDialog)
        

        return thread

    def setConfigData(self, data):
        self.configData = data
        self.setOptions()
        # print(self.configData)
        self.show()

    def start_jobs_thread(self):
        self.showSuccessDialog(message="Cargando la información")
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
        self.systeminfo = info
        self.ui.TextBiosVersion.setText(info["bios"]["Version"])
        self.ui.TextTotalRAM.setText(ram)
        self.ui.TextProcessorName.setText(cpu_model)
        self.ui.TextModel.setText(info["computer_system"]["Model"])
        self.ui.TextServiceNumber.setText(info["bios"]["SerialNumber"])
        # Add all Disks to table
        self.ui.TableStorage.setRowCount(len(info['disks']))
        add_data_to_table(info['disks'], self.ui.TableStorage)
        # Add all gpus to table
        self.ui.TableGPUs.setRowCount(len(info['gpus']))
        add_data_to_table(info['gpus'], self.ui.TableGPUs)
        

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