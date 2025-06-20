# -*- coding: latin-1 -*-
import pythoncom
from PySide6.QtCore import QThreadPool, QThread, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QTableWidgetItem
from ui.loading_dialog_ui import Ui_LoadingDialog

from Jobs.Initialization import Initialization
from Jobs.GetPrograms import GetProgramsJob
from Jobs.DiskInfo import DiskInfoJob
from Jobs.Gpuz import GpuzJob

from PIL.ImageQt import ImageQt

from functools import partial
from modules.helpers.system_accions import open_program

from modules.utils import convert_size, is_battery_installed
from modules.helpers.helpers import add_data_to_table

import qrcode
# from PatiaTest import MainWindow
from functools import partial


# from Jobs.worker import Worker

# from Dialogs import showSuccessDialog, showFailDialog
from multiprocessing import freeze_support
freeze_support()
class LoadingDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.parent = parent
        self.enable_register = False
        self.ui = Ui_LoadingDialog()
        self.ui.setupUi(self)
        self.system_info = None
        self.__thread_initialization = QThread()
        self.__thread_gpuz = QThread()
        self.__thread_getprograms = QThread()
        self.__thread_diskinfo = QThread()
        self.threadpool = QThreadPool()
        self.serial_number = ""
        self.this_computer = None
        self.battery_health = ""

        print(
            "Multithreading with maximum %d threads" % self.threadpool.maxThreadCount()
        )

        self.start_jobs_thread()
        self.start_getprograms_thread()
        self.start_thread_gpuz()
        self.start_thread_diskinfo()


    # SECTION - Jobs Thread
    def __get_thread_initialization(self):
        thread = QThread()
        worker = Initialization()
        worker.moveToThread(thread)

        # this is essential when worker is in local scope!
        pythoncom.CoInitialize()
        thread.worker = worker

        thread.started.connect(worker.run)
        worker.systemData.connect(self.set_system_info)
        worker.progress.connect(self.ui.PlainTextLog.appendPlainText)
        worker.finished.connect(lambda: self.loading_finished())
        # worker.error.connect(lambda m: showFailDialog(self, m))

        return thread
    
    def start_jobs_thread(self):
        if not self.__thread_initialization.isRunning():
            self.__thread_initialization = self.__get_thread_initialization()
            self.__thread_initialization.start()

    def stop_jobs_thread(self):
        if self.__thread_initialization.isRunning():
            self.__thread_initialization.worker.stop()
            self.__thread_initialization.quit()
    
    def __get_thread_getprograms(self):
        thread = QThread()
        worker = GetProgramsJob()
        worker.moveToThread(thread)
        thread.worker = worker
        thread.started.connect(worker.run)
        worker.progress.connect(self.ui.PlainTextLog.appendPlainText)
        worker.finished.connect(self.set_programs_to_menu)
        
        return thread
    
    def set_programs_to_menu(self, programs):
        for program in programs:
            self.parent.ui.menuTools.addAction(
                program["name"], partial(open_program, program["name"])
            )
    
    def start_getprograms_thread(self):
        if not self.__thread_getprograms.isRunning():
            self.__thread_getprograms = self.__get_thread_getprograms()
            self.__thread_getprograms.start()

    def stop_getprograms_thread(self):
        if self.__thread_getprograms.isRunning():
            self.__thread_getprograms.worker.stop()
            self.__thread_getprograms.quit()
    
    def __get_thread_gpuz(self):
        thread = QThread()
        worker = GpuzJob()
        worker.moveToThread(thread)
        thread.worker = worker
        thread.started.connect(worker.run)
        worker.progress.connect(self.ui.PlainTextLog.appendPlainText)
        worker.finished.connect(self.set_gpu_info)
        
        return thread
    
    def set_gpu_info(self, gpus):
        print(gpus)
        self.parent.ui.TableGPUs.setRowCount(len(gpus))
        add_data_to_table(gpus, self.parent.ui.TableGPUs)
    
    def start_thread_gpuz(self):
        if not self.__thread_gpuz.isRunning():
            self.__thread_gpuz = self.__get_thread_gpuz()
            self.__thread_gpuz.start()

    def stop_thread_gpuz(self):
        if self.__thread_gpuz.isRunning():
            self.__thread_gpuz.worker.stop()
            self.__thread_gpuz.quit()
            
    def __get_thread_diskinfo(self):
        thread = QThread()
        worker = DiskInfoJob()
        worker.moveToThread(thread)
        thread.worker = worker
        thread.started.connect(worker.run)
        worker.progress.connect(self.ui.PlainTextLog.appendPlainText)
        worker.finished.connect(self.set_diskinfo)
        
        return thread
    
    def set_diskinfo(self, disks):
        if disks:
            for idx, disk in enumerate(disks):
                self.parent.ui.TableStorage.setItem(
                    0,
                    idx,
                    QTableWidgetItem(str(disk["Model"] if "Model" in disk else "")),
                )
                self.parent.ui.TableStorage.setItem(
                    1,
                    idx,
                    QTableWidgetItem(
                        str(disk["Disk Size"] if "Disk Size" in disk else "")
                    ),
                )
                self.parent.ui.TableStorage.setItem(
                    2,
                    idx,
                    QTableWidgetItem(
                        str(disk["Health Status"] if "Health Status" in disk else "")
                    ),
                )
                self.parent.ui.TableStorage.setItem(
                    3,
                    idx,
                    QTableWidgetItem(
                        str(disk["Interface"] if "Interface" in disk else "")
                    ),
                )
                self.parent.ui.TableStorage.setItem(
                    4,
                    idx,
                    QTableWidgetItem(
                        str(disk["Host Reads"] if "Host Reads" in disk else "")
                    ),
                )
                self.parent.ui.TableStorage.setItem(
                    5,
                    idx,
                    QTableWidgetItem(
                        str(disk["Host Writes"] if "Host Writes" in disk else "")
                    ),
                )
                self.parent.ui.TableStorage.setItem(
                    6,
                    idx,
                    QTableWidgetItem(
                        str(disk["Power On Count"] if "Power On Count" in disk else "")
                    ),
                )
                self.parent.ui.TableStorage.setItem(
                    7,
                    idx,
                    QTableWidgetItem(
                        str(disk["Power On Hours"] if "Power On Hours" in disk else "")
                    ),
                )
    
    def start_thread_diskinfo(self):
        if not self.__thread_diskinfo.isRunning():
            self.__thread_diskinfo = self.__get_thread_diskinfo()
            self.__thread_diskinfo.start()

    def stop_thread_diskinfo(self):
        if self.__thread_diskinfo.isRunning():
            self.__thread_diskinfo.worker.stop()
            self.__thread_diskinfo.quit()

    def setConfigData(self, data):
        self.parent.configData = data
        # print("imprimiendo configuracion", data)
        # print(self.configData)

    def setThisComputerData(self, data):
        self.enable_register = True
        self.parent.ui.TextPixelId.setText(str(data["internal_id"]))

    

    # SECTION - Get system info

    def set_system_info(self, info):
        self.system_info = info
        
        if len(info['cameras']) > 1:
            self.parent.ui.BtnSwitchCamera.setVisible(True) 
        
        model = info["computer_system"]["Model"]
        bios_ver = info["bios"]["Version"]
        serial = info["bios"]["SerialNumber"]
        # if (info['cpu']['vendor_id_raw'] == 'GenuineIntel'):
        #     try:
        #         cpu_model = re.search(
        #             "[A-z]\d-\d{4}[A-Z]", info["cpu"]["brand_raw"]).group()
        #     except:
        #         cpu_model = info["cpu"]["brand_raw"]
        # else:
        cpu_model = info["cpu"]["brand_raw"]
        ram = (
            str(convert_size(info["virtual_memory"]["total"]))
            + " "
            + info["memories"][0]["Tipo"]
        )
        self.parent.systeminfo = info
        self.parent.ui.TextWinver.setText(info["winver"])
        self.parent.ui.TextBiosVersion.setText(bios_ver)
        self.parent.ui.TextTotalRAM.setText(ram)
        self.parent.ui.TextProcessorName.setText(cpu_model)
        self.parent.ui.TextModel.setText(model)
        self.parent.ui.TextServiceNumber.setText(serial)
        # Add all Disks to table
        
        # Add all gpus to table
        
        self.serial_number = serial
        print(info['cameras'])

        if is_battery_installed():

            for idx, battery in enumerate(info["batteries"]):
                self.parent.ui.TableBatteryInfo.setItem(
                    0, idx, QTableWidgetItem(str(battery["Battery Name"]))
                )
                self.parent.ui.TableBatteryInfo.setItem(
                    1, idx, QTableWidgetItem(str(battery["Manufacture Name"]))
                )
                self.parent.ui.TableBatteryInfo.setItem(
                    2, idx, QTableWidgetItem(str(battery["Manufacture Date"]))
                )
                self.parent.ui.TableBatteryInfo.setItem(
                    3, idx, QTableWidgetItem(str(battery["Serial Number"]))
                )
                self.parent.ui.TableBatteryInfo.setItem(
                    4, idx, QTableWidgetItem(str(battery["Full Charged Capacity"]))
                )
                self.parent.ui.TableBatteryInfo.setItem(
                    5, idx, QTableWidgetItem(str(battery["Designed Capacity"]))
                )
                self.parent.ui.TableBatteryInfo.setItem(
                    6, idx, QTableWidgetItem(str(battery["Battery Health"]))
                )
                self.parent.ui.TableBatteryInfo.setItem(
                    7,
                    idx,
                    QTableWidgetItem(str(battery["Number of charge/discharge cycles"])),
                )

                if info["batteries"][idx]["Voltage"] != "":
                    if idx != len(info["batteries"]) - 1:
                        self.battery_health = (
                            self.battery_health
                            + info["batteries"][idx]["Battery Health"]
                            + ", "
                        )
                    else:
                        self.battery_health = (
                            self.battery_health
                            + info["batteries"][idx]["Battery Health"]
                        )
        else:
            self.battery_health = "Sin batería"

        self.parent.ui.TextBatteryHealth.setText(self.battery_health)
        
        data = {
            "model": model,
            "serial": serial,
            "battery": self.battery_health,
            "cpu": cpu_model,
            "ram": ram,
        }
        
        img = qrcode.make(data)
        
        qim = ImageQt(img)
        pix =QPixmap.fromImage(qim)
        self.parent.ui.LBQrCode.setPixmap(pix)




    def loading_finished(self):
        
        if is_battery_installed():
            self.parent.ui.tabBatteryTest.setEnabled(True)
        self.parent.show()
        self.close()

    # def closeEvent(self, event: QCloseEvent) -> None:
    #     # self.parent.close()
