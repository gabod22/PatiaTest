from PySide6.QtWidgets import QDialog, QLineEdit, QListWidget,QMessageBox, QComboBox
from PySide6.QtGui import QCloseEvent
from ui.loading_dialog_ui import Ui_LoadingDialog

class LoadingDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_LoadingDialog()
        self.ui.setupUi(self)
        