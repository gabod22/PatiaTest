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
        Dialog.resize(637, 604)
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
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 593, 507))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_17)

        self.TextSSID5G = QLineEdit(self.groupBox_2)
        self.TextSSID5G.setObjectName(u"TextSSID5G")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.TextSSID5G)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_6)

        self.TextPass5G = QLineEdit(self.groupBox_2)
        self.TextPass5G.setObjectName(u"TextPass5G")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.TextPass5G)


        self.horizontalLayout.addLayout(self.formLayout_2)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.groupBox_7 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_5 = QLabel(self.groupBox_7)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.TextSSID = QLineEdit(self.groupBox_7)
        self.TextSSID.setObjectName(u"TextSSID")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.TextSSID)

        self.label_4 = QLabel(self.groupBox_7)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.TextPass = QLineEdit(self.groupBox_7)
        self.TextPass.setObjectName(u"TextPass")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.TextPass)


        self.horizontalLayout_3.addLayout(self.formLayout_3)


        self.verticalLayout_2.addWidget(self.groupBox_7)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 593, 507))
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.label_30 = QLabel(self.scrollAreaWidgetContents)
        self.label_30.setObjectName(u"label_30")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_30)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.CboxBattery = QComboBox(self.scrollAreaWidgetContents)
        self.CboxBattery.setObjectName(u"CboxBattery")
        self.CboxBattery.setMinimumSize(QSize(150, 0))
        self.CboxBattery.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_2.addWidget(self.CboxBattery)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.BtnResetBattery = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetBattery.setObjectName(u"BtnResetBattery")
        self.BtnResetBattery.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.BtnResetBattery)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_13 = QLabel(self.scrollAreaWidgetContents)
        self.label_13.setObjectName(u"label_13")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_13)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.CboxEthernet = QComboBox(self.scrollAreaWidgetContents)
        self.CboxEthernet.setObjectName(u"CboxEthernet")
        self.CboxEthernet.setMinimumSize(QSize(150, 0))
        self.CboxEthernet.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_4.addWidget(self.CboxEthernet)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.BtnResetEthernet = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetEthernet.setObjectName(u"BtnResetEthernet")
        self.BtnResetEthernet.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_4.addWidget(self.BtnResetEthernet)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.label_14 = QLabel(self.scrollAreaWidgetContents)
        self.label_14.setObjectName(u"label_14")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_14)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.CboxPlug = QComboBox(self.scrollAreaWidgetContents)
        self.CboxPlug.setObjectName(u"CboxPlug")
        self.CboxPlug.setMinimumSize(QSize(150, 0))
        self.CboxPlug.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_6.addWidget(self.CboxPlug)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.BtnResetPlug = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetPlug.setObjectName(u"BtnResetPlug")
        self.BtnResetPlug.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_6.addWidget(self.BtnResetPlug)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_6)

        self.label_15 = QLabel(self.scrollAreaWidgetContents)
        self.label_15.setObjectName(u"label_15")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_15)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.CboxUSB = QComboBox(self.scrollAreaWidgetContents)
        self.CboxUSB.setObjectName(u"CboxUSB")
        self.CboxUSB.setMinimumSize(QSize(150, 0))
        self.CboxUSB.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_7.addWidget(self.CboxUSB)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)

        self.BtnResetUSB = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetUSB.setObjectName(u"BtnResetUSB")
        self.BtnResetUSB.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_7.addWidget(self.BtnResetUSB)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_7)

        self.label_16 = QLabel(self.scrollAreaWidgetContents)
        self.label_16.setObjectName(u"label_16")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_16)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.CboxScreen = QComboBox(self.scrollAreaWidgetContents)
        self.CboxScreen.setObjectName(u"CboxScreen")
        self.CboxScreen.setMinimumSize(QSize(150, 0))
        self.CboxScreen.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_8.addWidget(self.CboxScreen)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)

        self.BtnResetScreen = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetScreen.setObjectName(u"BtnResetScreen")
        self.BtnResetScreen.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_8.addWidget(self.BtnResetScreen)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_8)

        self.label_18 = QLabel(self.scrollAreaWidgetContents)
        self.label_18.setObjectName(u"label_18")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_18)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.CboxSpikers = QComboBox(self.scrollAreaWidgetContents)
        self.CboxSpikers.setObjectName(u"CboxSpikers")
        self.CboxSpikers.setMinimumSize(QSize(150, 0))
        self.CboxSpikers.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_9.addWidget(self.CboxSpikers)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_6)

        self.BtnResetSpikers = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetSpikers.setObjectName(u"BtnResetSpikers")
        self.BtnResetSpikers.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_9.addWidget(self.BtnResetSpikers)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_9)

        self.label_19 = QLabel(self.scrollAreaWidgetContents)
        self.label_19.setObjectName(u"label_19")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_19)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.CboxKeyboard = QComboBox(self.scrollAreaWidgetContents)
        self.CboxKeyboard.setObjectName(u"CboxKeyboard")
        self.CboxKeyboard.setMinimumSize(QSize(150, 0))
        self.CboxKeyboard.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_10.addWidget(self.CboxKeyboard)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_7)

        self.BtnResetKeyboard = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetKeyboard.setObjectName(u"BtnResetKeyboard")
        self.BtnResetKeyboard.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_10.addWidget(self.BtnResetKeyboard)


        self.formLayout.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout_10)

        self.label_20 = QLabel(self.scrollAreaWidgetContents)
        self.label_20.setObjectName(u"label_20")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_20)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.CboxCamera = QComboBox(self.scrollAreaWidgetContents)
        self.CboxCamera.setObjectName(u"CboxCamera")
        self.CboxCamera.setMinimumSize(QSize(150, 0))
        self.CboxCamera.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_11.addWidget(self.CboxCamera)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_8)

        self.BtnResetCamera = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetCamera.setObjectName(u"BtnResetCamera")
        self.BtnResetCamera.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_11.addWidget(self.BtnResetCamera)


        self.formLayout.setLayout(7, QFormLayout.FieldRole, self.horizontalLayout_11)

        self.label_21 = QLabel(self.scrollAreaWidgetContents)
        self.label_21.setObjectName(u"label_21")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_21)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.CboxMicro = QComboBox(self.scrollAreaWidgetContents)
        self.CboxMicro.setObjectName(u"CboxMicro")
        self.CboxMicro.setMinimumSize(QSize(150, 0))
        self.CboxMicro.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_12.addWidget(self.CboxMicro)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_9)

        self.BtnResetMicro = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetMicro.setObjectName(u"BtnResetMicro")
        self.BtnResetMicro.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_12.addWidget(self.BtnResetMicro)


        self.formLayout.setLayout(8, QFormLayout.FieldRole, self.horizontalLayout_12)

        self.label_32 = QLabel(self.scrollAreaWidgetContents)
        self.label_32.setObjectName(u"label_32")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_32)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.CboxConnectivity = QComboBox(self.scrollAreaWidgetContents)
        self.CboxConnectivity.setObjectName(u"CboxConnectivity")
        self.CboxConnectivity.setMinimumSize(QSize(150, 0))
        self.CboxConnectivity.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_13.addWidget(self.CboxConnectivity)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_10)

        self.BtnResetConnectivity = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetConnectivity.setObjectName(u"BtnResetConnectivity")
        self.BtnResetConnectivity.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_13.addWidget(self.BtnResetConnectivity)


        self.formLayout.setLayout(9, QFormLayout.FieldRole, self.horizontalLayout_13)

        self.label_22 = QLabel(self.scrollAreaWidgetContents)
        self.label_22.setObjectName(u"label_22")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.label_22)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.CboxTouchpad = QComboBox(self.scrollAreaWidgetContents)
        self.CboxTouchpad.setObjectName(u"CboxTouchpad")
        self.CboxTouchpad.setMinimumSize(QSize(150, 0))
        self.CboxTouchpad.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_14.addWidget(self.CboxTouchpad)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_11)

        self.BtnResetTouchpad = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetTouchpad.setObjectName(u"BtnResetTouchpad")
        self.BtnResetTouchpad.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_14.addWidget(self.BtnResetTouchpad)


        self.formLayout.setLayout(10, QFormLayout.FieldRole, self.horizontalLayout_14)

        self.label_25 = QLabel(self.scrollAreaWidgetContents)
        self.label_25.setObjectName(u"label_25")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.label_25)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.CboxTouchscreen = QComboBox(self.scrollAreaWidgetContents)
        self.CboxTouchscreen.setObjectName(u"CboxTouchscreen")
        self.CboxTouchscreen.setMinimumSize(QSize(150, 0))
        self.CboxTouchscreen.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_15.addWidget(self.CboxTouchscreen)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_12)

        self.BtnResetTouchscreen = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetTouchscreen.setObjectName(u"BtnResetTouchscreen")
        self.BtnResetTouchscreen.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_15.addWidget(self.BtnResetTouchscreen)


        self.formLayout.setLayout(11, QFormLayout.FieldRole, self.horizontalLayout_15)

        self.label_26 = QLabel(self.scrollAreaWidgetContents)
        self.label_26.setObjectName(u"label_26")

        self.formLayout.setWidget(12, QFormLayout.LabelRole, self.label_26)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.CboxHinges = QComboBox(self.scrollAreaWidgetContents)
        self.CboxHinges.setObjectName(u"CboxHinges")
        self.CboxHinges.setMinimumSize(QSize(150, 0))
        self.CboxHinges.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_16.addWidget(self.CboxHinges)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_13)

        self.BtnResetHinges = QPushButton(self.scrollAreaWidgetContents)
        self.BtnResetHinges.setObjectName(u"BtnResetHinges")
        self.BtnResetHinges.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_16.addWidget(self.BtnResetHinges)


        self.formLayout.setLayout(12, QFormLayout.FieldRole, self.horizontalLayout_16)

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
        self.CboxBattery.setCurrentIndex(-1)
        self.CboxEthernet.setCurrentIndex(-1)
        self.CboxPlug.setCurrentIndex(-1)
        self.CboxUSB.setCurrentIndex(-1)
        self.CboxScreen.setCurrentIndex(-1)
        self.CboxSpikers.setCurrentIndex(-1)
        self.CboxKeyboard.setCurrentIndex(-1)
        self.CboxCamera.setCurrentIndex(-1)
        self.CboxMicro.setCurrentIndex(-1)
        self.CboxConnectivity.setCurrentIndex(-1)
        self.CboxTouchpad.setCurrentIndex(-1)
        self.CboxTouchscreen.setCurrentIndex(-1)
        self.CboxHinges.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"WIFI 5G", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"SSID", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Contrase\u00f1a", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Dialog", u"WIFI 2.4G", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"SSID", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Contrase\u00f1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("Dialog", u"General", None))
        self.label_30.setText(QCoreApplication.translate("Dialog", u"Bater\u00eda", None))
        self.CboxBattery.setCurrentText("")
        self.CboxBattery.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetBattery.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Ethernet", None))
        self.CboxEthernet.setCurrentText("")
        self.CboxEthernet.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetEthernet.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Puerto de carga", None))
        self.CboxPlug.setCurrentText("")
        self.CboxPlug.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetPlug.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"USB", None))
        self.CboxUSB.setCurrentText("")
        self.CboxUSB.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetUSB.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Pantalla", None))
        self.CboxScreen.setCurrentText("")
        self.CboxScreen.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetScreen.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Bocinas", None))
        self.CboxSpikers.setCurrentText("")
        self.CboxSpikers.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetSpikers.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Teclado", None))
        self.CboxKeyboard.setCurrentText("")
        self.CboxKeyboard.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetKeyboard.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"C\u00e1mara", None))
        self.CboxCamera.setCurrentText("")
        self.CboxCamera.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetCamera.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Microfono", None))
        self.CboxMicro.setCurrentText("")
        self.CboxMicro.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetMicro.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_32.setText(QCoreApplication.translate("Dialog", u"Conectividad", None))
        self.CboxConnectivity.setCurrentText("")
        self.CboxConnectivity.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetConnectivity.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"TouchPad", None))
        self.CboxTouchpad.setCurrentText("")
        self.CboxTouchpad.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetTouchpad.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"TouchScreen", None))
        self.CboxTouchscreen.setCurrentText("")
        self.CboxTouchscreen.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetTouchscreen.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"Bisagras", None))
        self.CboxHinges.setCurrentText("")
        self.CboxHinges.setPlaceholderText(QCoreApplication.translate("Dialog", u"Selecciona", None))
        self.BtnResetHinges.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"Valores por defecto", None))
        self.BtnAddToSelectedPrograms.setText(QCoreApplication.translate("Dialog", u"Agregar", None))
        self.BtnDeleteFromSelectedPrograms.setText(QCoreApplication.translate("Dialog", u"Eliminar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("Dialog", u"Programas", None))
    # retranslateUi

