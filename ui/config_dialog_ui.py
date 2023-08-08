# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(512, 538)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_17 = QVBoxLayout(self.tab_6)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.scrollArea_2 = QScrollArea(self.tab_6)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, -331, 451, 806))
        self.verticalLayout_16 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.groupBox_5 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout_8 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.ListTechnician = QListWidget(self.groupBox_5)
        self.ListTechnician.setObjectName(u"ListTechnician")

        self.horizontalLayout_8.addWidget(self.ListTechnician)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.TextTechnicianName = QLineEdit(self.groupBox_5)
        self.TextTechnicianName.setObjectName(u"TextTechnicianName")

        self.verticalLayout_15.addWidget(self.TextTechnicianName)

        self.BtnAddTechnician = QPushButton(self.groupBox_5)
        self.BtnAddTechnician.setObjectName(u"BtnAddTechnician")

        self.verticalLayout_15.addWidget(self.BtnAddTechnician)

        self.BtnDeleteTechnician = QPushButton(self.groupBox_5)
        self.BtnDeleteTechnician.setObjectName(u"BtnDeleteTechnician")

        self.verticalLayout_15.addWidget(self.BtnDeleteTechnician)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_15.addItem(self.verticalSpacer_8)

        self.label_7 = QLabel(self.groupBox_5)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_15.addWidget(self.label_7)

        self.CboxDefaultTechnician = QComboBox(self.groupBox_5)
        self.CboxDefaultTechnician.setObjectName(u"CboxDefaultTechnician")

        self.verticalLayout_15.addWidget(self.CboxDefaultTechnician)


        self.horizontalLayout_8.addLayout(self.verticalLayout_15)


        self.verticalLayout_16.addWidget(self.groupBox_5)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.ListComponentStateOptions = QListWidget(self.groupBox_3)
        self.ListComponentStateOptions.setObjectName(u"ListComponentStateOptions")

        self.horizontalLayout_6.addWidget(self.ListComponentStateOptions)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.TextComponentSatateOption = QLineEdit(self.groupBox_3)
        self.TextComponentSatateOption.setObjectName(u"TextComponentSatateOption")

        self.verticalLayout_13.addWidget(self.TextComponentSatateOption)

        self.BtnAddComponenteStateOption = QPushButton(self.groupBox_3)
        self.BtnAddComponenteStateOption.setObjectName(u"BtnAddComponenteStateOption")

        self.verticalLayout_13.addWidget(self.BtnAddComponenteStateOption)

        self.BtnDeleteComponenteStateOption = QPushButton(self.groupBox_3)
        self.BtnDeleteComponenteStateOption.setObjectName(u"BtnDeleteComponenteStateOption")

        self.verticalLayout_13.addWidget(self.BtnDeleteComponenteStateOption)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_6)


        self.horizontalLayout_6.addLayout(self.verticalLayout_13)


        self.verticalLayout_16.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.ListAesthericOptions = QListWidget(self.groupBox_4)
        self.ListAesthericOptions.setObjectName(u"ListAesthericOptions")

        self.horizontalLayout_7.addWidget(self.ListAesthericOptions)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.TextAestheticOption = QLineEdit(self.groupBox_4)
        self.TextAestheticOption.setObjectName(u"TextAestheticOption")

        self.verticalLayout_14.addWidget(self.TextAestheticOption)

        self.BtnAddAestheticOption = QPushButton(self.groupBox_4)
        self.BtnAddAestheticOption.setObjectName(u"BtnAddAestheticOption")

        self.verticalLayout_14.addWidget(self.BtnAddAestheticOption)

        self.BtnDeleteAestheticOption = QPushButton(self.groupBox_4)
        self.BtnDeleteAestheticOption.setObjectName(u"BtnDeleteAestheticOption")

        self.verticalLayout_14.addWidget(self.BtnDeleteAestheticOption)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_7)


        self.horizontalLayout_7.addLayout(self.verticalLayout_14)


        self.verticalLayout_16.addWidget(self.groupBox_4)

        self.groupBox_6 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.groupBox_6)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.TextDocumentName = QLineEdit(self.groupBox_6)
        self.TextDocumentName.setObjectName(u"TextDocumentName")

        self.verticalLayout_4.addWidget(self.TextDocumentName)

        self.label_2 = QLabel(self.groupBox_6)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_4.addWidget(self.label_2)

        self.TextSheetName = QLineEdit(self.groupBox_6)
        self.TextSheetName.setObjectName(u"TextSheetName")

        self.verticalLayout_4.addWidget(self.TextSheetName)


        self.verticalLayout_16.addWidget(self.groupBox_6)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_6.addWidget(self.label_17)

        self.TextSSID5G = QLineEdit(self.groupBox_2)
        self.TextSSID5G.setObjectName(u"TextSSID5G")

        self.verticalLayout_6.addWidget(self.TextSSID5G)


        self.horizontalLayout.addLayout(self.verticalLayout_6)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_7.addWidget(self.label_6)

        self.TextPass5G = QLineEdit(self.groupBox_2)
        self.TextPass5G.setObjectName(u"TextPass5G")

        self.verticalLayout_7.addWidget(self.TextPass5G)


        self.horizontalLayout.addLayout(self.verticalLayout_7)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.groupBox_7 = QGroupBox(self.groupBox)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_5 = QLabel(self.groupBox_7)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_8.addWidget(self.label_5)

        self.TextSSID = QLineEdit(self.groupBox_7)
        self.TextSSID.setObjectName(u"TextSSID")

        self.verticalLayout_8.addWidget(self.TextSSID)


        self.horizontalLayout_3.addLayout(self.verticalLayout_8)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_4 = QLabel(self.groupBox_7)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_9.addWidget(self.label_4)

        self.TextPass = QLineEdit(self.groupBox_7)
        self.TextPass.setObjectName(u"TextPass")

        self.verticalLayout_9.addWidget(self.TextPass)


        self.horizontalLayout_3.addLayout(self.verticalLayout_9)


        self.verticalLayout_3.addWidget(self.groupBox_7)


        self.verticalLayout_16.addWidget(self.groupBox)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_17.addWidget(self.scrollArea_2)

        self.tabWidget.addTab(self.tab_6, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_12 = QVBoxLayout(self.tab_3)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.scrollArea = QScrollArea(self.tab_3)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 468, 441))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_13 = QLabel(self.scrollAreaWidgetContents)
        self.label_13.setObjectName(u"label_13")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_13)

        self.CboxEthernet = QComboBox(self.scrollAreaWidgetContents)
        self.CboxEthernet.setObjectName(u"CboxEthernet")
        self.CboxEthernet.setMinimumSize(QSize(140, 0))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.CboxEthernet)

        self.label_14 = QLabel(self.scrollAreaWidgetContents)
        self.label_14.setObjectName(u"label_14")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_14)

        self.CboxPlug = QComboBox(self.scrollAreaWidgetContents)
        self.CboxPlug.setObjectName(u"CboxPlug")
        self.CboxPlug.setMinimumSize(QSize(140, 0))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.CboxPlug)

        self.label_15 = QLabel(self.scrollAreaWidgetContents)
        self.label_15.setObjectName(u"label_15")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_15)

        self.CboxUSB = QComboBox(self.scrollAreaWidgetContents)
        self.CboxUSB.setObjectName(u"CboxUSB")
        self.CboxUSB.setMinimumSize(QSize(140, 0))

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.CboxUSB)

        self.label_16 = QLabel(self.scrollAreaWidgetContents)
        self.label_16.setObjectName(u"label_16")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_16)

        self.CboxScreen = QComboBox(self.scrollAreaWidgetContents)
        self.CboxScreen.setObjectName(u"CboxScreen")
        self.CboxScreen.setMinimumSize(QSize(140, 0))

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.CboxScreen)

        self.label_18 = QLabel(self.scrollAreaWidgetContents)
        self.label_18.setObjectName(u"label_18")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_18)

        self.CboxSpikers = QComboBox(self.scrollAreaWidgetContents)
        self.CboxSpikers.setObjectName(u"CboxSpikers")
        self.CboxSpikers.setMinimumSize(QSize(140, 0))

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.CboxSpikers)

        self.label_19 = QLabel(self.scrollAreaWidgetContents)
        self.label_19.setObjectName(u"label_19")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_19)

        self.CboxKeyboard = QComboBox(self.scrollAreaWidgetContents)
        self.CboxKeyboard.setObjectName(u"CboxKeyboard")
        self.CboxKeyboard.setMinimumSize(QSize(140, 0))

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.CboxKeyboard)

        self.label_20 = QLabel(self.scrollAreaWidgetContents)
        self.label_20.setObjectName(u"label_20")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_20)

        self.CboxCamera = QComboBox(self.scrollAreaWidgetContents)
        self.CboxCamera.setObjectName(u"CboxCamera")
        self.CboxCamera.setMinimumSize(QSize(140, 0))

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.CboxCamera)

        self.label_21 = QLabel(self.scrollAreaWidgetContents)
        self.label_21.setObjectName(u"label_21")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_21)

        self.CboxMicro = QComboBox(self.scrollAreaWidgetContents)
        self.CboxMicro.setObjectName(u"CboxMicro")
        self.CboxMicro.setMinimumSize(QSize(140, 0))

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.CboxMicro)

        self.label_22 = QLabel(self.scrollAreaWidgetContents)
        self.label_22.setObjectName(u"label_22")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_22)

        self.CboxTouchpad = QComboBox(self.scrollAreaWidgetContents)
        self.CboxTouchpad.setObjectName(u"CboxTouchpad")
        self.CboxTouchpad.setMinimumSize(QSize(140, 0))

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.CboxTouchpad)

        self.label_25 = QLabel(self.scrollAreaWidgetContents)
        self.label_25.setObjectName(u"label_25")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_25)

        self.CboxTouchscreen = QComboBox(self.scrollAreaWidgetContents)
        self.CboxTouchscreen.setObjectName(u"CboxTouchscreen")
        self.CboxTouchscreen.setMinimumSize(QSize(140, 0))

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.CboxTouchscreen)

        self.label_26 = QLabel(self.scrollAreaWidgetContents)
        self.label_26.setObjectName(u"label_26")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.label_26)

        self.CboxHinges = QComboBox(self.scrollAreaWidgetContents)
        self.CboxHinges.setObjectName(u"CboxHinges")
        self.CboxHinges.setMinimumSize(QSize(140, 0))

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.CboxHinges)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_12.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.horizontalLayout_5 = QHBoxLayout(self.tab_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.ListAllPrograms = QListWidget(self.tab_5)
        self.ListAllPrograms.setObjectName(u"ListAllPrograms")

        self.horizontalLayout_5.addWidget(self.ListAllPrograms)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.BtnAddToSelectedPrograms = QPushButton(self.tab_5)
        self.BtnAddToSelectedPrograms.setObjectName(u"BtnAddToSelectedPrograms")

        self.verticalLayout_11.addWidget(self.BtnAddToSelectedPrograms)

        self.BtnDeleteFromSelectedPrograms = QPushButton(self.tab_5)
        self.BtnDeleteFromSelectedPrograms.setObjectName(u"BtnDeleteFromSelectedPrograms")

        self.verticalLayout_11.addWidget(self.BtnDeleteFromSelectedPrograms)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_5)


        self.horizontalLayout_5.addLayout(self.verticalLayout_11)

        self.ListSelectedProgrms = QListWidget(self.tab_5)
        self.ListSelectedProgrms.setObjectName(u"ListSelectedProgrms")

        self.horizontalLayout_5.addWidget(self.ListSelectedProgrms)

        self.tabWidget.addTab(self.tab_5, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.tabWidget.setCurrentIndex(1)
        self.CboxEthernet.setCurrentIndex(-1)
        self.CboxPlug.setCurrentIndex(-1)
        self.CboxUSB.setCurrentIndex(-1)
        self.CboxScreen.setCurrentIndex(-1)
        self.CboxSpikers.setCurrentIndex(-1)
        self.CboxKeyboard.setCurrentIndex(-1)
        self.CboxCamera.setCurrentIndex(-1)
        self.CboxMicro.setCurrentIndex(-1)
        self.CboxTouchpad.setCurrentIndex(-1)
        self.CboxTouchscreen.setCurrentIndex(-1)
        self.CboxHinges.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Dialog", u"T\u00e9cnicos", None))
        self.BtnAddTechnician.setText(QCoreApplication.translate("Dialog", u"A\u00f1adir", None))
        self.BtnDeleteTechnician.setText(QCoreApplication.translate("Dialog", u"Eliminar Seleccionado", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Empledo por defecto", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Opciones de estado de componente", None))
        self.BtnAddComponenteStateOption.setText(QCoreApplication.translate("Dialog", u"A\u00f1adir", None))
        self.BtnDeleteComponenteStateOption.setText(QCoreApplication.translate("Dialog", u"Eliminar Seleccionado", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Opciones de est\u00e9tica", None))
        self.BtnAddAestheticOption.setText(QCoreApplication.translate("Dialog", u"A\u00f1adir", None))
        self.BtnDeleteAestheticOption.setText(QCoreApplication.translate("Dialog", u"Eliminar Seleccionado", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Dialog", u"Google Sheets", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Documento", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Pesta\u00f1a", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"WIFI", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"5G", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"SSID", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Contrase\u00f1a", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Dialog", u"2.4G", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"SSID", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Contrase\u00f1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("Dialog", u"General", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Ethernet", None))
        self.CboxEthernet.setCurrentText("")
        self.CboxEthernet.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Puerto de carga", None))
        self.CboxPlug.setCurrentText("")
        self.CboxPlug.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"USB", None))
        self.CboxUSB.setCurrentText("")
        self.CboxUSB.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Pantalla", None))
        self.CboxScreen.setCurrentText("")
        self.CboxScreen.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Bocinas", None))
        self.CboxSpikers.setCurrentText("")
        self.CboxSpikers.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Teclado", None))
        self.CboxKeyboard.setCurrentText("")
        self.CboxKeyboard.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"C\u00e1mara", None))
        self.CboxCamera.setCurrentText("")
        self.CboxCamera.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Microfono", None))
        self.CboxMicro.setCurrentText("")
        self.CboxMicro.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"TouchPad", None))
        self.CboxTouchpad.setCurrentText("")
        self.CboxTouchpad.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"TouchScreen", None))
        self.CboxTouchscreen.setCurrentText("")
        self.CboxTouchscreen.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"Bisagras", None))
        self.CboxHinges.setCurrentText("")
        self.CboxHinges.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"Valores por defecto", None))
        self.BtnAddToSelectedPrograms.setText(QCoreApplication.translate("Dialog", u"Agregar", None))
        self.BtnDeleteFromSelectedPrograms.setText(QCoreApplication.translate("Dialog", u"Eliminar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("Dialog", u"Programas", None))
    # retranslateUi

