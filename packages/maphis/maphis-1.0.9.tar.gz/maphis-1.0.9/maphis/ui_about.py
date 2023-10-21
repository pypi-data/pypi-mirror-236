# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_AboutMAPHIS(object):
    def setupUi(self, AboutMAPHIS):
        if not AboutMAPHIS.objectName():
            AboutMAPHIS.setObjectName(u"AboutMAPHIS")
        AboutMAPHIS.resize(432, 298)
        self.horizontalLayout = QHBoxLayout(AboutMAPHIS)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.lblMAPHIS = QLabel(AboutMAPHIS)
        self.lblMAPHIS.setObjectName(u"lblMAPHIS")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMAPHIS.sizePolicy().hasHeightForWidth())
        self.lblMAPHIS.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.lblMAPHIS, 0, Qt.AlignHCenter)

        self.lblVersion = QLabel(AboutMAPHIS)
        self.lblVersion.setObjectName(u"lblVersion")
        sizePolicy.setHeightForWidth(self.lblVersion.sizePolicy().hasHeightForWidth())
        self.lblVersion.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.lblVersion, 0, Qt.AlignHCenter)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.lblLicense = QLabel(AboutMAPHIS)
        self.lblLicense.setObjectName(u"lblLicense")
        self.lblLicense.setTextFormat(Qt.RichText)

        self.verticalLayout.addWidget(self.lblLicense, 0, Qt.AlignHCenter)

        self.lblWebsite = QLabel(AboutMAPHIS)
        self.lblWebsite.setObjectName(u"lblWebsite")
        self.lblWebsite.setTextFormat(Qt.MarkdownText)
        self.lblWebsite.setOpenExternalLinks(True)
        self.lblWebsite.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.lblWebsite, 0, Qt.AlignHCenter)

        self.lblFAQ = QLabel(AboutMAPHIS)
        self.lblFAQ.setObjectName(u"lblFAQ")
        self.lblFAQ.setTextFormat(Qt.MarkdownText)
        self.lblFAQ.setAlignment(Qt.AlignCenter)
        self.lblFAQ.setOpenExternalLinks(True)
        self.lblFAQ.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.lblFAQ, 0, Qt.AlignHCenter)

        self.lblProjectRepoURL = QLabel(AboutMAPHIS)
        self.lblProjectRepoURL.setObjectName(u"lblProjectRepoURL")
        self.lblProjectRepoURL.setTextFormat(Qt.MarkdownText)
        self.lblProjectRepoURL.setOpenExternalLinks(True)
        self.lblProjectRepoURL.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.lblProjectRepoURL, 0, Qt.AlignHCenter)

        self.gridAuthors = QGroupBox(AboutMAPHIS)
        self.gridAuthors.setObjectName(u"gridAuthors")
        self.gridLayout_2 = QGridLayout(self.gridAuthors)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_5 = QLabel(self.gridAuthors)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)

        self.lblMailPekarM = QLabel(self.gridAuthors)
        self.lblMailPekarM.setObjectName(u"lblMailPekarM")
        self.lblMailPekarM.setTextFormat(Qt.MarkdownText)
        self.lblMailPekarM.setOpenExternalLinks(True)
        self.lblMailPekarM.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout_2.addWidget(self.lblMailPekarM, 2, 1, 1, 1)

        self.label_7 = QLabel(self.gridAuthors)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)

        self.label = QLabel(self.gridAuthors)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(self.gridAuthors)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.lblMailStepkaK = QLabel(self.gridAuthors)
        self.lblMailStepkaK.setObjectName(u"lblMailStepkaK")
        self.lblMailStepkaK.setTextFormat(Qt.MarkdownText)
        self.lblMailStepkaK.setOpenExternalLinks(True)
        self.lblMailStepkaK.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout_2.addWidget(self.lblMailStepkaK, 4, 1, 1, 1)

        self.lblMailMatulaP = QLabel(self.gridAuthors)
        self.lblMailMatulaP.setObjectName(u"lblMailMatulaP")
        self.lblMailMatulaP.setTextFormat(Qt.MarkdownText)
        self.lblMailMatulaP.setOpenExternalLinks(True)
        self.lblMailMatulaP.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout_2.addWidget(self.lblMailMatulaP, 0, 1, 1, 1)

        self.label_9 = QLabel(self.gridAuthors)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 4, 0, 1, 1)

        self.lblMailMrazR = QLabel(self.gridAuthors)
        self.lblMailMrazR.setObjectName(u"lblMailMrazR")
        self.lblMailMrazR.setTextFormat(Qt.MarkdownText)
        self.lblMailMrazR.setOpenExternalLinks(True)
        self.lblMailMrazR.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout_2.addWidget(self.lblMailMrazR, 1, 1, 1, 1)

        self.lblMailPekarS = QLabel(self.gridAuthors)
        self.lblMailPekarS.setObjectName(u"lblMailPekarS")
        self.lblMailPekarS.setTextFormat(Qt.MarkdownText)
        self.lblMailPekarS.setOpenExternalLinks(True)
        self.lblMailPekarS.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout_2.addWidget(self.lblMailPekarS, 3, 1, 1, 1)


        self.verticalLayout.addWidget(self.gridAuthors)

        self.lblCBIA = QLabel(AboutMAPHIS)
        self.lblCBIA.setObjectName(u"lblCBIA")
        self.lblCBIA.setTextFormat(Qt.MarkdownText)
        self.lblCBIA.setOpenExternalLinks(True)
        self.lblCBIA.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.lblCBIA, 0, Qt.AlignHCenter)


        self.horizontalLayout.addLayout(self.verticalLayout)

