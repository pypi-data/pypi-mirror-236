# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'computation.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGroupBox,
    QHBoxLayout, QLabel, QListView, QScrollArea,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

class Ui_Computations(object):
    def setupUi(self, Computations):
        if not Computations.objectName():
            Computations.setObjectName(u"Computations")
        Computations.resize(533, 458)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Computations.sizePolicy().hasHeightForWidth())
        Computations.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Computations)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.cmbRegComps = QComboBox(Computations)
        self.cmbRegComps.setObjectName(u"cmbRegComps")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cmbRegComps.sizePolicy().hasHeightForWidth())
        self.cmbRegComps.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.cmbRegComps)

        self.grpRegDesc = QGroupBox(Computations)
        self.grpRegDesc.setObjectName(u"grpRegDesc")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.grpRegDesc.sizePolicy().hasHeightForWidth())
        self.grpRegDesc.setSizePolicy(sizePolicy2)
        self.horizontalLayout_3 = QHBoxLayout(self.grpRegDesc)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.grpRegDesc)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy3)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 511, 69))
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy4)
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lblCompDesc = QLabel(self.scrollAreaWidgetContents)
        self.lblCompDesc.setObjectName(u"lblCompDesc")
        sizePolicy4.setHeightForWidth(self.lblCompDesc.sizePolicy().hasHeightForWidth())
        self.lblCompDesc.setSizePolicy(sizePolicy4)
        self.lblCompDesc.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.lblCompDesc)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_3.addWidget(self.scrollArea)


        self.verticalLayout.addWidget(self.grpRegDesc)

        self.grpRegionSettings = QGroupBox(Computations)
        self.grpRegionSettings.setObjectName(u"grpRegionSettings")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.grpRegionSettings.sizePolicy().hasHeightForWidth())
        self.grpRegionSettings.setSizePolicy(sizePolicy5)

        self.verticalLayout.addWidget(self.grpRegionSettings)

        self.grpRegRestrict = QGroupBox(Computations)
        self.grpRegRestrict.setObjectName(u"grpRegRestrict")
        sizePolicy5.setHeightForWidth(self.grpRegRestrict.sizePolicy().hasHeightForWidth())
        self.grpRegRestrict.setSizePolicy(sizePolicy5)
        self.verticalLayout_4 = QVBoxLayout(self.grpRegRestrict)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.regRestrictView = QListView(self.grpRegRestrict)
        self.regRestrictView.setObjectName(u"regRestrictView")
        sizePolicy5.setHeightForWidth(self.regRestrictView.sizePolicy().hasHeightForWidth())
        self.regRestrictView.setSizePolicy(sizePolicy5)
        self.regRestrictView.setSelectionMode(QAbstractItemView.MultiSelection)
        self.regRestrictView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_4.addWidget(self.regRestrictView)


        self.verticalLayout.addWidget(self.grpRegRestrict)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnRegApply = QToolButton(Computations)
        self.btnRegApply.setObjectName(u"btnRegApply")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.btnRegApply.sizePolicy().hasHeightForWidth())
        self.btnRegApply.setSizePolicy(sizePolicy6)

        self.horizontalLayout_2.addWidget(self.btnRegApply)

        self.btnRegApplyAll = QToolButton(Computations)
        self.btnRegApplyAll.setObjectName(u"btnRegApplyAll")
        sizePolicy6.setHeightForWidth(self.btnRegApplyAll.sizePolicy().hasHeightForWidth())
        self.btnRegApplyAll.setSizePolicy(sizePolicy6)
        self.btnRegApplyAll.setPopupMode(QToolButton.MenuButtonPopup)
        self.btnRegApplyAll.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.btnRegApplyAll)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Computations)

        QMetaObject.connectSlotsByName(Computations)
    # setupUi

    def retranslateUi(self, Computations):
        Computations.setWindowTitle(QCoreApplication.translate("Computations", u"Form", None))
        self.grpRegDesc.setTitle(QCoreApplication.translate("Computations", u"Description", None))
        self.lblCompDesc.setText("")
        self.grpRegionSettings.setTitle(QCoreApplication.translate("Computations", u"Settings", None))
        self.grpRegRestrict.setTitle(QCoreApplication.translate("Computations", u"Apply to regions", None))
        self.btnRegApply.setText(QCoreApplication.translate("Computations", u"Apply to selected", None))
        self.btnRegApplyAll.setText(QCoreApplication.translate("Computations", u"Apply to all", None))
    # retranslateUi

