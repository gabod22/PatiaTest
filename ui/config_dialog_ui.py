# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
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

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.SpinDefaultTestTime = QSpinBox(self.groupBox)
        self.SpinDefaultTestTime.setObjectName(u"SpinDefaultTestTime")
        self.SpinDefaultTestTime.setMaximum(999)
        self.SpinDefaultTestTime.setValue(0)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.SpinDefaultTestTime)

        self.SpinMinimunLeftOver = QSpinBox(self.groupBox)
        self.SpinMinimunLeftOver.setObjectName(u"SpinMinimunLeftOver")
        self.SpinMinimunLeftOver.setValue(0)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.SpinMinimunLeftOver)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_17.addWidget(self.scrollArea_2)

        self.tabWidget.addTab(self.tab_6, "")
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

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_5)


        self.horizontalLayout_5.addLayout(self.verticalLayout_11)

        self.ListSelectedProgrms = QListWidget(self.tab_5)
        self.ListSelectedProgrms.setObjectName(u"ListSelectedProgrms")

        self.horizontalLayout_5.addWidget(self.ListSelectedProgrms)

        self.tabWidget.addTab(self.tab_5, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.tabWidget.setCurrentIndex(0)


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
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Pruebas de bater\u00eda", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Remanente minimo (%)", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Minutos por defecto", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("Dialog", u"General", None))
        self.BtnAddToSelectedPrograms.setText(QCoreApplication.translate("Dialog", u"Agregar", None))
        self.BtnDeleteFromSelectedPrograms.setText(QCoreApplication.translate("Dialog", u"Eliminar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("Dialog", u"Programas", None))
    # retranslateUi

