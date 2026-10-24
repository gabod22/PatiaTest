# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'load_panel.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_LoadPanel(object):
    def setupUi(self, LoadPanel):
        if not LoadPanel.objectName():
            LoadPanel.setObjectName(u"LoadPanel")
        self.layout = QVBoxLayout(LoadPanel)
        self.layout.setObjectName(u"layout")
        self.Intro = QLabel(LoadPanel)
        self.Intro.setObjectName(u"Intro")
        self.Intro.setWordWrap(True)

        self.layout.addWidget(self.Intro)

        self.ControlsHolder = QWidget(LoadPanel)
        self.ControlsHolder.setObjectName(u"ControlsHolder")
        self.ControlsLayout = QVBoxLayout(self.ControlsHolder)
        self.ControlsLayout.setObjectName(u"ControlsLayout")
        self.ControlsLayout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.ControlsHolder)

        self.buttons = QHBoxLayout()
        self.buttons.setObjectName(u"buttons")
        self.Start = QPushButton(LoadPanel)
        self.Start.setObjectName(u"Start")

        self.buttons.addWidget(self.Start)

        self.Apply = QPushButton(LoadPanel)
        self.Apply.setObjectName(u"Apply")

        self.buttons.addWidget(self.Apply)

        self.Stop = QPushButton(LoadPanel)
        self.Stop.setObjectName(u"Stop")

        self.buttons.addWidget(self.Stop)

        self.OpenLogs = QPushButton(LoadPanel)
        self.OpenLogs.setObjectName(u"OpenLogs")

        self.buttons.addWidget(self.OpenLogs)


        self.layout.addLayout(self.buttons)

        self.State = QLabel(LoadPanel)
        self.State.setObjectName(u"State")
        self.State.setWordWrap(True)

        self.layout.addWidget(self.State)

        self.Metrics = QLabel(LoadPanel)
        self.Metrics.setObjectName(u"Metrics")
        self.Metrics.setWordWrap(True)

        self.layout.addWidget(self.Metrics)

        self.space = QSpacerItem(10, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layout.addItem(self.space)


        self.retranslateUi(LoadPanel)

        QMetaObject.connectSlotsByName(LoadPanel)
    # setupUi

    def retranslateUi(self, LoadPanel):
        self.Intro.setText(QCoreApplication.translate("LoadPanel", u"Objetivos de uso total del equipo. El motor adapta su carga y puede ampliar los n\u00facleos iniciales. 0 % desactiva la carga generada de ese recurso.", None))
        self.Start.setText(QCoreApplication.translate("LoadPanel", u"Iniciar carga", None))
        self.Apply.setText(QCoreApplication.translate("LoadPanel", u"Aplicar cambios", None))
        self.Stop.setText(QCoreApplication.translate("LoadPanel", u"Detener carga", None))
        self.OpenLogs.setText(QCoreApplication.translate("LoadPanel", u"Abrir registros", None))
        self.State.setText(QCoreApplication.translate("LoadPanel", u"Consultando capacidades\u2026", None))
        self.Metrics.setText(QCoreApplication.translate("LoadPanel", u"Sin sesi\u00f3n activa.", None))
        pass
    # retranslateUi
