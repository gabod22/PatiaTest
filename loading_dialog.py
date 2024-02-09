import pythoncom
from PySide6.QtCore import QThreadPool, QThread, Qt
from PySide6.QtWidgets import QDialog, QTableWidgetItem
from Dialogs.CustomDialogs import RegisterComputerDialog, RegisterFormDialog
from ui.loading_dialog_ui import Ui_LoadingDialog
from Jobs.Jobs import Jobs
from modules.helpers import convert_size
from modules.helpers import add_data_to_table
from modules.battery import is_battery_installed
from modules.programs import get_all_programs
from function import open_program
from functools import partial


# from Jobs.worker import Worker

# from Dialogs import showSuccessDialog, showFailDialog


class LoadingDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.parent = parent
        self.enable_register = False
        self.ui = Ui_LoadingDialog()
        self.ui.setupUi(self)
        self.system_info = None
        self.__thread_jobs = QThread()
        self.threadpool = QThreadPool()
        self.serial_number = ""
        self.this_computer = None
        self.battery_health = ""

        print("Multithreading with maximum %d threads" %
              self.threadpool.maxThreadCount())

        # self.start_get_system_info_thread()
        self.start_jobs_thread()

        # MenuBar
        for program in get_all_programs():
            # pixmap = QPixmap(program['icon'])
            # icon = QIcon(pixmap)
            self.parent.ui.menuTools.addAction(
                program["name"], partial(open_program, program["name"]))

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
        worker.finished.connect(lambda: self.loading_finished())
        # worker.error.connect(lambda m: showFailDialog(self, m))

        return thread

    def setConfigData(self, data):

        self.parent.configData = data
        self.parent.set_options()
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
        # if (info['cpu']['vendor_id_raw'] == 'GenuineIntel'):
        #     try:
        #         cpu_model = re.search(
        #             "[A-z]\d-\d{4}[A-Z]", info["cpu"]["brand_raw"]).group()
        #     except:
        #         cpu_model = info["cpu"]["brand_raw"]
        # else:
        cpu_model = info["cpu"]["brand_raw"]
        ram = str(convert_size(info["virtual_memory"]
                  ["total"])) + " " + info["memories"][0]["Tipo"]
        self.parent.systeminfo = info
        self.parent.ui.TextWinver.setText(info['winver'])
        self.parent.ui.TextBiosVersion.setText(info["bios"]["Version"])
        self.parent.ui.TextTotalRAM.setText(ram)
        self.parent.ui.TextProcessorName.setText(cpu_model)
        self.parent.ui.TextModel.setText(info["computer_system"]["Model"])
        self.parent.ui.TextServiceNumber.setText(info["bios"]["SerialNumber"])
        # Add all Disks to table
        # print(info['disks']['disks'])
        if 'disks' in info:
            for idx, disk in enumerate(info['disks']):
                self.parent.ui.TableStorage.setItem(
                    0, idx, QTableWidgetItem(str(disk['Model'] if 'Model' in disk else "")))
                self.parent.ui.TableStorage.setItem(
                    1, idx, QTableWidgetItem(str(disk['Disk Size'] if 'Disk Size' in disk else "")))
                self.parent.ui.TableStorage.setItem(
                    2, idx, QTableWidgetItem(str(disk['Health Status'] if 'Health Status' in disk else "")))
                self.parent.ui.TableStorage.setItem(
                    3, idx, QTableWidgetItem(str(disk['Interface'] if 'Interface' in disk else "")))
                self.parent.ui.TableStorage.setItem(
                    4, idx, QTableWidgetItem(str(disk['Host Reads'] if 'Host Reads' in disk else "")))
                self.parent.ui.TableStorage.setItem(
                    5, idx, QTableWidgetItem(str(disk['Host Writes'] if 'Host Writes' in disk else "")))
                self.parent.ui.TableStorage.setItem(
                    6, idx, QTableWidgetItem(str(disk['Power On Count'] if 'Power On Count' in disk else "")))
                self.parent.ui.TableStorage.setItem(
                    7, idx, QTableWidgetItem(str(disk['Power On Hours'] if 'Power On Hours' in disk else "")))
        # Add all gpus to table
        self.parent.ui.TableGPUs.setRowCount(len(info['gpus']))
        add_data_to_table(info['gpus'],  self.parent.ui.TableGPUs)
        self.serial_number = info["bios"]["SerialNumber"]

        if (is_battery_installed()):

            for idx, battery in enumerate(info['batteries']):
                self.parent.ui.TableBatteryInfo.setItem(0, idx, QTableWidgetItem(
                    str(battery["Battery Name"])))
                self.parent.ui.TableBatteryInfo.setItem(1, idx, QTableWidgetItem(
                    str(battery["Manufacture Name"])))
                self.parent.ui.TableBatteryInfo.setItem(2, idx, QTableWidgetItem(
                    str(battery["Manufacture Date"])))
                self.parent.ui.TableBatteryInfo.setItem(3, idx, QTableWidgetItem(
                    str(battery["Serial Number"])))
                self.parent.ui.TableBatteryInfo.setItem(4, idx, QTableWidgetItem(
                    str(battery["Full Charged Capacity"])))
                self.parent.ui.TableBatteryInfo.setItem(5, idx, QTableWidgetItem(
                    str(battery["Designed Capacity"])))
                self.parent.ui.TableBatteryInfo.setItem(6, idx, QTableWidgetItem(
                    str(battery["Battery Health"])))
                self.parent.ui.TableBatteryInfo.setItem(7, idx, QTableWidgetItem(
                    str(battery["Number of charge/discharge cycles"])))

                if (info['batteries'][idx]["Voltage"] != ""):
                    if idx != len(info['batteries']) - 1:
                        self.battery_health = self.battery_health + \
                            info['batteries'][idx]["Battery Health"] + ", "
                    else:
                        self.battery_health = self.battery_health + \
                            info['batteries'][idx]["Battery Health"]
        else:
            self.battery_health = "Sin batería"

        self.parent.ui.TextBatteryHealth.setText(self.battery_health)
        self.parent.ui.TextBatteryHealth_2.setText(self.battery_health)

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
        # print(result)
        if result:
            print("Guardando info")
            self.enable_register = True
            # print(self.this_computer)
            self.parent.ui.TextPixelId.setText(
                self.this_computer['internal_id'])
            self.loading_finished()
        self.loading_finished()

    def printMessage(self):
        print("se ha registrado")

    def get_computer_done(self):
        print('asdasdads')

    def loading_finished(self):
        if self.enable_register:
            self.parent.ui.tabReport.setEnabled(True)
        if is_battery_installed():
            self.parent.ui.tabBatteryTest.setEnabled(True)
        self.parent.show()
        self.close()

    # def closeEvent(self, event: QCloseEvent) -> None:
    #     # self.parent.close()
