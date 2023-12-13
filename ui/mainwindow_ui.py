# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFormLayout, QFrame, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(940, 752)
        icon = QIcon()
        icon.addFile(u"../../../../../.designer/assets/logo_min.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSaveLocal = QAction(MainWindow)
        self.actionSaveLocal.setObjectName(u"actionSaveLocal")
        self.actionConfig = QAction(MainWindow)
        self.actionConfig.setObjectName(u"actionConfig")
        self.actionPrograma = QAction(MainWindow)
        self.actionPrograma.setObjectName(u"actionPrograma")
        self.actionReconectar_servidor = QAction(MainWindow)
        self.actionReconectar_servidor.setObjectName(u"actionReconectar_servidor")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_19 = QVBoxLayout(self.tab_3)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.groupBox_2 = QGroupBox(self.tab_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(0, 0))
        self.groupBox_2.setMaximumSize(QSize(5000, 16777215))
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.TextModel = QLineEdit(self.groupBox_2)
        self.TextModel.setObjectName(u"TextModel")
        self.TextModel.setStyleSheet(u"background-color: rgb(222, 222, 222);")
        self.TextModel.setReadOnly(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.TextModel)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.TextServiceNumber = QLineEdit(self.groupBox_2)
        self.TextServiceNumber.setObjectName(u"TextServiceNumber")
        self.TextServiceNumber.setStyleSheet(u"background-color: rgb(222, 222, 222);")
        self.TextServiceNumber.setReadOnly(True)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.TextServiceNumber)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_6)

        self.TextBatteryHealth = QLineEdit(self.groupBox_2)
        self.TextBatteryHealth.setObjectName(u"TextBatteryHealth")
        self.TextBatteryHealth.setStyleSheet(u"background-color: rgb(222, 222, 222);")
        self.TextBatteryHealth.setReadOnly(True)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.TextBatteryHealth)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_7)

        self.TextProcessorName = QLineEdit(self.groupBox_2)
        self.TextProcessorName.setObjectName(u"TextProcessorName")
        self.TextProcessorName.setAutoFillBackground(False)
        self.TextProcessorName.setStyleSheet(u"background-color: rgb(222, 222, 222);")
        self.TextProcessorName.setReadOnly(True)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.TextProcessorName)

        self.label_34 = QLabel(self.groupBox_2)
        self.label_34.setObjectName(u"label_34")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_34)

        self.TextTotalRAM = QLineEdit(self.groupBox_2)
        self.TextTotalRAM.setObjectName(u"TextTotalRAM")
        self.TextTotalRAM.setAutoFillBackground(False)
        self.TextTotalRAM.setStyleSheet(u"background-color: rgb(222, 222, 222);")
        self.TextTotalRAM.setReadOnly(True)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.TextTotalRAM)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_4)

        self.TextBiosVersion = QLineEdit(self.groupBox_2)
        self.TextBiosVersion.setObjectName(u"TextBiosVersion")
        self.TextBiosVersion.setAutoFillBackground(False)
        self.TextBiosVersion.setStyleSheet(u"background-color: rgb(222, 222, 222);")
        self.TextBiosVersion.setReadOnly(True)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.TextBiosVersion)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.label_22 = QLabel(self.groupBox_2)
        self.label_22.setObjectName(u"label_22")

        self.verticalLayout.addWidget(self.label_22)

        self.BarCPUPercentage = QProgressBar(self.groupBox_2)
        self.BarCPUPercentage.setObjectName(u"BarCPUPercentage")
        self.BarCPUPercentage.setValue(24)

        self.verticalLayout.addWidget(self.BarCPUPercentage)

        self.label_24 = QLabel(self.groupBox_2)
        self.label_24.setObjectName(u"label_24")

        self.verticalLayout.addWidget(self.label_24)

        self.BarRAMPercentage = QProgressBar(self.groupBox_2)
        self.BarRAMPercentage.setObjectName(u"BarRAMPercentage")
        self.BarRAMPercentage.setValue(24)

        self.verticalLayout.addWidget(self.BarRAMPercentage)

        self.label_29 = QLabel(self.groupBox_2)
        self.label_29.setObjectName(u"label_29")

        self.verticalLayout.addWidget(self.label_29)

        self.BarBatteryPercentage = QProgressBar(self.groupBox_2)
        self.BarBatteryPercentage.setObjectName(u"BarBatteryPercentage")
        self.BarBatteryPercentage.setValue(24)

        self.verticalLayout.addWidget(self.BarBatteryPercentage)

        self.line_5 = QFrame(self.groupBox_2)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_5)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)


        self.horizontalLayout_5.addWidget(self.groupBox_2)

        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_27 = QLabel(self.tab_3)
        self.label_27.setObjectName(u"label_27")

        self.verticalLayout_8.addWidget(self.label_27)

        self.TableStorage = QTableWidget(self.tab_3)
        if (self.TableStorage.columnCount() < 4):
            self.TableStorage.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.TableStorage.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.TableStorage.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.TableStorage.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.TableStorage.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.TableStorage.rowCount() < 2):
            self.TableStorage.setRowCount(2)
        self.TableStorage.setObjectName(u"TableStorage")
        self.TableStorage.setAutoScrollMargin(16)
        self.TableStorage.setRowCount(2)

        self.verticalLayout_8.addWidget(self.TableStorage)


        self.verticalLayout_17.addLayout(self.verticalLayout_8)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label_41 = QLabel(self.tab_3)
        self.label_41.setObjectName(u"label_41")

        self.verticalLayout_12.addWidget(self.label_41)

        self.TableGPUs = QTableWidget(self.tab_3)
        if (self.TableGPUs.columnCount() < 2):
            self.TableGPUs.setColumnCount(2)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.TableGPUs.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.TableGPUs.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        if (self.TableGPUs.rowCount() < 2):
            self.TableGPUs.setRowCount(2)
        self.TableGPUs.setObjectName(u"TableGPUs")
        self.TableGPUs.setAutoScrollMargin(16)
        self.TableGPUs.setRowCount(2)

        self.verticalLayout_12.addWidget(self.TableGPUs)


        self.verticalLayout_17.addLayout(self.verticalLayout_12)


        self.horizontalLayout_5.addLayout(self.verticalLayout_17)


        self.verticalLayout_19.addLayout(self.horizontalLayout_5)

        self.tabWidget.addTab(self.tab_3, "")
        self.tabReport = QWidget()
        self.tabReport.setObjectName(u"tabReport")
        self.verticalLayout_16 = QVBoxLayout(self.tabReport)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.label_9 = QLabel(self.tabReport)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_15.addWidget(self.label_9)

        self.TextPixelId = QLineEdit(self.tabReport)
        self.TextPixelId.setObjectName(u"TextPixelId")
        self.TextPixelId.setMaximumSize(QSize(16777215, 16777215))
        self.TextPixelId.setAutoFillBackground(True)
        self.TextPixelId.setReadOnly(True)

        self.verticalLayout_15.addWidget(self.TextPixelId)


        self.horizontalLayout.addLayout(self.verticalLayout_15)

        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.label_31 = QLabel(self.tabReport)
        self.label_31.setObjectName(u"label_31")

        self.verticalLayout_18.addWidget(self.label_31)

        self.CboxAesthetics = QComboBox(self.tabReport)
        self.CboxAesthetics.setObjectName(u"CboxAesthetics")

        self.verticalLayout_18.addWidget(self.CboxAesthetics)


        self.horizontalLayout.addLayout(self.verticalLayout_18)

        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.label_33 = QLabel(self.tabReport)
        self.label_33.setObjectName(u"label_33")

        self.verticalLayout_20.addWidget(self.label_33)

        self.CboxCheckedBy = QComboBox(self.tabReport)
        self.CboxCheckedBy.setObjectName(u"CboxCheckedBy")
        self.CboxCheckedBy.setMinimumSize(QSize(200, 0))
        self.CboxCheckedBy.setMaximumSize(QSize(500, 16777215))

        self.verticalLayout_20.addWidget(self.CboxCheckedBy)


        self.horizontalLayout.addLayout(self.verticalLayout_20)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_16.addLayout(self.horizontalLayout)

        self.groupBox_6 = QGroupBox(self.tabReport)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(self.groupBox_6)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 876, 445))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.TextBatteryHealth_2 = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextBatteryHealth_2.setObjectName(u"TextBatteryHealth_2")
        self.TextBatteryHealth_2.setMaximumSize(QSize(300, 16777215))
        self.TextBatteryHealth_2.setStyleSheet(u"")
        self.TextBatteryHealth_2.setReadOnly(False)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.TextBatteryHealth_2)

        self.label_13 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_13.setObjectName(u"label_13")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_13)

        self.label_14 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_14.setObjectName(u"label_14")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_14)

        self.CboxPlug = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxPlug.setObjectName(u"CboxPlug")
        self.CboxPlug.setMinimumSize(QSize(150, 0))
        self.CboxPlug.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.CboxPlug)

        self.label_15 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_15.setObjectName(u"label_15")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_15)

        self.CboxUSB = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxUSB.setObjectName(u"CboxUSB")
        self.CboxUSB.setMinimumSize(QSize(150, 0))
        self.CboxUSB.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.CboxUSB)

        self.label_16 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_16.setObjectName(u"label_16")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_16)

        self.CboxScreen = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxScreen.setObjectName(u"CboxScreen")
        self.CboxScreen.setMinimumSize(QSize(150, 0))
        self.CboxScreen.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.CboxScreen)

        self.label_17 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_17.setObjectName(u"label_17")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_17)

        self.CboxSpikers = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxSpikers.setObjectName(u"CboxSpikers")
        self.CboxSpikers.setMinimumSize(QSize(150, 0))
        self.CboxSpikers.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.CboxSpikers)

        self.label_18 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_18.setObjectName(u"label_18")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_18)

        self.CboxKeyboard = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxKeyboard.setObjectName(u"CboxKeyboard")
        self.CboxKeyboard.setMinimumSize(QSize(150, 0))
        self.CboxKeyboard.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.CboxKeyboard)

        self.label_19 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_19.setObjectName(u"label_19")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_19)

        self.CboxCamera = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxCamera.setObjectName(u"CboxCamera")
        self.CboxCamera.setMinimumSize(QSize(150, 0))
        self.CboxCamera.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.CboxCamera)

        self.label_20 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_20.setObjectName(u"label_20")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_20)

        self.CboxMicro = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxMicro.setObjectName(u"CboxMicro")
        self.CboxMicro.setMinimumSize(QSize(150, 0))
        self.CboxMicro.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.CboxMicro)

        self.label_21 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_21.setObjectName(u"label_21")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.label_21)

        self.CboxTouchpad = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxTouchpad.setObjectName(u"CboxTouchpad")
        self.CboxTouchpad.setMinimumSize(QSize(150, 0))
        self.CboxTouchpad.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(11, QFormLayout.FieldRole, self.CboxTouchpad)

        self.label_25 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_25.setObjectName(u"label_25")

        self.formLayout.setWidget(12, QFormLayout.LabelRole, self.label_25)

        self.CboxTouchscreen = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxTouchscreen.setObjectName(u"CboxTouchscreen")
        self.CboxTouchscreen.setMinimumSize(QSize(150, 0))
        self.CboxTouchscreen.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(12, QFormLayout.FieldRole, self.CboxTouchscreen)

        self.label_26 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_26.setObjectName(u"label_26")

        self.formLayout.setWidget(13, QFormLayout.LabelRole, self.label_26)

        self.CboxHinges = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxHinges.setObjectName(u"CboxHinges")
        self.CboxHinges.setMinimumSize(QSize(150, 0))
        self.CboxHinges.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(13, QFormLayout.FieldRole, self.CboxHinges)

        self.CboxEthernet = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxEthernet.setObjectName(u"CboxEthernet")
        self.CboxEthernet.setMinimumSize(QSize(150, 0))
        self.CboxEthernet.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.CboxEthernet)

        self.CboxBattery = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxBattery.setObjectName(u"CboxBattery")
        self.CboxBattery.setMinimumSize(QSize(150, 0))
        self.CboxBattery.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.CboxBattery)

        self.label_30 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_30.setObjectName(u"label_30")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_30)

        self.CboxConnectivity = QComboBox(self.scrollAreaWidgetContents_2)
        self.CboxConnectivity.setObjectName(u"CboxConnectivity")
        self.CboxConnectivity.setMinimumSize(QSize(150, 0))
        self.CboxConnectivity.setMaximumSize(QSize(300, 16777215))

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.CboxConnectivity)

        self.label_32 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_32.setObjectName(u"label_32")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.label_32)

        self.label_12 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_12.setObjectName(u"label_12")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_12)


        self.horizontalLayout_3.addLayout(self.formLayout)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.TextBatteryDuration = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextBatteryDuration.setObjectName(u"TextBatteryDuration")
        self.TextBatteryDuration.setMinimumSize(QSize(0, 0))
        self.TextBatteryDuration.setClearButtonEnabled(False)

        self.verticalLayout_14.addWidget(self.TextBatteryDuration)

        self.TextBatteryNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextBatteryNote.setObjectName(u"TextBatteryNote")
        self.TextBatteryNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextBatteryNote)

        self.TextEthernetNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextEthernetNote.setObjectName(u"TextEthernetNote")
        self.TextEthernetNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextEthernetNote)

        self.TextPlugNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextPlugNote.setObjectName(u"TextPlugNote")
        self.TextPlugNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextPlugNote)

        self.TextUSBNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextUSBNote.setObjectName(u"TextUSBNote")
        self.TextUSBNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextUSBNote)

        self.TextScreenNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextScreenNote.setObjectName(u"TextScreenNote")
        self.TextScreenNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextScreenNote)

        self.TextSpikersNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextSpikersNote.setObjectName(u"TextSpikersNote")
        self.TextSpikersNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextSpikersNote)

        self.TextKeyboardNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextKeyboardNote.setObjectName(u"TextKeyboardNote")
        self.TextKeyboardNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextKeyboardNote)

        self.TextCameraNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextCameraNote.setObjectName(u"TextCameraNote")
        self.TextCameraNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextCameraNote)

        self.TextMicroNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextMicroNote.setObjectName(u"TextMicroNote")
        self.TextMicroNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextMicroNote)

        self.TextConnectivityNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextConnectivityNote.setObjectName(u"TextConnectivityNote")
        self.TextConnectivityNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextConnectivityNote)

        self.TextTouchpadNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextTouchpadNote.setObjectName(u"TextTouchpadNote")
        self.TextTouchpadNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextTouchpadNote)

        self.TextTouchscreenNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextTouchscreenNote.setObjectName(u"TextTouchscreenNote")
        self.TextTouchscreenNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextTouchscreenNote)

        self.TextHingesNote = QLineEdit(self.scrollAreaWidgetContents_2)
        self.TextHingesNote.setObjectName(u"TextHingesNote")
        self.TextHingesNote.setMinimumSize(QSize(0, 0))

        self.verticalLayout_14.addWidget(self.TextHingesNote)


        self.horizontalLayout_3.addLayout(self.verticalLayout_14)

        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.label_28 = QLabel(self.groupBox_6)
        self.label_28.setObjectName(u"label_28")

        self.verticalLayout_2.addWidget(self.label_28)

        self.PlainTextDetails = QPlainTextEdit(self.groupBox_6)
        self.PlainTextDetails.setObjectName(u"PlainTextDetails")
        self.PlainTextDetails.setMaximumSize(QSize(16777215, 50))
        self.PlainTextDetails.setTabChangesFocus(True)

        self.verticalLayout_2.addWidget(self.PlainTextDetails)

        self.BtnSaveToGoogleSheets = QPushButton(self.groupBox_6)
        self.BtnSaveToGoogleSheets.setObjectName(u"BtnSaveToGoogleSheets")
        icon1 = QIcon()
        iconThemeName = u"document-save"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u"../../../../../PatiaTest_v1/PatiaTestUI_bak", QSize(), QIcon.Normal, QIcon.Off)

        self.BtnSaveToGoogleSheets.setIcon(icon1)

        self.verticalLayout_2.addWidget(self.BtnSaveToGoogleSheets)


        self.verticalLayout_16.addWidget(self.groupBox_6)

        self.tabWidget.addTab(self.tabReport, "")
        self.tabBatteryTest = QWidget()
        self.tabBatteryTest.setObjectName(u"tabBatteryTest")
        self.horizontalLayout_2 = QHBoxLayout(self.tabBatteryTest)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox_3 = QGroupBox(self.tabBatteryTest)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(0, 0))
        self.groupBox_3.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_23 = QLabel(self.groupBox_3)
        self.label_23.setObjectName(u"label_23")

        self.verticalLayout_7.addWidget(self.label_23)

        self.BarCPUPercentage_2 = QProgressBar(self.groupBox_3)
        self.BarCPUPercentage_2.setObjectName(u"BarCPUPercentage_2")
        self.BarCPUPercentage_2.setValue(24)

        self.verticalLayout_7.addWidget(self.BarCPUPercentage_2)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_7.addWidget(self.label_8)

        self.BarBatteryPercentage_2 = QProgressBar(self.groupBox_3)
        self.BarBatteryPercentage_2.setObjectName(u"BarBatteryPercentage_2")
        self.BarBatteryPercentage_2.setValue(24)

        self.verticalLayout_7.addWidget(self.BarBatteryPercentage_2)

        self.LbBatteryStatus = QLabel(self.groupBox_3)
        self.LbBatteryStatus.setObjectName(u"LbBatteryStatus")
        font = QFont()
        font.setPointSize(11)
        self.LbBatteryStatus.setFont(font)

        self.verticalLayout_7.addWidget(self.LbBatteryStatus)

        self.LbPluggedIn = QLabel(self.groupBox_3)
        self.LbPluggedIn.setObjectName(u"LbPluggedIn")
        self.LbPluggedIn.setFont(font)

        self.verticalLayout_7.addWidget(self.LbPluggedIn)

        self.label_36 = QLabel(self.groupBox_3)
        self.label_36.setObjectName(u"label_36")

        self.verticalLayout_7.addWidget(self.label_36)

        self.LbBatteryRemain = QLabel(self.groupBox_3)
        self.LbBatteryRemain.setObjectName(u"LbBatteryRemain")
        self.LbBatteryRemain.setFont(font)

        self.verticalLayout_7.addWidget(self.LbBatteryRemain)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.LBTimeElapsed = QLabel(self.groupBox_3)
        self.LBTimeElapsed.setObjectName(u"LBTimeElapsed")
        font1 = QFont()
        font1.setPointSize(26)
        font1.setBold(False)
        self.LBTimeElapsed.setFont(font1)

        self.verticalLayout_7.addWidget(self.LBTimeElapsed)

        self.BtnStopBatteryTest = QPushButton(self.groupBox_3)
        self.BtnStopBatteryTest.setObjectName(u"BtnStopBatteryTest")
        self.BtnStopBatteryTest.setEnabled(False)

        self.verticalLayout_7.addWidget(self.BtnStopBatteryTest)

        self.BtnStartBatteryTest = QPushButton(self.groupBox_3)
        self.BtnStartBatteryTest.setObjectName(u"BtnStartBatteryTest")

        self.verticalLayout_7.addWidget(self.BtnStartBatteryTest)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_6)

        self.verticalLayout_23 = QVBoxLayout()
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.label_37 = QLabel(self.groupBox_3)
        self.label_37.setObjectName(u"label_37")

        self.verticalLayout_23.addWidget(self.label_37)

        self.CboxBatCheckedBy = QComboBox(self.groupBox_3)
        self.CboxBatCheckedBy.setObjectName(u"CboxBatCheckedBy")
        self.CboxBatCheckedBy.setMaximumSize(QSize(500, 16777215))

        self.verticalLayout_23.addWidget(self.CboxBatCheckedBy)


        self.verticalLayout_7.addLayout(self.verticalLayout_23)

        self.ChkBoxSaveAtEnd = QCheckBox(self.groupBox_3)
        self.ChkBoxSaveAtEnd.setObjectName(u"ChkBoxSaveAtEnd")

        self.verticalLayout_7.addWidget(self.ChkBoxSaveAtEnd)

        self.BtnSaveBatteryRecord = QPushButton(self.groupBox_3)
        self.BtnSaveBatteryRecord.setObjectName(u"BtnSaveBatteryRecord")

        self.verticalLayout_7.addWidget(self.BtnSaveBatteryRecord)


        self.horizontalLayout_2.addWidget(self.groupBox_3)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.groupBox_4 = QGroupBox(self.tabBatteryTest)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.TableBatteryInfo = QTableWidget(self.groupBox_4)
        if (self.TableBatteryInfo.columnCount() < 5):
            self.TableBatteryInfo.setColumnCount(5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.TableBatteryInfo.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        if (self.TableBatteryInfo.rowCount() < 8):
            self.TableBatteryInfo.setRowCount(8)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(2, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(3, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(4, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(5, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(6, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(7, __qtablewidgetitem14)
        self.TableBatteryInfo.setObjectName(u"TableBatteryInfo")
        self.TableBatteryInfo.setEnabled(True)
        self.TableBatteryInfo.setAutoScrollMargin(16)
        self.TableBatteryInfo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.TableBatteryInfo.setColumnCount(5)

        self.verticalLayout_5.addWidget(self.TableBatteryInfo)


        self.verticalLayout_13.addWidget(self.groupBox_4)

        self.groupBox = QGroupBox(self.tabBatteryTest)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.TableBatteryLog = QTableWidget(self.groupBox)
        if (self.TableBatteryLog.columnCount() < 4):
            self.TableBatteryLog.setColumnCount(4)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.TableBatteryLog.setHorizontalHeaderItem(0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.TableBatteryLog.setHorizontalHeaderItem(1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.TableBatteryLog.setHorizontalHeaderItem(2, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.TableBatteryLog.setHorizontalHeaderItem(3, __qtablewidgetitem18)
        self.TableBatteryLog.setObjectName(u"TableBatteryLog")
        self.TableBatteryLog.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_4.addWidget(self.TableBatteryLog)


        self.verticalLayout_13.addWidget(self.groupBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_13)

        self.tabWidget.addTab(self.tabBatteryTest, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.horizontalLayout_6 = QHBoxLayout(self.tab_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.groupBox_7 = QGroupBox(self.tab_4)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.BtnOpenPrograms = QPushButton(self.groupBox_7)
        self.BtnOpenPrograms.setObjectName(u"BtnOpenPrograms")

        self.verticalLayout_6.addWidget(self.BtnOpenPrograms)

        self.BtnTestTouchscreen = QPushButton(self.groupBox_7)
        self.BtnTestTouchscreen.setObjectName(u"BtnTestTouchscreen")

        self.verticalLayout_6.addWidget(self.BtnTestTouchscreen)

        self.BtnStopTestSpeakers = QPushButton(self.groupBox_7)
        self.BtnStopTestSpeakers.setObjectName(u"BtnStopTestSpeakers")
        self.BtnStopTestSpeakers.setEnabled(True)

        self.verticalLayout_6.addWidget(self.BtnStopTestSpeakers)

        self.BtnTestSpeakers = QPushButton(self.groupBox_7)
        self.BtnTestSpeakers.setObjectName(u"BtnTestSpeakers")

        self.verticalLayout_6.addWidget(self.BtnTestSpeakers)

        self.BtnTestCamera = QPushButton(self.groupBox_7)
        self.BtnTestCamera.setObjectName(u"BtnTestCamera")

        self.verticalLayout_6.addWidget(self.BtnTestCamera)

        self.BtnTestMicrophone = QPushButton(self.groupBox_7)
        self.BtnTestMicrophone.setObjectName(u"BtnTestMicrophone")

        self.verticalLayout_6.addWidget(self.BtnTestMicrophone)

        self.BtnTestKeyboard = QPushButton(self.groupBox_7)
        self.BtnTestKeyboard.setObjectName(u"BtnTestKeyboard")

        self.verticalLayout_6.addWidget(self.BtnTestKeyboard)

        self.BtnTestScreen = QPushButton(self.groupBox_7)
        self.BtnTestScreen.setObjectName(u"BtnTestScreen")

        self.verticalLayout_6.addWidget(self.BtnTestScreen)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_4)


        self.horizontalLayout_6.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.tab_4)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_22 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.BtnStartCameraCapture = QPushButton(self.groupBox_8)
        self.BtnStartCameraCapture.setObjectName(u"BtnStartCameraCapture")

        self.verticalLayout_22.addWidget(self.BtnStartCameraCapture)

        self.BtnStopCameraCapture = QPushButton(self.groupBox_8)
        self.BtnStopCameraCapture.setObjectName(u"BtnStopCameraCapture")

        self.verticalLayout_22.addWidget(self.BtnStopCameraCapture)

        self.CameraLabel = QLabel(self.groupBox_8)
        self.CameraLabel.setObjectName(u"CameraLabel")

        self.verticalLayout_22.addWidget(self.CameraLabel)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_5)

        self.LbRecordAudio = QLabel(self.groupBox_8)
        self.LbRecordAudio.setObjectName(u"LbRecordAudio")

        self.verticalLayout_22.addWidget(self.LbRecordAudio)

        self.BtnRecordAudio = QPushButton(self.groupBox_8)
        self.BtnRecordAudio.setObjectName(u"BtnRecordAudio")

        self.verticalLayout_22.addWidget(self.BtnRecordAudio)

        self.BtnPlayAudio = QPushButton(self.groupBox_8)
        self.BtnPlayAudio.setObjectName(u"BtnPlayAudio")

        self.verticalLayout_22.addWidget(self.BtnPlayAudio)

        self.BtnStopAudio = QPushButton(self.groupBox_8)
        self.BtnStopAudio.setObjectName(u"BtnStopAudio")
        self.BtnStopAudio.setEnabled(True)

        self.verticalLayout_22.addWidget(self.BtnStopAudio)


        self.horizontalLayout_6.addWidget(self.groupBox_8)

        self.tabWidget.addTab(self.tab_4, "")

        self.horizontalLayout_4.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 940, 22))
        self.menuConfiguraci_n = QMenu(self.menubar)
        self.menuConfiguraci_n.setObjectName(u"menuConfiguraci_n")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuConfiguraci_n.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menuConfiguraci_n.addAction(self.actionSave)
        self.menuConfiguraci_n.addAction(self.actionSaveLocal)
        self.menuConfiguraci_n.addSeparator()
        self.menuConfiguraci_n.addAction(self.actionConfig)
        self.menuConfiguraci_n.addAction(self.actionReconectar_servidor)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(3)
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
        self.CboxEthernet.setCurrentIndex(-1)
        self.CboxBattery.setCurrentIndex(-1)
        self.CboxConnectivity.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Patiatest", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Guardar", None))
        self.actionSaveLocal.setText(QCoreApplication.translate("MainWindow", u"Guardar local", None))
        self.actionConfig.setText(QCoreApplication.translate("MainWindow", u"Configuraci\u00f3n", None))
        self.actionPrograma.setText(QCoreApplication.translate("MainWindow", u"Programa", None))
        self.actionReconectar_servidor.setText(QCoreApplication.translate("MainWindow", u"Reconectar servidor", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Info del pc", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Modelo", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"No. Servicio", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Salud de bater\u00eda", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Procesador", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"RAM", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"BIOS", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"CPU", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"RAM", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Bater\u00eda", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Unidades de almacenamiento", None))
        ___qtablewidgetitem = self.TableStorage.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Nombre", None));
        ___qtablewidgetitem1 = self.TableStorage.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Interfaz", None));
        ___qtablewidgetitem2 = self.TableStorage.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Capacidad", None));
        ___qtablewidgetitem3 = self.TableStorage.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"GPUs", None))
        ___qtablewidgetitem4 = self.TableGPUs.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Nombre", None));
        ___qtablewidgetitem5 = self.TableGPUs.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Capacidad", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Informaci\u00f3n del equipo", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"PIXEL ID", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Est\u00e9tica", None))
        self.CboxAesthetics.setPlaceholderText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Revisado por:", None))
        self.CboxCheckedBy.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona el t\u00e9cnico", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Reporte", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Ethernet", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Puerto de carga", None))
        self.CboxPlug.setCurrentText("")
        self.CboxPlug.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"USB", None))
        self.CboxUSB.setCurrentText("")
        self.CboxUSB.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Pantalla", None))
        self.CboxScreen.setCurrentText("")
        self.CboxScreen.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Bocinas", None))
        self.CboxSpikers.setCurrentText("")
        self.CboxSpikers.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Teclado", None))
        self.CboxKeyboard.setCurrentText("")
        self.CboxKeyboard.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"C\u00e1mara", None))
        self.CboxCamera.setCurrentText("")
        self.CboxCamera.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Microfono", None))
        self.CboxMicro.setCurrentText("")
        self.CboxMicro.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"TouchPad", None))
        self.CboxTouchpad.setCurrentText("")
        self.CboxTouchpad.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"TouchScreen", None))
        self.CboxTouchscreen.setCurrentText("")
        self.CboxTouchscreen.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Bisagras", None))
        self.CboxHinges.setCurrentText("")
        self.CboxHinges.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.CboxEthernet.setCurrentText("")
        self.CboxEthernet.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.CboxBattery.setCurrentText("")
        self.CboxBattery.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Bater\u00eda", None))
        self.CboxConnectivity.setCurrentText("")
        self.CboxConnectivity.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Conectividad", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Salud de bater\u00eda", None))
        self.TextBatteryDuration.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Duraci\u00f3n de la bater\u00eda...", None))
        self.TextBatteryNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.TextEthernetNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.TextPlugNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.TextUSBNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.TextScreenNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.TextSpikersNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.TextKeyboardNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.TextCameraNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.TextMicroNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.TextConnectivityNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.TextTouchpadNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.TextTouchscreenNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.TextHingesNote.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nota...", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Detalles", None))
        self.BtnSaveToGoogleSheets.setText(QCoreApplication.translate("MainWindow", u"Guardar reporte", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabReport), QCoreApplication.translate("MainWindow", u"Reporte", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Estado general", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"CPU", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Bater\u00eda", None))
        self.LbBatteryStatus.setText(QCoreApplication.translate("MainWindow", u"LbBatteryStatus", None))
        self.LbPluggedIn.setText(QCoreApplication.translate("MainWindow", u"LbPluggedIn", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Tiempo restante con carga total", None))
        self.LbBatteryRemain.setText(QCoreApplication.translate("MainWindow", u"LBBatteryRemain", None))
        self.LBTimeElapsed.setText(QCoreApplication.translate("MainWindow", u"No iniciado", None))
        self.BtnStopBatteryTest.setText(QCoreApplication.translate("MainWindow", u"Detener prueba de bater\u00eda", None))
        self.BtnStartBatteryTest.setText(QCoreApplication.translate("MainWindow", u"Iniciar prueba de bater\u00eda", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Revisado por:", None))
        self.CboxBatCheckedBy.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Selecciona el t\u00e9cnico", None))
        self.ChkBoxSaveAtEnd.setText(QCoreApplication.translate("MainWindow", u"\u00bfGuardar al terminar?", None))
        self.BtnSaveBatteryRecord.setText(QCoreApplication.translate("MainWindow", u"Guardar prueba", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Bater\u00edas", None))
        ___qtablewidgetitem6 = self.TableBatteryInfo.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem7 = self.TableBatteryInfo.verticalHeaderItem(0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Battery name", None));
        ___qtablewidgetitem8 = self.TableBatteryInfo.verticalHeaderItem(1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Manufacture Name", None));
        ___qtablewidgetitem9 = self.TableBatteryInfo.verticalHeaderItem(2)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Manufacture Date", None));
        ___qtablewidgetitem10 = self.TableBatteryInfo.verticalHeaderItem(3)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Serial Number", None));
        ___qtablewidgetitem11 = self.TableBatteryInfo.verticalHeaderItem(4)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Full Charged Capacity", None));
        ___qtablewidgetitem12 = self.TableBatteryInfo.verticalHeaderItem(5)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Designed Capacity", None));
        ___qtablewidgetitem13 = self.TableBatteryInfo.verticalHeaderItem(6)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Battery Health", None));
        ___qtablewidgetitem14 = self.TableBatteryInfo.verticalHeaderItem(7)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Cycles", None));
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Historial", None))
        ___qtablewidgetitem15 = self.TableBatteryLog.horizontalHeaderItem(0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Fecha", None));
        ___qtablewidgetitem16 = self.TableBatteryLog.horizontalHeaderItem(1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Porcentaje", None));
        ___qtablewidgetitem17 = self.TableBatteryLog.horizontalHeaderItem(2)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Cargador", None));
        ___qtablewidgetitem18 = self.TableBatteryLog.horizontalHeaderItem(3)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"CPU(%)", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBatteryTest), QCoreApplication.translate("MainWindow", u"Revisi\u00f3n de bater\u00eda", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Probar el equipo", None))
        self.BtnOpenPrograms.setText(QCoreApplication.translate("MainWindow", u"Abrir programas", None))
        self.BtnTestTouchscreen.setText(QCoreApplication.translate("MainWindow", u"Touchscreen", None))
        self.BtnStopTestSpeakers.setText(QCoreApplication.translate("MainWindow", u"Detener Sonido", None))
        self.BtnTestSpeakers.setText(QCoreApplication.translate("MainWindow", u"Reproducir sonido", None))
        self.BtnTestCamera.setText(QCoreApplication.translate("MainWindow", u"Abrir c\u00e1mara", None))
        self.BtnTestMicrophone.setText(QCoreApplication.translate("MainWindow", u"Abrir configuracion micro", None))
        self.BtnTestKeyboard.setText(QCoreApplication.translate("MainWindow", u"Teclado", None))
        self.BtnTestScreen.setText(QCoreApplication.translate("MainWindow", u"Pantalla", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Programas", None))
        self.BtnStartCameraCapture.setText(QCoreApplication.translate("MainWindow", u"Probar c\u00e1mara", None))
        self.BtnStopCameraCapture.setText(QCoreApplication.translate("MainWindow", u"Detener", None))
        self.CameraLabel.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.LbRecordAudio.setText("")
        self.BtnRecordAudio.setText(QCoreApplication.translate("MainWindow", u"Grabar microfono", None))
        self.BtnPlayAudio.setText(QCoreApplication.translate("MainWindow", u"Reproducir grabaci\u00f3n", None))
        self.BtnStopAudio.setText(QCoreApplication.translate("MainWindow", u"Detener audio", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Herramientas", None))
        self.menuConfiguraci_n.setTitle(QCoreApplication.translate("MainWindow", u"Archivo", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Herramientas", None))
    # retranslateUi

