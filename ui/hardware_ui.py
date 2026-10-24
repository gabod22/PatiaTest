# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hardware.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_HardwarePanel(object):
    def setupUi(self, HardwarePanel):
        if not HardwarePanel.objectName():
            HardwarePanel.setObjectName(u"HardwarePanel")
        self.layout = QVBoxLayout(HardwarePanel)
        self.layout.setObjectName(u"layout")
        self.HardwareStatus = QLabel(HardwarePanel)
        self.HardwareStatus.setObjectName(u"HardwareStatus")
        self.HardwareStatus.setWordWrap(True)

        self.layout.addWidget(self.HardwareStatus)

        self.buttons = QHBoxLayout()
        self.buttons.setObjectName(u"buttons")
        self.RefreshHardware = QPushButton(HardwarePanel)
        self.RefreshHardware.setObjectName(u"RefreshHardware")

        self.buttons.addWidget(self.RefreshHardware)

        self.PrepareSensors = QPushButton(HardwarePanel)
        self.PrepareSensors.setObjectName(u"PrepareSensors")

        self.buttons.addWidget(self.PrepareSensors)

        self.ResetSensorHistory = QPushButton(HardwarePanel)
        self.ResetSensorHistory.setObjectName(u"ResetSensorHistory")

        self.buttons.addWidget(self.ResetSensorHistory)


        self.layout.addLayout(self.buttons)

        self.HardwareTabs = QTabWidget(HardwarePanel)
        self.HardwareTabs.setObjectName(u"HardwareTabs")
        self.BatteryDetailsTab = QWidget()
        self.BatteryDetailsTab.setObjectName(u"BatteryDetailsTab")
        self.batteryLayout = QVBoxLayout(self.BatteryDetailsTab)
        self.batteryLayout.setObjectName(u"batteryLayout")
        self.BatteryDetails = QTableWidget(self.BatteryDetailsTab)
        self.BatteryDetails.setObjectName(u"BatteryDetails")
        self.BatteryDetails.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.batteryLayout.addWidget(self.BatteryDetails)

        self.HardwareTabs.addTab(self.BatteryDetailsTab, "")
        self.DiskDetailsTab = QWidget()
        self.DiskDetailsTab.setObjectName(u"DiskDetailsTab")
        self.diskLayout = QVBoxLayout(self.DiskDetailsTab)
        self.diskLayout.setObjectName(u"diskLayout")
        self.DiskDetails = QTableWidget(self.DiskDetailsTab)
        self.DiskDetails.setObjectName(u"DiskDetails")
        self.DiskDetails.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.diskLayout.addWidget(self.DiskDetails)

        self.HardwareTabs.addTab(self.DiskDetailsTab, "")
        self.CpuDetailsTab = QWidget()
        self.CpuDetailsTab.setObjectName(u"CpuDetailsTab")
        self.cpuLayout = QVBoxLayout(self.CpuDetailsTab)
        self.cpuLayout.setObjectName(u"cpuLayout")
        self.CpuDetails = QTableWidget(self.CpuDetailsTab)
        self.CpuDetails.setObjectName(u"CpuDetails")
        self.CpuDetails.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.cpuLayout.addWidget(self.CpuDetails)

        self.HardwareTabs.addTab(self.CpuDetailsTab, "")
        self.GpuDetailsTab = QWidget()
        self.GpuDetailsTab.setObjectName(u"GpuDetailsTab")
        self.gpuLayout = QVBoxLayout(self.GpuDetailsTab)
        self.gpuLayout.setObjectName(u"gpuLayout")
        self.GpuDetails = QTableWidget(self.GpuDetailsTab)
        self.GpuDetails.setObjectName(u"GpuDetails")
        self.GpuDetails.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.gpuLayout.addWidget(self.GpuDetails)

        self.HardwareTabs.addTab(self.GpuDetailsTab, "")
        self.SensorsTab = QWidget()
        self.SensorsTab.setObjectName(u"SensorsTab")
        self.sensorsLayout = QVBoxLayout(self.SensorsTab)
        self.sensorsLayout.setObjectName(u"sensorsLayout")
        self.SensorReadings = QTableWidget(self.SensorsTab)
        self.SensorReadings.setObjectName(u"SensorReadings")
        self.SensorReadings.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.sensorsLayout.addWidget(self.SensorReadings)

        self.HardwareTabs.addTab(self.SensorsTab, "")

        self.layout.addWidget(self.HardwareTabs)


        self.retranslateUi(HardwarePanel)

        QMetaObject.connectSlotsByName(HardwarePanel)
    # setupUi

    def retranslateUi(self, HardwarePanel):
        self.HardwareStatus.setText(QCoreApplication.translate("HardwarePanel", u"Consultando hardware\u2026", None))
        self.RefreshHardware.setText(QCoreApplication.translate("HardwarePanel", u"Actualizar dispositivos", None))
        self.PrepareSensors.setText(QCoreApplication.translate("HardwarePanel", u"Preparar sensores (PawnIO)", None))
        self.ResetSensorHistory.setText(QCoreApplication.translate("HardwarePanel", u"Reiniciar m\u00ednimos/m\u00e1ximos", None))
        self.HardwareTabs.setTabText(self.HardwareTabs.indexOf(self.BatteryDetailsTab), QCoreApplication.translate("HardwarePanel", u"Bater\u00edas", None))
        self.HardwareTabs.setTabText(self.HardwareTabs.indexOf(self.DiskDetailsTab), QCoreApplication.translate("HardwarePanel", u"Discos", None))
        self.HardwareTabs.setTabText(self.HardwareTabs.indexOf(self.CpuDetailsTab), QCoreApplication.translate("HardwarePanel", u"CPU / RAM / placa", None))
        self.HardwareTabs.setTabText(self.HardwareTabs.indexOf(self.GpuDetailsTab), QCoreApplication.translate("HardwarePanel", u"GPU", None))
        self.HardwareTabs.setTabText(self.HardwareTabs.indexOf(self.SensorsTab), QCoreApplication.translate("HardwarePanel", u"Sensores", None))
        pass
    # retranslateUi
