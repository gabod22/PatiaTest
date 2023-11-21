from PySide6.QtWidgets import QDialog, QLineEdit, QListWidget, QMessageBox, QComboBox
from PySide6.QtGui import QCloseEvent
from ui.config_dialog_ui import Ui_Dialog
from modules.constants import config, config_file
from modules.files_managment import write_yaml
from modules.programs import get_all_programs


class ConfigDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.info = dict()
        self.config = config

        # SECTION - Programs
        self.ui.BtnAddToSelectedPrograms.clicked.connect(lambda: self.move_item_to_list(
            self.ui.ListAllPrograms, self.ui.ListSelectedProgrms))
        self.ui.BtnDeleteFromSelectedPrograms.clicked.connect(
            lambda: self.del_selected_item_from_list(self.ui.ListSelectedProgrms))

        # Get Config info
        self.accepted.connect(lambda: self.save_config())
        self.rejected.connect(lambda: self.parent.update_config())
        self.setOptions()
        self.set_config_info()

    def save_config(self):

        self.config['DEFAULT_EMPLOYEE'] = self.ui.CboxDefaultTechnician.currentIndex()

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
    def add_item_to_list(self, item: QLineEdit, list: QListWidget, cbox: QComboBox = None):
        if (item.text() != ""):
            list.addItem(item.text())
            if cbox != None:
                cbox.addItem(item.text())
            item.setText("")

    def del_selected_item_from_list(self, list: QListWidget, cbox: QComboBox = None):
        listItems = list.selectedItems()
        if not listItems:
            return
        for item in listItems:
            if cbox != None:
                cbox.removeItem(list.row(item))
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

    def setOptions(self):
        for status in self.parent.configData['component_statuses']:
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

    def set_config_info(self):

        for program in get_all_programs():
            self.ui.ListAllPrograms.addItem(program["name"])

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