#if QT_CONFIG(shortcut)
        self.lblWebsite.setBuddy(self.lblFAQ)
        self.lblFAQ.setBuddy(self.lblProjectRepoURL)
        self.lblProjectRepoURL.setBuddy(self.lblMailMatulaP)
        self.lblMailPekarM.setBuddy(self.lblMailPekarS)
        self.lblMailStepkaK.setBuddy(self.lblCBIA)
        self.lblMailMatulaP.setBuddy(self.lblMailMrazR)
        self.lblMailMrazR.setBuddy(self.lblMailPekarM)
        self.lblMailPekarS.setBuddy(self.lblMailStepkaK)
        self.lblCBIA.setBuddy(self.lblWebsite)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(AboutMAPHIS)

        QMetaObject.connectSlotsByName(AboutMAPHIS)
    # setupUi

    def retranslateUi(self, AboutMAPHIS):
        AboutMAPHIS.setWindowTitle(QCoreApplication.translate("AboutMAPHIS", u"About MAPHIS", None))
        self.lblMAPHIS.setText(QCoreApplication.translate("AboutMAPHIS", u"MAPHIS", None))
        self.lblVersion.setText(QCoreApplication.translate("AboutMAPHIS", u"<version>", None))
        self.lblLicense.setText(QCoreApplication.translate("AboutMAPHIS", u"license", None))
        self.lblWebsite.setText(QCoreApplication.translate("AboutMAPHIS", u"Website: https://maphis.fi.muni.cz", None))
        self.lblFAQ.setText(QCoreApplication.translate("AboutMAPHIS", u"Frequently asked questions: https://maphis.fi.muni.cz/FAQ/", None))
        self.lblProjectRepoURL.setText(QCoreApplication.translate("AboutMAPHIS", u"Project repository: https://gitlab.fi.muni.cz/cbia/maphis", None))
        self.gridAuthors.setTitle(QCoreApplication.translate("AboutMAPHIS", u"Authors", None))
        self.label_5.setText(QCoreApplication.translate("AboutMAPHIS", u"Mat\u011bj Pek\u00e1r", None))
        self.lblMailPekarM.setText(QCoreApplication.translate("AboutMAPHIS", u"matej.pekar120@gmail.com", None))
        self.label_7.setText(QCoreApplication.translate("AboutMAPHIS", u"Stano Pek\u00e1r", None))
        self.label.setText(QCoreApplication.translate("AboutMAPHIS", u"Petr Matula", None))
        self.label_3.setText(QCoreApplication.translate("AboutMAPHIS", u"Radoslav Mr\u00e1z", None))
        self.lblMailStepkaK.setText(QCoreApplication.translate("AboutMAPHIS", u"172454@mail.muni.cz", None))
        self.lblMailMatulaP.setText(QCoreApplication.translate("AboutMAPHIS", u"pem@fi.muni.cz", None))
        self.label_9.setText(QCoreApplication.translate("AboutMAPHIS", u"Karel \u0160t\u011bpka", None))
        self.lblMailMrazR.setText(QCoreApplication.translate("AboutMAPHIS", u"radoslav.mraz95@gmail.com", None))
        self.lblMailPekarS.setText(QCoreApplication.translate("AboutMAPHIS", u"56765@muni.cz", None))
        self.lblCBIA.setText(QCoreApplication.translate("AboutMAPHIS", u"Developed at CBIA https://cbia.fi.muni.cz", None))
    # retranslateUi

