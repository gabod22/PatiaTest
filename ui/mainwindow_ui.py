# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(874, 729)
        icon = QIcon()
        icon.addFile(u"C:/Users/brian/.designer/assets/logo_min.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
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
        self.verticalLayout_10 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.horizontalLayout_5 = QHBoxLayout(self.tab_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.groupBox_2 = QGroupBox(self.tab_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(0, 0))
        self.groupBox_2.setMaximumSize(QSize(5000, 16777215))
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.TextWinver = QLineEdit(self.groupBox_2)
        self.TextWinver.setObjectName(u"TextWinver")
        self.TextWinver.setStyleSheet(u"background-color: rgb(222, 222, 222);\n"
"color:rgb(0,0,0)")
        self.TextWinver.setReadOnly(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.TextWinver)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.TextModel = QLineEdit(self.groupBox_2)
        self.TextModel.setObjectName(u"TextModel")
        self.TextModel.setStyleSheet(u"background-color: rgb(222, 222, 222);\n"
"color:rgb(0,0,0)")
        self.TextModel.setReadOnly(True)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.TextModel)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.TextServiceNumber = QLineEdit(self.groupBox_2)
        self.TextServiceNumber.setObjectName(u"TextServiceNumber")
        self.TextServiceNumber.setStyleSheet(u"background-color: rgb(222, 222, 222);\n"
"color: rgb(0,0,0)\n"
"")
        self.TextServiceNumber.setReadOnly(True)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.TextServiceNumber)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_6)

        self.TextBatteryHealth = QLineEdit(self.groupBox_2)
        self.TextBatteryHealth.setObjectName(u"TextBatteryHealth")
        self.TextBatteryHealth.setStyleSheet(u"background-color: rgb(222, 222, 222);\n"
"color: rgb(0,0,0)\n"
"")
        self.TextBatteryHealth.setReadOnly(True)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.TextBatteryHealth)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_7)

        self.label_34 = QLabel(self.groupBox_2)
        self.label_34.setObjectName(u"label_34")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_34)

        self.TextTotalRAM = QLineEdit(self.groupBox_2)
        self.TextTotalRAM.setObjectName(u"TextTotalRAM")
        self.TextTotalRAM.setAutoFillBackground(False)
        self.TextTotalRAM.setStyleSheet(u"background-color: rgb(222, 222, 222);\n"
"color: rgb(0,0,0)\n"
"")
        self.TextTotalRAM.setReadOnly(True)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.TextTotalRAM)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_4)

        self.TextBiosVersion = QLineEdit(self.groupBox_2)
        self.TextBiosVersion.setObjectName(u"TextBiosVersion")
        self.TextBiosVersion.setAutoFillBackground(False)
        self.TextBiosVersion.setStyleSheet(u"background-color: rgb(222, 222, 222);\n"
"color: rgb(0,0,0)\n"
"")
        self.TextBiosVersion.setReadOnly(True)

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.TextBiosVersion)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.TextProcessorName = QLineEdit(self.groupBox_2)
        self.TextProcessorName.setObjectName(u"TextProcessorName")
        self.TextProcessorName.setAutoFillBackground(False)
        self.TextProcessorName.setStyleSheet(u"background-color: rgb(222, 222, 222);\n"
"color: rgb(0,0,0)\n"
"")
        self.TextProcessorName.setReadOnly(True)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.TextProcessorName)


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
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_5)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.PixelLapLogo = QLabel(self.groupBox_2)
        self.PixelLapLogo.setObjectName(u"PixelLapLogo")

        self.verticalLayout.addWidget(self.PixelLapLogo)


        self.horizontalLayout_5.addWidget(self.groupBox_2)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_27 = QLabel(self.tab_3)
        self.label_27.setObjectName(u"label_27")

        self.verticalLayout_8.addWidget(self.label_27)

        self.TableStorage = QTableWidget(self.tab_3)
        if (self.TableStorage.columnCount() < 5):
            self.TableStorage.setColumnCount(5)
        if (self.TableStorage.rowCount() < 8):
            self.TableStorage.setRowCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.TableStorage.setVerticalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.TableStorage.setVerticalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.TableStorage.setVerticalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.TableStorage.setVerticalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.TableStorage.setVerticalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.TableStorage.setVerticalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.TableStorage.setVerticalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.TableStorage.setVerticalHeaderItem(7, __qtablewidgetitem7)
        self.TableStorage.setObjectName(u"TableStorage")
        self.TableStorage.setEnabled(True)
        self.TableStorage.setAutoScrollMargin(16)
        self.TableStorage.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.TableStorage.setColumnCount(5)

        self.verticalLayout_8.addWidget(self.TableStorage)


        self.verticalLayout_9.addLayout(self.verticalLayout_8)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label_41 = QLabel(self.tab_3)
        self.label_41.setObjectName(u"label_41")

        self.verticalLayout_12.addWidget(self.label_41)

        self.TableGPUs = QTableWidget(self.tab_3)
        if (self.TableGPUs.columnCount() < 4):
            self.TableGPUs.setColumnCount(4)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.TableGPUs.setHorizontalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.TableGPUs.setHorizontalHeaderItem(1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.TableGPUs.setHorizontalHeaderItem(2, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.TableGPUs.setHorizontalHeaderItem(3, __qtablewidgetitem11)
        if (self.TableGPUs.rowCount() < 2):
            self.TableGPUs.setRowCount(2)
        self.TableGPUs.setObjectName(u"TableGPUs")
        self.TableGPUs.setAutoScrollMargin(16)
        self.TableGPUs.setRowCount(2)

        self.verticalLayout_12.addWidget(self.TableGPUs)


        self.verticalLayout_9.addLayout(self.verticalLayout_12)


        self.horizontalLayout_5.addLayout(self.verticalLayout_9)

        self.tabWidget.addTab(self.tab_3, "")
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

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.LBTimeElapsed = QLabel(self.groupBox_3)
        self.LBTimeElapsed.setObjectName(u"LBTimeElapsed")
        font1 = QFont()
        font1.setPointSize(26)
        font1.setBold(False)
        self.LBTimeElapsed.setFont(font1)

        self.verticalLayout_7.addWidget(self.LBTimeElapsed)

        self.CbxBetteryTestType = QComboBox(self.groupBox_3)
        self.CbxBetteryTestType.addItem("")
        self.CbxBetteryTestType.addItem("")
        self.CbxBetteryTestType.addItem("")
        self.CbxBetteryTestType.setObjectName(u"CbxBetteryTestType")

        self.verticalLayout_7.addWidget(self.CbxBetteryTestType)

        self.lbMinutestime = QLabel(self.groupBox_3)
        self.lbMinutestime.setObjectName(u"lbMinutestime")

        self.verticalLayout_7.addWidget(self.lbMinutestime)

        self.SpinTimeToTest = QSpinBox(self.groupBox_3)
        self.SpinTimeToTest.setObjectName(u"SpinTimeToTest")
        self.SpinTimeToTest.setMinimum(1)
        self.SpinTimeToTest.setMaximum(9999)
        self.SpinTimeToTest.setSingleStep(10)
        self.SpinTimeToTest.setValue(120)

        self.verticalLayout_7.addWidget(self.SpinTimeToTest)

        self.BtnStopBatteryTest = QPushButton(self.groupBox_3)
        self.BtnStopBatteryTest.setObjectName(u"BtnStopBatteryTest")
        self.BtnStopBatteryTest.setEnabled(False)

        self.verticalLayout_7.addWidget(self.BtnStopBatteryTest)

        self.BtnStartBatteryTest = QPushButton(self.groupBox_3)
        self.BtnStartBatteryTest.setObjectName(u"BtnStartBatteryTest")

        self.verticalLayout_7.addWidget(self.BtnStartBatteryTest)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_6)

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
        __qtablewidgetitem12 = QTableWidgetItem()
        self.TableBatteryInfo.setHorizontalHeaderItem(0, __qtablewidgetitem12)
        if (self.TableBatteryInfo.rowCount() < 8):
            self.TableBatteryInfo.setRowCount(8)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(0, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(1, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(2, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(3, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(4, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(5, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(6, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.TableBatteryInfo.setVerticalHeaderItem(7, __qtablewidgetitem20)
        self.TableBatteryInfo.setObjectName(u"TableBatteryInfo")
        self.TableBatteryInfo.setEnabled(True)
        self.TableBatteryInfo.setAutoScrollMargin(16)
        self.TableBatteryInfo.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
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
        __qtablewidgetitem21 = QTableWidgetItem()
        self.TableBatteryLog.setHorizontalHeaderItem(0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.TableBatteryLog.setHorizontalHeaderItem(1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.TableBatteryLog.setHorizontalHeaderItem(2, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.TableBatteryLog.setHorizontalHeaderItem(3, __qtablewidgetitem24)
        self.TableBatteryLog.setObjectName(u"TableBatteryLog")
        self.TableBatteryLog.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

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

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_4)


        self.horizontalLayout_6.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.tab_4)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.BtnStartCameraCapture = QPushButton(self.groupBox_8)
        self.BtnStartCameraCapture.setObjectName(u"BtnStartCameraCapture")

        self.verticalLayout_17.addWidget(self.BtnStartCameraCapture)

        self.BtnStopCameraCapture = QPushButton(self.groupBox_8)
        self.BtnStopCameraCapture.setObjectName(u"BtnStopCameraCapture")

        self.verticalLayout_17.addWidget(self.BtnStopCameraCapture)

        self.BtnSwitchCamera = QPushButton(self.groupBox_8)
        self.BtnSwitchCamera.setObjectName(u"BtnSwitchCamera")

        self.verticalLayout_17.addWidget(self.BtnSwitchCamera)

        self.CameraLabel = QLabel(self.groupBox_8)
        self.CameraLabel.setObjectName(u"CameraLabel")

        self.verticalLayout_17.addWidget(self.CameraLabel)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_5)

        self.LbRecordAudio = QLabel(self.groupBox_8)
        self.LbRecordAudio.setObjectName(u"LbRecordAudio")

        self.verticalLayout_17.addWidget(self.LbRecordAudio)

        self.BtnRecordAudio = QPushButton(self.groupBox_8)
        self.BtnRecordAudio.setObjectName(u"BtnRecordAudio")

        self.verticalLayout_17.addWidget(self.BtnRecordAudio)

        self.BtnPlayAudio = QPushButton(self.groupBox_8)
        self.BtnPlayAudio.setObjectName(u"BtnPlayAudio")

        self.verticalLayout_17.addWidget(self.BtnPlayAudio)

        self.BtnStopAudio = QPushButton(self.groupBox_8)
        self.BtnStopAudio.setObjectName(u"BtnStopAudio")
        self.BtnStopAudio.setEnabled(True)

        self.verticalLayout_17.addWidget(self.BtnStopAudio)


        self.horizontalLayout_6.addWidget(self.groupBox_8)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_11 = QVBoxLayout(self.tab)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.LBQrCode = QLabel(self.tab)
        self.LBQrCode.setObjectName(u"LBQrCode")
        self.LBQrCode.setScaledContents(False)

        self.verticalLayout_11.addWidget(self.LBQrCode)

        self.tabWidget.addTab(self.tab, "")

        self.verticalLayout_10.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 874, 33))
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
        self.menuConfiguraci_n.addAction(self.actionConfig)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Pixel-lap - PixelTest", None))
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
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Versi\u00f3n de windows", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"CPU", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"RAM", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Bater\u00eda", None))
        self.PixelLapLogo.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Unidades de almacenamiento", None))
        ___qtablewidgetitem = self.TableStorage.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Modelo", None));
        ___qtablewidgetitem1 = self.TableStorage.verticalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Capacidad", None));
        ___qtablewidgetitem2 = self.TableStorage.verticalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Salud", None));
        ___qtablewidgetitem3 = self.TableStorage.verticalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Interfaz", None));
        ___qtablewidgetitem4 = self.TableStorage.verticalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"N\u00b0 de lecturas", None));
        ___qtablewidgetitem5 = self.TableStorage.verticalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"N\u00b0 de escrituras", None));
        ___qtablewidgetitem6 = self.TableStorage.verticalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"N\u00b0 de encendidos", None));
        ___qtablewidgetitem7 = self.TableStorage.verticalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Horas de encendido", None));
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"GPUs", None))
        ___qtablewidgetitem8 = self.TableGPUs.horizontalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Nombre", None));
        ___qtablewidgetitem9 = self.TableGPUs.horizontalHeaderItem(1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Fabricante", None));
        ___qtablewidgetitem10 = self.TableGPUs.horizontalHeaderItem(2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Capacidad", None));
        ___qtablewidgetitem11 = self.TableGPUs.horizontalHeaderItem(3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Tipo memoria", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Informaci\u00f3n del equipo", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Estado general", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"CPU", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Bater\u00eda", None))
        self.LbBatteryStatus.setText(QCoreApplication.translate("MainWindow", u"LbBatteryStatus", None))
        self.LbPluggedIn.setText(QCoreApplication.translate("MainWindow", u"LbPluggedIn", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Tiempo restante con carga total", None))
        self.LbBatteryRemain.setText(QCoreApplication.translate("MainWindow", u"LBBatteryRemain", None))
        self.LBTimeElapsed.setText(QCoreApplication.translate("MainWindow", u"No iniciado", None))
        self.CbxBetteryTestType.setItemText(0, QCoreApplication.translate("MainWindow", u"Por tiempo", None))
        self.CbxBetteryTestType.setItemText(1, QCoreApplication.translate("MainWindow", u"Intensiva", None))
        self.CbxBetteryTestType.setItemText(2, QCoreApplication.translate("MainWindow", u"Exaustiva", None))

        self.lbMinutestime.setText(QCoreApplication.translate("MainWindow", u"Minutos de duraci\u00f3n", None))
        self.BtnStopBatteryTest.setText(QCoreApplication.translate("MainWindow", u"Detener prueba de bater\u00eda", None))
        self.BtnStartBatteryTest.setText(QCoreApplication.translate("MainWindow", u"Iniciar prueba de bater\u00eda", None))
        self.BtnSaveBatteryRecord.setText(QCoreApplication.translate("MainWindow", u"QR ", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Bater\u00edas", None))
        ___qtablewidgetitem12 = self.TableBatteryInfo.horizontalHeaderItem(0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem13 = self.TableBatteryInfo.verticalHeaderItem(0)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Battery name", None));
        ___qtablewidgetitem14 = self.TableBatteryInfo.verticalHeaderItem(1)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Manufacture Name", None));
        ___qtablewidgetitem15 = self.TableBatteryInfo.verticalHeaderItem(2)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Manufacture Date", None));
        ___qtablewidgetitem16 = self.TableBatteryInfo.verticalHeaderItem(3)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Serial Number", None));
        ___qtablewidgetitem17 = self.TableBatteryInfo.verticalHeaderItem(4)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Full Charged Capacity", None));
        ___qtablewidgetitem18 = self.TableBatteryInfo.verticalHeaderItem(5)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Designed Capacity", None));
        ___qtablewidgetitem19 = self.TableBatteryInfo.verticalHeaderItem(6)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Battery Health", None));
        ___qtablewidgetitem20 = self.TableBatteryInfo.verticalHeaderItem(7)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Cycles", None));
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Historial", None))
        ___qtablewidgetitem21 = self.TableBatteryLog.horizontalHeaderItem(0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Fecha", None));
        ___qtablewidgetitem22 = self.TableBatteryLog.horizontalHeaderItem(1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Porcentaje", None));
        ___qtablewidgetitem23 = self.TableBatteryLog.horizontalHeaderItem(2)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Cargador", None));
        ___qtablewidgetitem24 = self.TableBatteryLog.horizontalHeaderItem(3)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"CPU(%)", None));
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
        self.BtnSwitchCamera.setText(QCoreApplication.translate("MainWindow", u"Cambiar c\u00e1mara", None))
        self.CameraLabel.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.LbRecordAudio.setText("")
        self.BtnRecordAudio.setText(QCoreApplication.translate("MainWindow", u"Grabar microfono", None))
        self.BtnPlayAudio.setText(QCoreApplication.translate("MainWindow", u"Reproducir grabaci\u00f3n", None))
        self.BtnStopAudio.setText(QCoreApplication.translate("MainWindow", u"Detener audio", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Herramientas", None))
        self.LBQrCode.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"C\u00f3digo QR", None))
        self.menuConfiguraci_n.setTitle(QCoreApplication.translate("MainWindow", u"Archivo", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Herramientas", None))
    # retranslateUi

