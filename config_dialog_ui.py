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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QRadioButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(574, 444)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_2 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ListEmployees = QListWidget(self.tab_2)
        self.ListEmployees.setObjectName(u"ListEmployees")

        self.horizontalLayout_2.addWidget(self.ListEmployees)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.TextItemName = QLineEdit(self.tab_2)
        self.TextItemName.setObjectName(u"TextItemName")

        self.verticalLayout_4.addWidget(self.TextItemName)

        self.BtnAdd = QPushButton(self.tab_2)
        self.BtnAdd.setObjectName(u"BtnAdd")

        self.verticalLayout_4.addWidget(self.BtnAdd)

        self.BtnDelete = QPushButton(self.tab_2)
        self.BtnDelete.setObjectName(u"BtnDelete")

        self.verticalLayout_4.addWidget(self.BtnDelete)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.label_3 = QLabel(self.tab_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_4.addWidget(self.label_3)

        self.CboxDefaultEmployee = QComboBox(self.tab_2)
        self.CboxDefaultEmployee.setObjectName(u"CboxDefaultEmployee")

        self.verticalLayout_4.addWidget(self.CboxDefaultEmployee)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_5 = QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.TextDocumentName = QLineEdit(self.tab)
        self.TextDocumentName.setObjectName(u"TextDocumentName")

        self.verticalLayout_2.addWidget(self.TextDocumentName)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.TextSheetName = QLineEdit(self.tab)
        self.TextSheetName.setObjectName(u"TextSheetName")

        self.verticalLayout_3.addWidget(self.TextSheetName)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tab, "")
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 518, 1642))
        self.verticalLayout_22 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.label_20 = QLabel(self.scrollAreaWidgetContents)
        self.label_20.setObjectName(u"label_20")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_20.setFont(font)

        self.verticalLayout_26.addWidget(self.label_20)

        self.formLayout_9 = QFormLayout()
        self.formLayout_9.setObjectName(u"formLayout_9")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_59 = QLabel(self.scrollAreaWidgetContents)
        self.label_59.setObjectName(u"label_59")

        self.horizontalLayout_8.addWidget(self.label_59)

        self.label_60 = QLabel(self.scrollAreaWidgetContents)
        self.label_60.setObjectName(u"label_60")

        self.horizontalLayout_8.addWidget(self.label_60)

        self.label_61 = QLabel(self.scrollAreaWidgetContents)
        self.label_61.setObjectName(u"label_61")

        self.horizontalLayout_8.addWidget(self.label_61)

        self.label_62 = QLabel(self.scrollAreaWidgetContents)
        self.label_62.setObjectName(u"label_62")

        self.horizontalLayout_8.addWidget(self.label_62)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)


        self.formLayout_9.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_8)

        self.checkBox_92 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_92.setObjectName(u"checkBox_92")

        self.formLayout_9.setWidget(2, QFormLayout.LabelRole, self.checkBox_92)

        self.horizontalLayout_113 = QHBoxLayout()
        self.horizontalLayout_113.setObjectName(u"horizontalLayout_113")
        self.radioButton_334 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_334.setObjectName(u"radioButton_334")
        self.radioButton_334.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_113.addWidget(self.radioButton_334)

        self.radioButton_335 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_335.setObjectName(u"radioButton_335")
        self.radioButton_335.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_113.addWidget(self.radioButton_335)

        self.radioButton_336 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_336.setObjectName(u"radioButton_336")
        self.radioButton_336.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_113.addWidget(self.radioButton_336)

        self.lineEdit_100 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_100.setObjectName(u"lineEdit_100")

        self.horizontalLayout_113.addWidget(self.lineEdit_100)


        self.formLayout_9.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_113)

        self.checkBox_93 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_93.setObjectName(u"checkBox_93")

        self.formLayout_9.setWidget(4, QFormLayout.LabelRole, self.checkBox_93)

        self.horizontalLayout_114 = QHBoxLayout()
        self.horizontalLayout_114.setObjectName(u"horizontalLayout_114")
        self.radioButton_337 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_337.setObjectName(u"radioButton_337")
        self.radioButton_337.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_114.addWidget(self.radioButton_337)

        self.radioButton_338 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_338.setObjectName(u"radioButton_338")
        self.radioButton_338.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_114.addWidget(self.radioButton_338)

        self.radioButton_339 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_339.setObjectName(u"radioButton_339")
        self.radioButton_339.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_114.addWidget(self.radioButton_339)

        self.lineEdit_101 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_101.setObjectName(u"lineEdit_101")

        self.horizontalLayout_114.addWidget(self.lineEdit_101)


        self.formLayout_9.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_114)

        self.checkBox_94 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_94.setObjectName(u"checkBox_94")

        self.formLayout_9.setWidget(5, QFormLayout.LabelRole, self.checkBox_94)

        self.horizontalLayout_115 = QHBoxLayout()
        self.horizontalLayout_115.setObjectName(u"horizontalLayout_115")
        self.radioButton_340 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_340.setObjectName(u"radioButton_340")
        self.radioButton_340.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_115.addWidget(self.radioButton_340)

        self.radioButton_341 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_341.setObjectName(u"radioButton_341")
        self.radioButton_341.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_115.addWidget(self.radioButton_341)

        self.radioButton_342 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_342.setObjectName(u"radioButton_342")
        self.radioButton_342.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_115.addWidget(self.radioButton_342)

        self.lineEdit_102 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_102.setObjectName(u"lineEdit_102")

        self.horizontalLayout_115.addWidget(self.lineEdit_102)


        self.formLayout_9.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_115)

        self.checkBox_95 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_95.setObjectName(u"checkBox_95")

        self.formLayout_9.setWidget(6, QFormLayout.LabelRole, self.checkBox_95)

        self.horizontalLayout_116 = QHBoxLayout()
        self.horizontalLayout_116.setObjectName(u"horizontalLayout_116")
        self.radioButton_343 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_343.setObjectName(u"radioButton_343")
        self.radioButton_343.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_116.addWidget(self.radioButton_343)

        self.radioButton_344 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_344.setObjectName(u"radioButton_344")
        self.radioButton_344.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_116.addWidget(self.radioButton_344)

        self.radioButton_345 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_345.setObjectName(u"radioButton_345")
        self.radioButton_345.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_116.addWidget(self.radioButton_345)

        self.lineEdit_103 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_103.setObjectName(u"lineEdit_103")

        self.horizontalLayout_116.addWidget(self.lineEdit_103)


        self.formLayout_9.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout_116)

        self.checkBox_96 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_96.setObjectName(u"checkBox_96")

        self.formLayout_9.setWidget(7, QFormLayout.LabelRole, self.checkBox_96)

        self.horizontalLayout_117 = QHBoxLayout()
        self.horizontalLayout_117.setObjectName(u"horizontalLayout_117")
        self.radioButton_346 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_346.setObjectName(u"radioButton_346")
        self.radioButton_346.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_117.addWidget(self.radioButton_346)

        self.radioButton_347 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_347.setObjectName(u"radioButton_347")
        self.radioButton_347.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_117.addWidget(self.radioButton_347)

        self.radioButton_348 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_348.setObjectName(u"radioButton_348")
        self.radioButton_348.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_117.addWidget(self.radioButton_348)

        self.lineEdit_104 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_104.setObjectName(u"lineEdit_104")

        self.horizontalLayout_117.addWidget(self.lineEdit_104)


        self.formLayout_9.setLayout(7, QFormLayout.FieldRole, self.horizontalLayout_117)

        self.label_30 = QLabel(self.scrollAreaWidgetContents)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setMinimumSize(QSize(140, 0))

        self.formLayout_9.setWidget(0, QFormLayout.LabelRole, self.label_30)

        self.checkBox_97 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_97.setObjectName(u"checkBox_97")

        self.formLayout_9.setWidget(1, QFormLayout.LabelRole, self.checkBox_97)

        self.horizontalLayout_118 = QHBoxLayout()
        self.horizontalLayout_118.setObjectName(u"horizontalLayout_118")
        self.radioButton_349 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_349.setObjectName(u"radioButton_349")
        self.radioButton_349.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_118.addWidget(self.radioButton_349)

        self.radioButton_350 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_350.setObjectName(u"radioButton_350")
        self.radioButton_350.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_118.addWidget(self.radioButton_350)

        self.radioButton_351 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_351.setObjectName(u"radioButton_351")
        self.radioButton_351.setMinimumSize(QSize(0, 0))
        self.radioButton_351.setCursor(QCursor(Qt.PointingHandCursor))
        self.radioButton_351.setIconSize(QSize(16, 16))

        self.horizontalLayout_118.addWidget(self.radioButton_351)

        self.lineEdit_105 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_105.setObjectName(u"lineEdit_105")

        self.horizontalLayout_118.addWidget(self.lineEdit_105)


        self.formLayout_9.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_118)


        self.verticalLayout_26.addLayout(self.formLayout_9)


        self.verticalLayout_22.addLayout(self.verticalLayout_26)

        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.label_18 = QLabel(self.scrollAreaWidgetContents)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)

        self.verticalLayout_24.addWidget(self.label_18)

        self.formLayout_7 = QFormLayout()
        self.formLayout_7.setObjectName(u"formLayout_7")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_51 = QLabel(self.scrollAreaWidgetContents)
        self.label_51.setObjectName(u"label_51")

        self.horizontalLayout_6.addWidget(self.label_51)

        self.label_52 = QLabel(self.scrollAreaWidgetContents)
        self.label_52.setObjectName(u"label_52")

        self.horizontalLayout_6.addWidget(self.label_52)

        self.label_53 = QLabel(self.scrollAreaWidgetContents)
        self.label_53.setObjectName(u"label_53")

        self.horizontalLayout_6.addWidget(self.label_53)

        self.label_54 = QLabel(self.scrollAreaWidgetContents)
        self.label_54.setObjectName(u"label_54")

        self.horizontalLayout_6.addWidget(self.label_54)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)


        self.formLayout_7.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_6)

        self.checkBox_72 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_72.setObjectName(u"checkBox_72")

        self.formLayout_7.setWidget(1, QFormLayout.LabelRole, self.checkBox_72)

        self.horizontalLayout_93 = QHBoxLayout()
        self.horizontalLayout_93.setObjectName(u"horizontalLayout_93")
        self.radioButton_274 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_274.setObjectName(u"radioButton_274")
        self.radioButton_274.setCursor(QCursor(Qt.PointingHandCursor))
        self.radioButton_274.setIconSize(QSize(32, 32))

        self.horizontalLayout_93.addWidget(self.radioButton_274)

        self.radioButton_275 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_275.setObjectName(u"radioButton_275")
        self.radioButton_275.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_93.addWidget(self.radioButton_275)

        self.radioButton_276 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_276.setObjectName(u"radioButton_276")
        self.radioButton_276.setCursor(QCursor(Qt.PointingHandCursor))
        self.radioButton_276.setChecked(True)

        self.horizontalLayout_93.addWidget(self.radioButton_276)

        self.lineEdit_80 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_80.setObjectName(u"lineEdit_80")

        self.horizontalLayout_93.addWidget(self.lineEdit_80)


        self.formLayout_7.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_93)

        self.checkBox_73 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_73.setObjectName(u"checkBox_73")

        self.formLayout_7.setWidget(2, QFormLayout.LabelRole, self.checkBox_73)

        self.horizontalLayout_94 = QHBoxLayout()
        self.horizontalLayout_94.setObjectName(u"horizontalLayout_94")
        self.radioButton_277 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_277.setObjectName(u"radioButton_277")
        self.radioButton_277.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_94.addWidget(self.radioButton_277)

        self.radioButton_278 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_278.setObjectName(u"radioButton_278")
        self.radioButton_278.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_94.addWidget(self.radioButton_278)

        self.radioButton_279 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_279.setObjectName(u"radioButton_279")
        self.radioButton_279.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_94.addWidget(self.radioButton_279)

        self.lineEdit_81 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_81.setObjectName(u"lineEdit_81")

        self.horizontalLayout_94.addWidget(self.lineEdit_81)


        self.formLayout_7.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_94)

        self.checkBox_74 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_74.setObjectName(u"checkBox_74")

        self.formLayout_7.setWidget(3, QFormLayout.LabelRole, self.checkBox_74)

        self.horizontalLayout_95 = QHBoxLayout()
        self.horizontalLayout_95.setObjectName(u"horizontalLayout_95")
        self.radioButton_280 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_280.setObjectName(u"radioButton_280")
        self.radioButton_280.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_95.addWidget(self.radioButton_280)

        self.radioButton_281 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_281.setObjectName(u"radioButton_281")
        self.radioButton_281.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_95.addWidget(self.radioButton_281)

        self.radioButton_282 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_282.setObjectName(u"radioButton_282")
        self.radioButton_282.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_95.addWidget(self.radioButton_282)

        self.lineEdit_82 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_82.setObjectName(u"lineEdit_82")

        self.horizontalLayout_95.addWidget(self.lineEdit_82)


        self.formLayout_7.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_95)

        self.checkBox_76 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_76.setObjectName(u"checkBox_76")

        self.formLayout_7.setWidget(4, QFormLayout.LabelRole, self.checkBox_76)

        self.horizontalLayout_97 = QHBoxLayout()
        self.horizontalLayout_97.setObjectName(u"horizontalLayout_97")
        self.radioButton_286 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_286.setObjectName(u"radioButton_286")
        self.radioButton_286.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_97.addWidget(self.radioButton_286)

        self.radioButton_287 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_287.setObjectName(u"radioButton_287")
        self.radioButton_287.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_97.addWidget(self.radioButton_287)

        self.radioButton_288 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_288.setObjectName(u"radioButton_288")
        self.radioButton_288.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_97.addWidget(self.radioButton_288)

        self.lineEdit_84 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_84.setObjectName(u"lineEdit_84")

        self.horizontalLayout_97.addWidget(self.lineEdit_84)


        self.formLayout_7.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_97)

        self.label_31 = QLabel(self.scrollAreaWidgetContents)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(140, 0))

        self.formLayout_7.setWidget(0, QFormLayout.LabelRole, self.label_31)


        self.verticalLayout_24.addLayout(self.formLayout_7)


        self.verticalLayout_22.addLayout(self.verticalLayout_24)

        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.label_16 = QLabel(self.scrollAreaWidgetContents)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)

        self.verticalLayout_21.addWidget(self.label_16)

        self.formLayout_5 = QFormLayout()
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_43 = QLabel(self.scrollAreaWidgetContents)
        self.label_43.setObjectName(u"label_43")

        self.horizontalLayout_9.addWidget(self.label_43)

        self.label_44 = QLabel(self.scrollAreaWidgetContents)
        self.label_44.setObjectName(u"label_44")

        self.horizontalLayout_9.addWidget(self.label_44)

        self.label_45 = QLabel(self.scrollAreaWidgetContents)
        self.label_45.setObjectName(u"label_45")

        self.horizontalLayout_9.addWidget(self.label_45)

        self.label_46 = QLabel(self.scrollAreaWidgetContents)
        self.label_46.setObjectName(u"label_46")

        self.horizontalLayout_9.addWidget(self.label_46)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_2)


        self.formLayout_5.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_9)

        self.checkBox_41 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_41.setObjectName(u"checkBox_41")

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.checkBox_41)

        self.horizontalLayout_62 = QHBoxLayout()
        self.horizontalLayout_62.setObjectName(u"horizontalLayout_62")
        self.radioButton_181 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_181.setObjectName(u"radioButton_181")
        self.radioButton_181.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_62.addWidget(self.radioButton_181)

        self.radioButton_182 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_182.setObjectName(u"radioButton_182")
        self.radioButton_182.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_62.addWidget(self.radioButton_182)

        self.radioButton_183 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_183.setObjectName(u"radioButton_183")
        self.radioButton_183.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_62.addWidget(self.radioButton_183)

        self.lineEdit_49 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_49.setObjectName(u"lineEdit_49")

        self.horizontalLayout_62.addWidget(self.lineEdit_49)


        self.formLayout_5.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_62)

        self.checkBox_42 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_42.setObjectName(u"checkBox_42")

        self.formLayout_5.setWidget(2, QFormLayout.LabelRole, self.checkBox_42)

        self.horizontalLayout_63 = QHBoxLayout()
        self.horizontalLayout_63.setObjectName(u"horizontalLayout_63")
        self.radioButton_184 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_184.setObjectName(u"radioButton_184")
        self.radioButton_184.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_63.addWidget(self.radioButton_184)

        self.radioButton_185 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_185.setObjectName(u"radioButton_185")
        self.radioButton_185.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_63.addWidget(self.radioButton_185)

        self.radioButton_186 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_186.setObjectName(u"radioButton_186")
        self.radioButton_186.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_63.addWidget(self.radioButton_186)

        self.lineEdit_50 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_50.setObjectName(u"lineEdit_50")

        self.horizontalLayout_63.addWidget(self.lineEdit_50)


        self.formLayout_5.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_63)

        self.checkBox_43 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_43.setObjectName(u"checkBox_43")

        self.formLayout_5.setWidget(3, QFormLayout.LabelRole, self.checkBox_43)

        self.horizontalLayout_64 = QHBoxLayout()
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.radioButton_187 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_187.setObjectName(u"radioButton_187")
        self.radioButton_187.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_64.addWidget(self.radioButton_187)

        self.radioButton_188 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_188.setObjectName(u"radioButton_188")
        self.radioButton_188.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_64.addWidget(self.radioButton_188)

        self.radioButton_189 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_189.setObjectName(u"radioButton_189")
        self.radioButton_189.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_64.addWidget(self.radioButton_189)

        self.lineEdit_51 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_51.setObjectName(u"lineEdit_51")

        self.horizontalLayout_64.addWidget(self.lineEdit_51)


        self.formLayout_5.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_64)

        self.checkBox_44 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_44.setObjectName(u"checkBox_44")

        self.formLayout_5.setWidget(4, QFormLayout.LabelRole, self.checkBox_44)

        self.horizontalLayout_65 = QHBoxLayout()
        self.horizontalLayout_65.setObjectName(u"horizontalLayout_65")
        self.radioButton_190 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_190.setObjectName(u"radioButton_190")
        self.radioButton_190.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_65.addWidget(self.radioButton_190)

        self.radioButton_191 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_191.setObjectName(u"radioButton_191")
        self.radioButton_191.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_65.addWidget(self.radioButton_191)

        self.radioButton_192 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_192.setObjectName(u"radioButton_192")
        self.radioButton_192.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_65.addWidget(self.radioButton_192)

        self.lineEdit_52 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_52.setObjectName(u"lineEdit_52")

        self.horizontalLayout_65.addWidget(self.lineEdit_52)


        self.formLayout_5.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_65)

        self.checkBox_45 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_45.setObjectName(u"checkBox_45")

        self.formLayout_5.setWidget(5, QFormLayout.LabelRole, self.checkBox_45)

        self.horizontalLayout_66 = QHBoxLayout()
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.radioButton_193 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_193.setObjectName(u"radioButton_193")
        self.radioButton_193.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_66.addWidget(self.radioButton_193)

        self.radioButton_194 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_194.setObjectName(u"radioButton_194")
        self.radioButton_194.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_66.addWidget(self.radioButton_194)

        self.radioButton_195 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_195.setObjectName(u"radioButton_195")
        self.radioButton_195.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_66.addWidget(self.radioButton_195)

        self.lineEdit_53 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_53.setObjectName(u"lineEdit_53")

        self.horizontalLayout_66.addWidget(self.lineEdit_53)


        self.formLayout_5.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_66)

        self.checkBox_46 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_46.setObjectName(u"checkBox_46")

        self.formLayout_5.setWidget(6, QFormLayout.LabelRole, self.checkBox_46)

        self.horizontalLayout_67 = QHBoxLayout()
        self.horizontalLayout_67.setObjectName(u"horizontalLayout_67")
        self.radioButton_196 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_196.setObjectName(u"radioButton_196")
        self.radioButton_196.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_67.addWidget(self.radioButton_196)

        self.radioButton_197 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_197.setObjectName(u"radioButton_197")
        self.radioButton_197.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_67.addWidget(self.radioButton_197)

        self.radioButton_198 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_198.setObjectName(u"radioButton_198")
        self.radioButton_198.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_67.addWidget(self.radioButton_198)

        self.lineEdit_54 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_54.setObjectName(u"lineEdit_54")

        self.horizontalLayout_67.addWidget(self.lineEdit_54)


        self.formLayout_5.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout_67)

        self.checkBox_47 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_47.setObjectName(u"checkBox_47")

        self.formLayout_5.setWidget(7, QFormLayout.LabelRole, self.checkBox_47)

        self.horizontalLayout_68 = QHBoxLayout()
        self.horizontalLayout_68.setObjectName(u"horizontalLayout_68")
        self.radioButton_199 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_199.setObjectName(u"radioButton_199")
        self.radioButton_199.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_68.addWidget(self.radioButton_199)

        self.radioButton_200 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_200.setObjectName(u"radioButton_200")
        self.radioButton_200.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_68.addWidget(self.radioButton_200)

        self.radioButton_201 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_201.setObjectName(u"radioButton_201")
        self.radioButton_201.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_68.addWidget(self.radioButton_201)

        self.lineEdit_55 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_55.setObjectName(u"lineEdit_55")

        self.horizontalLayout_68.addWidget(self.lineEdit_55)


        self.formLayout_5.setLayout(7, QFormLayout.FieldRole, self.horizontalLayout_68)

        self.checkBox_48 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_48.setObjectName(u"checkBox_48")

        self.formLayout_5.setWidget(8, QFormLayout.LabelRole, self.checkBox_48)

        self.horizontalLayout_69 = QHBoxLayout()
        self.horizontalLayout_69.setObjectName(u"horizontalLayout_69")
        self.radioButton_202 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_202.setObjectName(u"radioButton_202")
        self.radioButton_202.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_69.addWidget(self.radioButton_202)

        self.radioButton_203 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_203.setObjectName(u"radioButton_203")
        self.radioButton_203.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_69.addWidget(self.radioButton_203)

        self.radioButton_204 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_204.setObjectName(u"radioButton_204")
        self.radioButton_204.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_69.addWidget(self.radioButton_204)

        self.lineEdit_56 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_56.setObjectName(u"lineEdit_56")

        self.horizontalLayout_69.addWidget(self.lineEdit_56)


        self.formLayout_5.setLayout(8, QFormLayout.FieldRole, self.horizontalLayout_69)

        self.label_32 = QLabel(self.scrollAreaWidgetContents)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setMinimumSize(QSize(140, 0))

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.label_32)


        self.verticalLayout_21.addLayout(self.formLayout_5)


        self.verticalLayout_22.addLayout(self.verticalLayout_21)

        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.label_21 = QLabel(self.scrollAreaWidgetContents)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font)

        self.verticalLayout_27.addWidget(self.label_21)

        self.formLayout_10 = QFormLayout()
        self.formLayout_10.setObjectName(u"formLayout_10")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_63 = QLabel(self.scrollAreaWidgetContents)
        self.label_63.setObjectName(u"label_63")

        self.horizontalLayout_10.addWidget(self.label_63)

        self.label_64 = QLabel(self.scrollAreaWidgetContents)
        self.label_64.setObjectName(u"label_64")

        self.horizontalLayout_10.addWidget(self.label_64)

        self.label_65 = QLabel(self.scrollAreaWidgetContents)
        self.label_65.setObjectName(u"label_65")

        self.horizontalLayout_10.addWidget(self.label_65)

        self.label_66 = QLabel(self.scrollAreaWidgetContents)
        self.label_66.setObjectName(u"label_66")

        self.horizontalLayout_10.addWidget(self.label_66)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_7)


        self.formLayout_10.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_10)

        self.checkBox_38 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_38.setObjectName(u"checkBox_38")

        self.formLayout_10.setWidget(1, QFormLayout.LabelRole, self.checkBox_38)

        self.horizontalLayout_58 = QHBoxLayout()
        self.horizontalLayout_58.setObjectName(u"horizontalLayout_58")
        self.radioButton_169 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_169.setObjectName(u"radioButton_169")

        self.horizontalLayout_58.addWidget(self.radioButton_169)

        self.radioButton_170 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_170.setObjectName(u"radioButton_170")

        self.horizontalLayout_58.addWidget(self.radioButton_170)

        self.radioButton_171 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_171.setObjectName(u"radioButton_171")

        self.horizontalLayout_58.addWidget(self.radioButton_171)

        self.lineEdit_45 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_45.setObjectName(u"lineEdit_45")

        self.horizontalLayout_58.addWidget(self.lineEdit_45)


        self.formLayout_10.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_58)

        self.checkBox_39 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_39.setObjectName(u"checkBox_39")

        self.formLayout_10.setWidget(2, QFormLayout.LabelRole, self.checkBox_39)

        self.horizontalLayout_59 = QHBoxLayout()
        self.horizontalLayout_59.setObjectName(u"horizontalLayout_59")
        self.radioButton_172 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_172.setObjectName(u"radioButton_172")

        self.horizontalLayout_59.addWidget(self.radioButton_172)

        self.radioButton_173 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_173.setObjectName(u"radioButton_173")

        self.horizontalLayout_59.addWidget(self.radioButton_173)

        self.radioButton_174 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_174.setObjectName(u"radioButton_174")

        self.horizontalLayout_59.addWidget(self.radioButton_174)

        self.lineEdit_46 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_46.setObjectName(u"lineEdit_46")

        self.horizontalLayout_59.addWidget(self.lineEdit_46)


        self.formLayout_10.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_59)

        self.checkBox_40 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_40.setObjectName(u"checkBox_40")

        self.formLayout_10.setWidget(3, QFormLayout.LabelRole, self.checkBox_40)

        self.horizontalLayout_60 = QHBoxLayout()
        self.horizontalLayout_60.setObjectName(u"horizontalLayout_60")
        self.radioButton_175 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_175.setObjectName(u"radioButton_175")

        self.horizontalLayout_60.addWidget(self.radioButton_175)

        self.radioButton_176 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_176.setObjectName(u"radioButton_176")

        self.horizontalLayout_60.addWidget(self.radioButton_176)

        self.radioButton_177 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_177.setObjectName(u"radioButton_177")

        self.horizontalLayout_60.addWidget(self.radioButton_177)

        self.lineEdit_47 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_47.setObjectName(u"lineEdit_47")

        self.horizontalLayout_60.addWidget(self.lineEdit_47)


        self.formLayout_10.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_60)

        self.checkBox_63 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_63.setObjectName(u"checkBox_63")

        self.formLayout_10.setWidget(4, QFormLayout.LabelRole, self.checkBox_63)

        self.horizontalLayout_61 = QHBoxLayout()
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.radioButton_178 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_178.setObjectName(u"radioButton_178")

        self.horizontalLayout_61.addWidget(self.radioButton_178)

        self.radioButton_179 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_179.setObjectName(u"radioButton_179")

        self.horizontalLayout_61.addWidget(self.radioButton_179)

        self.radioButton_180 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_180.setObjectName(u"radioButton_180")

        self.horizontalLayout_61.addWidget(self.radioButton_180)

        self.lineEdit_48 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_48.setObjectName(u"lineEdit_48")

        self.horizontalLayout_61.addWidget(self.lineEdit_48)


        self.formLayout_10.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_61)

        self.checkBox_64 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_64.setObjectName(u"checkBox_64")

        self.formLayout_10.setWidget(5, QFormLayout.LabelRole, self.checkBox_64)

        self.horizontalLayout_84 = QHBoxLayout()
        self.horizontalLayout_84.setObjectName(u"horizontalLayout_84")
        self.radioButton_247 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_247.setObjectName(u"radioButton_247")

        self.horizontalLayout_84.addWidget(self.radioButton_247)

        self.radioButton_248 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_248.setObjectName(u"radioButton_248")

        self.horizontalLayout_84.addWidget(self.radioButton_248)

        self.radioButton_249 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_249.setObjectName(u"radioButton_249")

        self.horizontalLayout_84.addWidget(self.radioButton_249)

        self.lineEdit_71 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_71.setObjectName(u"lineEdit_71")

        self.horizontalLayout_84.addWidget(self.lineEdit_71)


        self.formLayout_10.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_84)

        self.checkBox_65 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_65.setObjectName(u"checkBox_65")

        self.formLayout_10.setWidget(6, QFormLayout.LabelRole, self.checkBox_65)

        self.horizontalLayout_85 = QHBoxLayout()
        self.horizontalLayout_85.setObjectName(u"horizontalLayout_85")
        self.radioButton_250 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_250.setObjectName(u"radioButton_250")

        self.horizontalLayout_85.addWidget(self.radioButton_250)

        self.radioButton_251 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_251.setObjectName(u"radioButton_251")

        self.horizontalLayout_85.addWidget(self.radioButton_251)

        self.radioButton_252 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_252.setObjectName(u"radioButton_252")

        self.horizontalLayout_85.addWidget(self.radioButton_252)

        self.lineEdit_72 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_72.setObjectName(u"lineEdit_72")

        self.horizontalLayout_85.addWidget(self.lineEdit_72)


        self.formLayout_10.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout_85)

        self.label_26 = QLabel(self.scrollAreaWidgetContents)
        self.label_26.setObjectName(u"label_26")

        self.formLayout_10.setWidget(7, QFormLayout.LabelRole, self.label_26)

        self.checkBox_11 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_11.setObjectName(u"checkBox_11")

        self.formLayout_10.setWidget(8, QFormLayout.LabelRole, self.checkBox_11)

        self.horizontalLayout_87 = QHBoxLayout()
        self.horizontalLayout_87.setObjectName(u"horizontalLayout_87")
        self.radioButton_256 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_256.setObjectName(u"radioButton_256")

        self.horizontalLayout_87.addWidget(self.radioButton_256)

        self.radioButton_257 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_257.setObjectName(u"radioButton_257")

        self.horizontalLayout_87.addWidget(self.radioButton_257)

        self.radioButton_258 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_258.setObjectName(u"radioButton_258")

        self.horizontalLayout_87.addWidget(self.radioButton_258)

        self.lineEdit_74 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_74.setObjectName(u"lineEdit_74")

        self.horizontalLayout_87.addWidget(self.lineEdit_74)


        self.formLayout_10.setLayout(8, QFormLayout.FieldRole, self.horizontalLayout_87)

        self.checkBox_67 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_67.setObjectName(u"checkBox_67")

        self.formLayout_10.setWidget(9, QFormLayout.LabelRole, self.checkBox_67)

        self.horizontalLayout_88 = QHBoxLayout()
        self.horizontalLayout_88.setObjectName(u"horizontalLayout_88")
        self.radioButton_259 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_259.setObjectName(u"radioButton_259")

        self.horizontalLayout_88.addWidget(self.radioButton_259)

        self.radioButton_260 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_260.setObjectName(u"radioButton_260")

        self.horizontalLayout_88.addWidget(self.radioButton_260)

        self.radioButton_261 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_261.setObjectName(u"radioButton_261")

        self.horizontalLayout_88.addWidget(self.radioButton_261)

        self.lineEdit_75 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_75.setObjectName(u"lineEdit_75")

        self.horizontalLayout_88.addWidget(self.lineEdit_75)


        self.formLayout_10.setLayout(9, QFormLayout.FieldRole, self.horizontalLayout_88)

        self.checkBox_68 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_68.setObjectName(u"checkBox_68")

        self.formLayout_10.setWidget(10, QFormLayout.LabelRole, self.checkBox_68)

        self.horizontalLayout_89 = QHBoxLayout()
        self.horizontalLayout_89.setObjectName(u"horizontalLayout_89")
        self.radioButton_262 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_262.setObjectName(u"radioButton_262")

        self.horizontalLayout_89.addWidget(self.radioButton_262)

        self.radioButton_263 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_263.setObjectName(u"radioButton_263")

        self.horizontalLayout_89.addWidget(self.radioButton_263)

        self.radioButton_264 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_264.setObjectName(u"radioButton_264")

        self.horizontalLayout_89.addWidget(self.radioButton_264)

        self.lineEdit_76 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_76.setObjectName(u"lineEdit_76")

        self.horizontalLayout_89.addWidget(self.lineEdit_76)


        self.formLayout_10.setLayout(10, QFormLayout.FieldRole, self.horizontalLayout_89)

        self.label_33 = QLabel(self.scrollAreaWidgetContents)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setMinimumSize(QSize(140, 0))

        self.formLayout_10.setWidget(0, QFormLayout.LabelRole, self.label_33)


        self.verticalLayout_27.addLayout(self.formLayout_10)


        self.verticalLayout_22.addLayout(self.verticalLayout_27)

        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.label_15 = QLabel(self.scrollAreaWidgetContents)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)

        self.verticalLayout_20.addWidget(self.label_15)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_35 = QLabel(self.scrollAreaWidgetContents)
        self.label_35.setObjectName(u"label_35")

        self.horizontalLayout_11.addWidget(self.label_35)

        self.label_37 = QLabel(self.scrollAreaWidgetContents)
        self.label_37.setObjectName(u"label_37")

        self.horizontalLayout_11.addWidget(self.label_37)

        self.label_38 = QLabel(self.scrollAreaWidgetContents)
        self.label_38.setObjectName(u"label_38")

        self.horizontalLayout_11.addWidget(self.label_38)

        self.label_39 = QLabel(self.scrollAreaWidgetContents)
        self.label_39.setObjectName(u"label_39")

        self.horizontalLayout_11.addWidget(self.label_39)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_11)

        self.checkBox_3 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.checkBox_3)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.radioButton_61 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_61.setObjectName(u"radioButton_61")
        self.radioButton_61.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_22.addWidget(self.radioButton_61)

        self.radioButton_62 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_62.setObjectName(u"radioButton_62")
        self.radioButton_62.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_22.addWidget(self.radioButton_62)

        self.radioButton_63 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_63.setObjectName(u"radioButton_63")
        self.radioButton_63.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_22.addWidget(self.radioButton_63)

        self.lineEdit_5 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.horizontalLayout_22.addWidget(self.lineEdit_5)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_22)

        self.checkBox_12 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_12.setObjectName(u"checkBox_12")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.checkBox_12)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.radioButton_67 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_67.setObjectName(u"radioButton_67")
        self.radioButton_67.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_24.addWidget(self.radioButton_67)

        self.radioButton_68 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_68.setObjectName(u"radioButton_68")
        self.radioButton_68.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_24.addWidget(self.radioButton_68)

        self.radioButton_69 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_69.setObjectName(u"radioButton_69")
        self.radioButton_69.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_24.addWidget(self.radioButton_69)

        self.lineEdit_7 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.horizontalLayout_24.addWidget(self.lineEdit_7)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_24)

        self.checkBox_13 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_13.setObjectName(u"checkBox_13")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.checkBox_13)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.radioButton_70 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_70.setObjectName(u"radioButton_70")
        self.radioButton_70.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_25.addWidget(self.radioButton_70)

        self.radioButton_71 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_71.setObjectName(u"radioButton_71")
        self.radioButton_71.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_25.addWidget(self.radioButton_71)

        self.radioButton_72 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_72.setObjectName(u"radioButton_72")
        self.radioButton_72.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_25.addWidget(self.radioButton_72)

        self.lineEdit_8 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_8.setObjectName(u"lineEdit_8")

        self.horizontalLayout_25.addWidget(self.lineEdit_8)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_25)

        self.checkBox_14 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_14.setObjectName(u"checkBox_14")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.checkBox_14)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.radioButton_85 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_85.setObjectName(u"radioButton_85")
        self.radioButton_85.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_30.addWidget(self.radioButton_85)

        self.radioButton_86 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_86.setObjectName(u"radioButton_86")
        self.radioButton_86.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_30.addWidget(self.radioButton_86)

        self.radioButton_87 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_87.setObjectName(u"radioButton_87")
        self.radioButton_87.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_30.addWidget(self.radioButton_87)

        self.lineEdit_17 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_17.setObjectName(u"lineEdit_17")

        self.horizontalLayout_30.addWidget(self.lineEdit_17)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_30)

        self.checkBox_15 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_15.setObjectName(u"checkBox_15")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.checkBox_15)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.radioButton_88 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_88.setObjectName(u"radioButton_88")
        self.radioButton_88.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_31.addWidget(self.radioButton_88)

        self.radioButton_89 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_89.setObjectName(u"radioButton_89")
        self.radioButton_89.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_31.addWidget(self.radioButton_89)

        self.radioButton_90 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_90.setObjectName(u"radioButton_90")
        self.radioButton_90.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_31.addWidget(self.radioButton_90)

        self.lineEdit_18 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_18.setObjectName(u"lineEdit_18")

        self.horizontalLayout_31.addWidget(self.lineEdit_18)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_31)

        self.checkBox_16 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_16.setObjectName(u"checkBox_16")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.checkBox_16)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.radioButton_91 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_91.setObjectName(u"radioButton_91")
        self.radioButton_91.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_32.addWidget(self.radioButton_91)

        self.radioButton_92 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_92.setObjectName(u"radioButton_92")
        self.radioButton_92.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_32.addWidget(self.radioButton_92)

        self.radioButton_93 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_93.setObjectName(u"radioButton_93")
        self.radioButton_93.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_32.addWidget(self.radioButton_93)

        self.lineEdit_19 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_19.setObjectName(u"lineEdit_19")

        self.horizontalLayout_32.addWidget(self.lineEdit_19)


        self.formLayout.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout_32)

        self.checkBox_17 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_17.setObjectName(u"checkBox_17")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.checkBox_17)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.radioButton_94 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_94.setObjectName(u"radioButton_94")
        self.radioButton_94.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_33.addWidget(self.radioButton_94)

        self.radioButton_95 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_95.setObjectName(u"radioButton_95")
        self.radioButton_95.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_33.addWidget(self.radioButton_95)

        self.radioButton_96 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_96.setObjectName(u"radioButton_96")
        self.radioButton_96.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_33.addWidget(self.radioButton_96)

        self.lineEdit_20 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_20.setObjectName(u"lineEdit_20")

        self.horizontalLayout_33.addWidget(self.lineEdit_20)


        self.formLayout.setLayout(7, QFormLayout.FieldRole, self.horizontalLayout_33)

        self.checkBox_18 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_18.setObjectName(u"checkBox_18")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.checkBox_18)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.radioButton_97 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_97.setObjectName(u"radioButton_97")
        self.radioButton_97.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_34.addWidget(self.radioButton_97)

        self.radioButton_98 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_98.setObjectName(u"radioButton_98")
        self.radioButton_98.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_34.addWidget(self.radioButton_98)

        self.radioButton_99 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_99.setObjectName(u"radioButton_99")
        self.radioButton_99.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_34.addWidget(self.radioButton_99)

        self.lineEdit_21 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_21.setObjectName(u"lineEdit_21")

        self.horizontalLayout_34.addWidget(self.lineEdit_21)


        self.formLayout.setLayout(8, QFormLayout.FieldRole, self.horizontalLayout_34)

        self.checkBox_19 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_19.setObjectName(u"checkBox_19")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.checkBox_19)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.radioButton_106 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_106.setObjectName(u"radioButton_106")
        self.radioButton_106.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_37.addWidget(self.radioButton_106)

        self.radioButton_107 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_107.setObjectName(u"radioButton_107")
        self.radioButton_107.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_37.addWidget(self.radioButton_107)

        self.radioButton_108 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_108.setObjectName(u"radioButton_108")
        self.radioButton_108.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_37.addWidget(self.radioButton_108)

        self.lineEdit_24 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_24.setObjectName(u"lineEdit_24")

        self.horizontalLayout_37.addWidget(self.lineEdit_24)


        self.formLayout.setLayout(9, QFormLayout.FieldRole, self.horizontalLayout_37)

        self.checkBox_34 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_34.setObjectName(u"checkBox_34")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.checkBox_34)

        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.radioButton_112 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_112.setObjectName(u"radioButton_112")
        self.radioButton_112.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_39.addWidget(self.radioButton_112)

        self.radioButton_113 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_113.setObjectName(u"radioButton_113")
        self.radioButton_113.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_39.addWidget(self.radioButton_113)

        self.radioButton_114 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_114.setObjectName(u"radioButton_114")
        self.radioButton_114.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_39.addWidget(self.radioButton_114)

        self.lineEdit_26 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_26.setObjectName(u"lineEdit_26")

        self.horizontalLayout_39.addWidget(self.lineEdit_26)


        self.formLayout.setLayout(10, QFormLayout.FieldRole, self.horizontalLayout_39)

        self.label_22 = QLabel(self.scrollAreaWidgetContents)
        self.label_22.setObjectName(u"label_22")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.label_22)

        self.checkBox_10 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_10.setObjectName(u"checkBox_10")

        self.formLayout.setWidget(12, QFormLayout.LabelRole, self.checkBox_10)

        self.horizontalLayout_40 = QHBoxLayout()
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.radioButton_115 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_115.setObjectName(u"radioButton_115")
        self.radioButton_115.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_40.addWidget(self.radioButton_115)

        self.radioButton_116 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_116.setObjectName(u"radioButton_116")
        self.radioButton_116.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_40.addWidget(self.radioButton_116)

        self.radioButton_117 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_117.setObjectName(u"radioButton_117")
        self.radioButton_117.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_40.addWidget(self.radioButton_117)

        self.lineEdit_27 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_27.setObjectName(u"lineEdit_27")

        self.horizontalLayout_40.addWidget(self.lineEdit_27)


        self.formLayout.setLayout(12, QFormLayout.FieldRole, self.horizontalLayout_40)

        self.checkBox_35 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_35.setObjectName(u"checkBox_35")

        self.formLayout.setWidget(13, QFormLayout.LabelRole, self.checkBox_35)

        self.horizontalLayout_42 = QHBoxLayout()
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.radioButton_121 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_121.setObjectName(u"radioButton_121")
        self.radioButton_121.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_42.addWidget(self.radioButton_121)

        self.radioButton_122 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_122.setObjectName(u"radioButton_122")
        self.radioButton_122.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_42.addWidget(self.radioButton_122)

        self.radioButton_123 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_123.setObjectName(u"radioButton_123")
        self.radioButton_123.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_42.addWidget(self.radioButton_123)

        self.lineEdit_29 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_29.setObjectName(u"lineEdit_29")

        self.horizontalLayout_42.addWidget(self.lineEdit_29)


        self.formLayout.setLayout(13, QFormLayout.FieldRole, self.horizontalLayout_42)

        self.checkBox_4 = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.formLayout.setWidget(14, QFormLayout.LabelRole, self.checkBox_4)

        self.horizontalLayout_41 = QHBoxLayout()
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.radioButton_118 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_118.setObjectName(u"radioButton_118")
        self.radioButton_118.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_41.addWidget(self.radioButton_118)

        self.radioButton_119 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_119.setObjectName(u"radioButton_119")
        self.radioButton_119.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_41.addWidget(self.radioButton_119)

        self.radioButton_120 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_120.setObjectName(u"radioButton_120")
        self.radioButton_120.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_41.addWidget(self.radioButton_120)

        self.lineEdit_28 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_28.setObjectName(u"lineEdit_28")

        self.horizontalLayout_41.addWidget(self.lineEdit_28)


        self.formLayout.setLayout(14, QFormLayout.FieldRole, self.horizontalLayout_41)

        self.label_34 = QLabel(self.scrollAreaWidgetContents)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(140, 0))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_34)


        self.verticalLayout_20.addLayout(self.formLayout)


        self.verticalLayout_22.addLayout(self.verticalLayout_20)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_12.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_10 = QVBoxLayout(self.tab_4)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.groupBox_2 = QGroupBox(self.tab_4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_6.addWidget(self.label_17)

        self.TextSSID5G = QLineEdit(self.groupBox_2)
        self.TextSSID5G.setObjectName(u"TextSSID5G")

        self.verticalLayout_6.addWidget(self.TextSSID5G)


        self.horizontalLayout_4.addLayout(self.verticalLayout_6)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_7.addWidget(self.label_6)

        self.TextPass5G = QLineEdit(self.groupBox_2)
        self.TextPass5G.setObjectName(u"TextPass5G")

        self.verticalLayout_7.addWidget(self.TextPass5G)


        self.horizontalLayout_4.addLayout(self.verticalLayout_7)


        self.verticalLayout_10.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.tab_4)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_8.addWidget(self.label_5)

        self.TextSSID = QLineEdit(self.groupBox)
        self.TextSSID.setObjectName(u"TextSSID")

        self.verticalLayout_8.addWidget(self.TextSSID)


        self.horizontalLayout_3.addLayout(self.verticalLayout_8)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_9.addWidget(self.label_4)

        self.TextPass = QLineEdit(self.groupBox)
        self.TextPass.setObjectName(u"TextPass")

        self.verticalLayout_9.addWidget(self.TextPass)


        self.horizontalLayout_3.addLayout(self.verticalLayout_9)


        self.verticalLayout_10.addWidget(self.groupBox)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_4)

        self.tabWidget.addTab(self.tab_4, "")
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

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.BtnAdd.setText(QCoreApplication.translate("Dialog", u"A\u00f1adir", None))
        self.BtnDelete.setText(QCoreApplication.translate("Dialog", u"Eliminar Seleccionado", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Empledo por defecto", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"T\u00e9cnicos", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Documento", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Pesta\u00f1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Google Sheets", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"SISTEMA DE ENERG\u00cdA", None))
        self.label_59.setText(QCoreApplication.translate("Dialog", u"C", None))
        self.label_60.setText(QCoreApplication.translate("Dialog", u"R", None))
        self.label_61.setText(QCoreApplication.translate("Dialog", u"N/A", None))
        self.label_62.setText(QCoreApplication.translate("Dialog", u"Nota", None))
        self.checkBox_92.setText(QCoreApplication.translate("Dialog", u"Cables de corriente", None))
        self.checkBox_93.setText(QCoreApplication.translate("Dialog", u"Contector de energ\u00eda", None))
        self.checkBox_94.setText(QCoreApplication.translate("Dialog", u"Ventilador fuente", None))
        self.checkBox_95.setText(QCoreApplication.translate("Dialog", u"Fuente de poder", None))
        self.checkBox_96.setText(QCoreApplication.translate("Dialog", u"Cargador", None))
        self.label_30.setText("")
        self.checkBox_97.setText(QCoreApplication.translate("Dialog", u"Bater\u00eda", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"SISTEMA DE REFRIGERACI\u00d3N", None))
        self.label_51.setText(QCoreApplication.translate("Dialog", u"C", None))
        self.label_52.setText(QCoreApplication.translate("Dialog", u"R", None))
        self.label_53.setText(QCoreApplication.translate("Dialog", u"N/A", None))
        self.label_54.setText(QCoreApplication.translate("Dialog", u"Nota", None))
        self.checkBox_72.setText(QCoreApplication.translate("Dialog", u"Ventiladores", None))
        self.checkBox_73.setText(QCoreApplication.translate("Dialog", u"Radiadores", None))
        self.checkBox_74.setText(QCoreApplication.translate("Dialog", u"Pasta t\u00e9rmica", None))
        self.checkBox_76.setText(QCoreApplication.translate("Dialog", u"Filtros de aire", None))
        self.label_31.setText("")
        self.label_16.setText(QCoreApplication.translate("Dialog", u"CONECTORES / PLUGS", None))
        self.label_43.setText(QCoreApplication.translate("Dialog", u"C", None))
        self.label_44.setText(QCoreApplication.translate("Dialog", u"R", None))
        self.label_45.setText(QCoreApplication.translate("Dialog", u"N/A", None))
        self.label_46.setText(QCoreApplication.translate("Dialog", u"Nota", None))
        self.checkBox_41.setText(QCoreApplication.translate("Dialog", u"USB", None))
        self.checkBox_42.setText(QCoreApplication.translate("Dialog", u"Ethernet", None))
        self.checkBox_43.setText(QCoreApplication.translate("Dialog", u"HDMI", None))
        self.checkBox_44.setText(QCoreApplication.translate("Dialog", u"DISPLAY PORT", None))
        self.checkBox_45.setText(QCoreApplication.translate("Dialog", u"VGA", None))
        self.checkBox_46.setText(QCoreApplication.translate("Dialog", u"JACK AUDIO", None))
        self.checkBox_47.setText(QCoreApplication.translate("Dialog", u"DVI", None))
        self.checkBox_48.setText(QCoreApplication.translate("Dialog", u"Lector de tajetas", None))
        self.label_32.setText("")
        self.label_21.setText(QCoreApplication.translate("Dialog", u"COMPONENTES EXTERNOS", None))
        self.label_63.setText(QCoreApplication.translate("Dialog", u"C", None))
        self.label_64.setText(QCoreApplication.translate("Dialog", u"R", None))
        self.label_65.setText(QCoreApplication.translate("Dialog", u"N/A", None))
        self.label_66.setText(QCoreApplication.translate("Dialog", u"Nota", None))
        self.checkBox_38.setText(QCoreApplication.translate("Dialog", u"C\u00e1mara", None))
        self.checkBox_39.setText(QCoreApplication.translate("Dialog", u"Pantalla", None))
        self.checkBox_40.setText(QCoreApplication.translate("Dialog", u"Teclado", None))
        self.checkBox_63.setText(QCoreApplication.translate("Dialog", u"Touchpad", None))
        self.checkBox_64.setText(QCoreApplication.translate("Dialog", u"Touchscreen", None))
        self.checkBox_65.setText(QCoreApplication.translate("Dialog", u"Lectora de discos", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"Slot de expaci\u00f3n", None))
        self.checkBox_11.setText(QCoreApplication.translate("Dialog", u"CheckBox", None))
        self.checkBox_67.setText(QCoreApplication.translate("Dialog", u"CheckBox", None))
        self.checkBox_68.setText(QCoreApplication.translate("Dialog", u"CheckBox", None))
        self.label_33.setText("")
        self.label_15.setText(QCoreApplication.translate("Dialog", u"COMPONENTES INTERNOS", None))
        self.label_35.setText(QCoreApplication.translate("Dialog", u"C", None))
        self.label_37.setText(QCoreApplication.translate("Dialog", u"R", None))
        self.label_38.setText(QCoreApplication.translate("Dialog", u"N/A", None))
        self.label_39.setText(QCoreApplication.translate("Dialog", u"Nota", None))
        self.checkBox_3.setText(QCoreApplication.translate("Dialog", u"Bocinas", None))
        self.checkBox_12.setText(QCoreApplication.translate("Dialog", u"RAM", None))
        self.checkBox_13.setText(QCoreApplication.translate("Dialog", u"DISCO DURO", None))
        self.checkBox_14.setText(QCoreApplication.translate("Dialog", u"SSD", None))
        self.checkBox_15.setText(QCoreApplication.translate("Dialog", u"Procesador", None))
        self.checkBox_16.setText(QCoreApplication.translate("Dialog", u"Bater\u00eda de reloj", None))
        self.checkBox_17.setText(QCoreApplication.translate("Dialog", u"Placa madre", None))
        self.checkBox_18.setText(QCoreApplication.translate("Dialog", u"Tarjeta de red", None))
        self.checkBox_19.setText(QCoreApplication.translate("Dialog", u"Tarjeta de v\u00eddeo", None))
        self.checkBox_34.setText(QCoreApplication.translate("Dialog", u"Bluetooth", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Slot de expaci\u00f3n", None))
        self.checkBox_10.setText(QCoreApplication.translate("Dialog", u"CheckBox", None))
        self.checkBox_35.setText(QCoreApplication.translate("Dialog", u"CheckBox", None))
        self.checkBox_4.setText(QCoreApplication.translate("Dialog", u"CheckBox", None))
        self.label_34.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"Valores por defecto", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Wifi 5G", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"SSID", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Contrase\u00f1a", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Wifi 2.5G", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"SSID", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Contrase\u00f1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Dialog", u"Wifi", None))
        self.BtnAddToSelectedPrograms.setText(QCoreApplication.translate("Dialog", u"Agregar", None))
        self.BtnDeleteFromSelectedPrograms.setText(QCoreApplication.translate("Dialog", u"Eliminar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("Dialog", u"Programas", None))
    # retranslateUi

