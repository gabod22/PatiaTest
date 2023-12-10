# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loading_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPlainTextEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_LoadingDialog(object):
    def setupUi(self, LoadingDialog):
        if not LoadingDialog.objectName():
            LoadingDialog.setObjectName(u"LoadingDialog")
        LoadingDialog.setWindowModality(Qt.ApplicationModal)
        LoadingDialog.resize(449, 358)
        LoadingDialog.setSizeGripEnabled(False)
        self.verticalLayout = QVBoxLayout(LoadingDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Logo = QLabel(LoadingDialog)
        self.Logo.setObjectName(u"Logo")
        self.Logo.setPixmap(QPixmap(u"../assets/logo.png"))
        self.Logo.setScaledContents(False)
        self.Logo.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.Logo)

        self.label_2 = QLabel(LoadingDialog)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.PlainTextLog = QPlainTextEdit(LoadingDialog)
        self.PlainTextLog.setObjectName(u"PlainTextLog")

        self.verticalLayout.addWidget(self.PlainTextLog)


        self.retranslateUi(LoadingDialog)

        QMetaObject.connectSlotsByName(LoadingDialog)
    # setupUi

    def retranslateUi(self, LoadingDialog):
        LoadingDialog.setWindowTitle(QCoreApplication.translate("LoadingDialog", u"Patiatest - Cargando...", None))
        self.Logo.setText("")
        self.label_2.setText(QCoreApplication.translate("LoadingDialog", u"Cargando....", None))
    # retranslateUi

