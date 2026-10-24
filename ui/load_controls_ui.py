# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'load_controls.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpinBox, QWidget)

class Ui_LoadControls(object):
    def setupUi(self, LoadControls):
        if not LoadControls.objectName():
            LoadControls.setObjectName(u"LoadControls")
        self.form = QFormLayout(LoadControls)
        self.form.setObjectName(u"form")
        self.profileLabel = QLabel(LoadControls)
        self.profileLabel.setObjectName(u"profileLabel")

        self.form.setWidget(0, QFormLayout.LabelRole, self.profileLabel)

        self.Profile = QComboBox(LoadControls)
        self.Profile.setObjectName(u"Profile")

        self.form.setWidget(0, QFormLayout.FieldRole, self.Profile)

        self.cpuLabel = QLabel(LoadControls)
        self.cpuLabel.setObjectName(u"cpuLabel")

        self.form.setWidget(1, QFormLayout.LabelRole, self.cpuLabel)

        self.CpuTarget = QComboBox(LoadControls)
        self.CpuTarget.setObjectName(u"CpuTarget")
        self.CpuTarget.setEditable(True)

        self.form.setWidget(1, QFormLayout.FieldRole, self.CpuTarget)

        self.coresLabel = QLabel(LoadControls)
        self.coresLabel.setObjectName(u"coresLabel")

        self.form.setWidget(2, QFormLayout.LabelRole, self.coresLabel)

        self.Cores = QComboBox(LoadControls)
        self.Cores.setObjectName(u"Cores")

        self.form.setWidget(2, QFormLayout.FieldRole, self.Cores)

        self.gpuLabel = QLabel(LoadControls)
        self.gpuLabel.setObjectName(u"gpuLabel")

        self.form.setWidget(3, QFormLayout.LabelRole, self.gpuLabel)

        self.GpuTarget = QComboBox(LoadControls)
        self.GpuTarget.setObjectName(u"GpuTarget")
        self.GpuTarget.setEditable(True)

        self.form.setWidget(3, QFormLayout.FieldRole, self.GpuTarget)

        self.adapterLabel = QLabel(LoadControls)
        self.adapterLabel.setObjectName(u"adapterLabel")

        self.form.setWidget(4, QFormLayout.LabelRole, self.adapterLabel)

        self.Adapter = QComboBox(LoadControls)
        self.Adapter.setObjectName(u"Adapter")

        self.form.setWidget(4, QFormLayout.FieldRole, self.Adapter)

        self.limitsLabel = QLabel(LoadControls)
        self.limitsLabel.setObjectName(u"limitsLabel")

        self.form.setWidget(5, QFormLayout.LabelRole, self.limitsLabel)

        self.limits = QHBoxLayout()
        self.limits.setObjectName(u"limits")
        self.CpuLimit = QSpinBox(LoadControls)
        self.CpuLimit.setObjectName(u"CpuLimit")
        self.CpuLimit.setMinimum(40)
        self.CpuLimit.setMaximum(110)
        self.CpuLimit.setValue(95)

        self.limits.addWidget(self.CpuLimit)

        self.GpuLimit = QSpinBox(LoadControls)
        self.GpuLimit.setObjectName(u"GpuLimit")
        self.GpuLimit.setMinimum(40)
        self.GpuLimit.setMaximum(110)
        self.GpuLimit.setValue(90)

        self.limits.addWidget(self.GpuLimit)


        self.form.setLayout(5, QFormLayout.FieldRole, self.limits)


        self.retranslateUi(LoadControls)

        QMetaObject.connectSlotsByName(LoadControls)
    # setupUi

    def retranslateUi(self, LoadControls):
        self.profileLabel.setText(QCoreApplication.translate("LoadControls", u"Perfil", None))
        self.cpuLabel.setText(QCoreApplication.translate("LoadControls", u"CPU objetivo (%)", None))
        self.coresLabel.setText(QCoreApplication.translate("LoadControls", u"N\u00facleos iniciales", None))
        self.gpuLabel.setText(QCoreApplication.translate("LoadControls", u"GPU objetivo (%)", None))
        self.adapterLabel.setText(QCoreApplication.translate("LoadControls", u"Adaptador GPU", None))
        self.limitsLabel.setText(QCoreApplication.translate("LoadControls", u"L\u00edmite CPU / GPU (\u00b0C)", None))
        pass
    # retranslateUi
