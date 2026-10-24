# -*- coding: utf-8 -*-
"""Startup tasks; hardware queries have an independently recoverable worker."""
from functools import partial
from os import path
from PIL.ImageQt import ImageQt
from PySide6.QtCore import QThread, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog
import qrcode
from Jobs.Initialization import Initialization
from Jobs.GetPrograms import GetProgramsJob
from modules.constants import dirname
from modules.helpers.system_accions import open_program
from modules.utils import convert_size, is_battery_installed
from ui.loading_dialog_ui import Ui_LoadingDialog


class LoadingDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.parent = parent
        self.ui = Ui_LoadingDialog()
        self.ui.setupUi(self)
        self.ui.Logo.setPixmap(QPixmap(path.join(dirname, "assets/logo_new.png")))
        self._pending = 2
        self.threads = []
        initialization = Initialization()
        initialization.systemData.connect(self.set_system_info)
        initialization.progress.connect(self.update_log)
        initialization.error.connect(self.update_log)
        initialization.finished.connect(self.job_finished)
        self.start_worker(initialization, initialization.finished)
        programs = GetProgramsJob()
        programs.finished.connect(self.set_programs_to_menu)
        programs.finished.connect(self.job_finished)
        programs.progress.connect(self.update_log)
        self.start_worker(programs, programs.finished)

    def start_worker(self, worker, finished):
        thread = QThread(self.parent)
        thread.worker = worker
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        finished.connect(thread.quit, Qt.DirectConnection)
        thread.finished.connect(worker.deleteLater)
        self.threads.append(thread)
        thread.start()

    def set_programs_to_menu(self, programs):
        existing = {action.text() for action in self.parent.ui.menuTools.actions()}
        for program in programs:
            if program["name"] not in existing:
                self.parent.ui.menuTools.addAction(program["name"], partial(open_program, program["name"]))

    def set_system_info(self, info):
        self.parent.systeminfo = info
        ui = self.parent.ui
        model = info.get("computer_system", {}).get("Model") or "No disponible"
        bios = info.get("bios", {})
        serial = bios.get("SerialNumber") or "No disponible"
        cpu = info.get("cpu", {}).get("brand_raw") or "No disponible"
        memory = info.get("memories", [])
        ram = convert_size(info.get("virtual_memory", {}).get("total", 0))
        if memory:
            ram += " " + memory[0].get("Tipo", "")
        ui.BtnSwitchCamera.setVisible(len(info.get("cameras", [])) > 1)
        ui.TextWinver.setText(info.get("winver", "No disponible"))
        ui.TextBiosVersion.setText(bios.get("Version") or "No disponible")
        ui.TextTotalRAM.setText(ram)
        ui.TextProcessorName.setText(cpu)
        ui.TextModel.setText(model)
        ui.TextServiceNumber.setText(serial)
        image = qrcode.make({"model": model, "serial": serial, "battery": ui.TextBatteryHealth.text(), "cpu": cpu, "ram": ram})
        ui.LBQrCode.setPixmap(QPixmap.fromImage(ImageQt(image.get_image())))

    def job_finished(self, *args):
        self._pending -= 1
        if self._pending == 0:
            self.parent.ui.tabBatteryTest.setEnabled(is_battery_installed())
            self.parent.show()
            self.close()

    def update_log(self, text):
        self.ui.PlainTextLog.appendPlainText(str(text))

    def stop(self):
        for thread in self.threads:
            if thread.isRunning() and hasattr(thread.worker, "stop"):
                thread.worker.stop()
            thread.quit()
        for thread in self.threads:
            thread.wait(5000)
