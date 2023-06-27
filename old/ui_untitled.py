# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledPmonca.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(459, 742)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setFamily(u"\u9ed1\u4f53")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setFrameShape(QFrame.Box)
        self.title.setFrameShadow(QFrame.Plain)
        self.title.setLineWidth(1)
        self.title.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.title, 0, 0, 1, 2)

        self.levelLabel = QLabel(self.centralwidget)
        self.levelLabel.setObjectName(u"levelLabel")
        font1 = QFont()
        font1.setFamily(u"\u9ed1\u4f53")
        font1.setPointSize(7)
        self.levelLabel.setFont(font1)
        self.levelLabel.setFrameShape(QFrame.Panel)
        self.levelLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.levelLabel, 1, 0, 1, 1)

        self.levelDrop = QComboBox(self.centralwidget)
        self.levelDrop.setObjectName(u"levelDrop")

        self.gridLayout.addWidget(self.levelDrop, 1, 1, 1, 1)

        self.subjectLabel = QLabel(self.centralwidget)
        self.subjectLabel.setObjectName(u"subjectLabel")
        self.subjectLabel.setFont(font1)
        self.subjectLabel.setFrameShape(QFrame.Panel)
        self.subjectLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.subjectLabel, 2, 0, 1, 1)

        self.subjectDrop = QComboBox(self.centralwidget)
        self.subjectDrop.setObjectName(u"subjectDrop")

        self.gridLayout.addWidget(self.subjectDrop, 2, 1, 1, 1)

        self.yearLabel = QLabel(self.centralwidget)
        self.yearLabel.setObjectName(u"yearLabel")
        self.yearLabel.setFont(font1)
        self.yearLabel.setFrameShape(QFrame.Panel)
        self.yearLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.yearLabel, 3, 0, 1, 1)

        self.yearDrop = QComboBox(self.centralwidget)
        self.yearDrop.setObjectName(u"yearDrop")

        self.gridLayout.addWidget(self.yearDrop, 3, 1, 1, 1)

        self.paperLabel = QLabel(self.centralwidget)
        self.paperLabel.setObjectName(u"paperLabel")
        self.paperLabel.setFont(font1)
        self.paperLabel.setFrameShape(QFrame.Panel)
        self.paperLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.paperLabel, 4, 0, 1, 1)

        self.paperDrop = QComboBox(self.centralwidget)
        self.paperDrop.setObjectName(u"paperDrop")

        self.gridLayout.addWidget(self.paperDrop, 4, 1, 1, 1)

        self.variantLabel = QLabel(self.centralwidget)
        self.variantLabel.setObjectName(u"variantLabel")
        self.variantLabel.setFont(font1)
        self.variantLabel.setFrameShape(QFrame.Panel)
        self.variantLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.variantLabel, 5, 0, 1, 1)

        self.variantDrop = QComboBox(self.centralwidget)
        self.variantDrop.setObjectName(u"variantDrop")

        self.gridLayout.addWidget(self.variantDrop, 5, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.msCheck_2 = QCheckBox(self.centralwidget)
        self.msCheck_2.setObjectName(u"msCheck_2")
        font2 = QFont()
        font2.setFamily(u"\u9ed1\u4f53")
        self.msCheck_2.setFont(font2)

        self.horizontalLayout.addWidget(self.msCheck_2)

        self.qpCheck = QCheckBox(self.centralwidget)
        self.qpCheck.setObjectName(u"qpCheck")
        self.qpCheck.setFont(font2)

        self.horizontalLayout.addWidget(self.qpCheck)

        self.msCheck = QCheckBox(self.centralwidget)
        self.msCheck.setObjectName(u"msCheck")
        self.msCheck.setFont(font2)

        self.horizontalLayout.addWidget(self.msCheck)

        self.msCheck_3 = QCheckBox(self.centralwidget)
        self.msCheck_3.setObjectName(u"msCheck_3")
        self.msCheck_3.setFont(font2)

        self.horizontalLayout.addWidget(self.msCheck_3)

        self.msCheck_4 = QCheckBox(self.centralwidget)
        self.msCheck_4.setObjectName(u"msCheck_4")
        self.msCheck_4.setFont(font2)

        self.horizontalLayout.addWidget(self.msCheck_4)


        self.gridLayout.addLayout(self.horizontalLayout, 6, 0, 1, 2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.addButton = QPushButton(self.centralwidget)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setFont(font2)

        self.verticalLayout.addWidget(self.addButton)

        self.deleteButton = QPushButton(self.centralwidget)
        self.deleteButton.setObjectName(u"deleteButton")
        self.deleteButton.setFont(font2)

        self.verticalLayout.addWidget(self.deleteButton)

        self.urlList = QListWidget(self.centralwidget)
        self.urlList.setObjectName(u"urlList")

        self.verticalLayout.addWidget(self.urlList)

        self.downloadButton = QPushButton(self.centralwidget)
        self.downloadButton.setObjectName(u"downloadButton")
        self.downloadButton.setFont(font2)

        self.verticalLayout.addWidget(self.downloadButton)


        self.gridLayout.addLayout(self.verticalLayout, 7, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 459, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"GCE Dowloader", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"GCE Downloader", None))
        self.levelLabel.setText(QCoreApplication.translate("MainWindow", u"IGCSE/ALevel", None))
        self.subjectLabel.setText(QCoreApplication.translate("MainWindow", u"Subject", None))
        self.yearLabel.setText(QCoreApplication.translate("MainWindow", u"Year", None))
        self.paperLabel.setText(QCoreApplication.translate("MainWindow", u"Paper", None))
        self.variantLabel.setText(QCoreApplication.translate("MainWindow", u"Variant", None))
        self.msCheck_2.setText(QCoreApplication.translate("MainWindow", u"SF", None))
        self.qpCheck.setText(QCoreApplication.translate("MainWindow", u"QP", None))
        self.msCheck.setText(QCoreApplication.translate("MainWindow", u"MS", None))
        self.msCheck_3.setText(QCoreApplication.translate("MainWindow", u"IN", None))
        self.msCheck_4.setText(QCoreApplication.translate("MainWindow", u"I2", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"Add to list", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", u"Delete last item", None))
        self.downloadButton.setText(QCoreApplication.translate("MainWindow", u"Download!", None))
    # retranslateUi

Ui_MainWindow.