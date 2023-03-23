# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FileSearchEngine.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                          QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient,
                         QCursor, QFont, QFontDatabase, QGradient,
                         QIcon, QImage, QKeySequence, QLinearGradient,
                         QPainter, QPalette, QPixmap, QRadialGradient,
                         QTransform)
from PyQt5.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QGridLayout,
                             QGroupBox, QHBoxLayout, QHeaderView, QLabel,
                             QLineEdit, QMainWindow, QMenu, QMenuBar,
                             QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
                             QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QAction


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(760, 594)
        icon = QIcon()
        icon.addFile(u"icons/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"QTreeView {\n"
                                 "	border:none\n"
                                 "}\n"
                                 "")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionHelp = QAction(MainWindow)
        self.actionHelp.setObjectName(u"actionHelp")
        self.actionSearchType = QAction(MainWindow)
        self.actionSearchType.setObjectName(u"actionSearchType")
        icon1 = QIcon()
        icon1.addFile(u"icons/radio-circle-marked.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSearchType.setIcon(icon1)
        self.actionSearchName = QAction(MainWindow)
        self.actionSearchName.setObjectName(u"actionSearchName")
        icon2 = QIcon()
        icon2.addFile(u"icons/radio-circle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSearchName.setIcon(icon2)
        self.actionTextViewer = QAction(MainWindow)
        self.actionTextViewer.setObjectName(u"actionTextViewer")
        self.actionPlayerViewer = QAction(MainWindow)
        self.actionPlayerViewer.setObjectName(u"actionPlayerViewer")
        self.actionImageViewer = QAction(MainWindow)
        self.actionImageViewer.setObjectName(u"actionImageViewer")
        self.actionSearchWeb = QAction(MainWindow)
        self.actionSearchWeb.setObjectName(u"actionSearchWeb")
        self.actionSearchWeb.setIcon(icon2)
        self.actionSearchKey = QAction(MainWindow)
        self.actionSearchKey.setObjectName(u"actionSearchKey")
        self.actionSearchKey.setIcon(icon2)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setEnabled(True)
        font = QFont()
        font.setStyleStrategy(QFont.PreferDefault)
        self.groupBox.setFont(font)
        self.groupBox.setMouseTracking(False)
        self.groupBox.setTabletTracking(False)
        self.groupBox.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.groupBox.setLayoutDirection(Qt.LeftToRight)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.groupBox.setFlat(False)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.upLineEdit = QLineEdit(self.groupBox)
        self.upLineEdit.setObjectName(u"upLineEdit")

        self.gridLayout.addWidget(self.upLineEdit, 0, 1, 1, 1)

        self.downLineEdit = QLineEdit(self.groupBox)
        self.downLineEdit.setObjectName(u"downLineEdit")

        self.gridLayout.addWidget(self.downLineEdit, 1, 1, 1, 1)

        self.downLabel = QLabel(self.groupBox)
        self.downLabel.setObjectName(u"downLabel")
        font1 = QFont()
        font1.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font1.setPointSize(11)
        font1.setBold(True)
        self.downLabel.setFont(font1)

        self.gridLayout.addWidget(self.downLabel, 1, 0, 1, 1)

        self.upLabel = QLabel(self.groupBox)
        self.upLabel.setObjectName(u"upLabel")
        self.upLabel.setFont(font1)

        self.gridLayout.addWidget(self.upLabel, 0, 0, 1, 1)

        self.searchButton = QPushButton(self.groupBox)
        self.searchButton.setObjectName(u"searchButton")

        self.gridLayout.addWidget(self.searchButton, 1, 2, 1, 1)

        self.browseButton = QPushButton(self.groupBox)
        self.browseButton.setObjectName(u"browseButton")

        self.gridLayout.addWidget(self.browseButton, 0, 2, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout.addWidget(self.groupBox)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.outputTreeWidget = QTreeWidget(self.centralwidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignTrailing | Qt.AlignVCenter);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignLeading | Qt.AlignVCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignLeading | Qt.AlignVCenter);
        self.outputTreeWidget.setHeaderItem(__qtreewidgetitem)
        self.outputTreeWidget.setObjectName(u"outputTreeWidget")
        self.outputTreeWidget.setEnabled(True)
        self.outputTreeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.outputTreeWidget.setProperty("showDropIndicator", True)
        self.outputTreeWidget.setIndentation(20)
        self.outputTreeWidget.setRootIsDecorated(False)
        self.outputTreeWidget.setUniformRowHeights(False)
        self.outputTreeWidget.setItemsExpandable(True)
        self.outputTreeWidget.setSortingEnabled(False)
        self.outputTreeWidget.setAnimated(False)
        self.outputTreeWidget.setAllColumnsShowFocus(False)
        self.outputTreeWidget.setHeaderHidden(False)
        self.outputTreeWidget.setExpandsOnDoubleClick(True)
        self.outputTreeWidget.setColumnCount(5)
        self.outputTreeWidget.header().setVisible(True)
        self.outputTreeWidget.header().setCascadingSectionResizes(False)
        self.outputTreeWidget.header().setMinimumSectionSize(25)
        self.outputTreeWidget.header().setDefaultSectionSize(100)
        self.outputTreeWidget.header().setHighlightSections(False)

        self.verticalLayout_2.addWidget(self.outputTreeWidget)

        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 760, 22))
        self.searchMenu = QMenu(self.menuBar)
        self.searchMenu.setObjectName(u"searchMenu")
        self.toolsMenu = QMenu(self.menuBar)
        self.toolsMenu.setObjectName(u"toolsMenu")
        self.helpMenu = QMenu(self.menuBar)
        self.helpMenu.setObjectName(u"helpMenu")
        self.aboutMenu = QMenu(self.menuBar)
        self.aboutMenu.setObjectName(u"aboutMenu")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.searchMenu.menuAction())
        self.menuBar.addAction(self.toolsMenu.menuAction())
        self.menuBar.addAction(self.helpMenu.menuAction())
        self.menuBar.addAction(self.aboutMenu.menuAction())
        self.searchMenu.addAction(self.actionSearchType)
        self.searchMenu.addAction(self.actionSearchName)
        self.searchMenu.addAction(self.actionSearchWeb)
        self.searchMenu.addAction(self.actionSearchKey)
        self.toolsMenu.addAction(self.actionTextViewer)
        self.toolsMenu.addAction(self.actionPlayerViewer)
        self.toolsMenu.addAction(self.actionImageViewer)
        self.helpMenu.addAction(self.actionHelp)
        self.aboutMenu.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Anything", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e\u4f5c\u8005", None))
        # if QT_CONFIG(shortcut)
        self.actionAbout.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+A", None))
        # endif // QT_CONFIG(shortcut)
        self.actionHelp.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u770b\u7528\u6cd5", None))
        # if QT_CONFIG(shortcut)
        self.actionHelp.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+H", None))
        # endif // QT_CONFIG(shortcut)
        self.actionSearchType.setText(QCoreApplication.translate("MainWindow", u"\u7c7b\u578b\u641c\u7d22", None))
        self.actionSearchName.setText(QCoreApplication.translate("MainWindow", u"\u540d\u79f0\u641c\u7d22", None))
        self.actionTextViewer.setText(QCoreApplication.translate("MainWindow", u"\u6587\u672c\u67e5\u770b\u5668", None))
        self.actionPlayerViewer.setText(
            QCoreApplication.translate("MainWindow", u"\u97f3\u9891\u64ad\u653e\u5668", None))
        self.actionImageViewer.setText(
            QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u67e5\u770b\u5668", None))
        self.actionSearchWeb.setText(QCoreApplication.translate("MainWindow", u"Web\u641c\u7d22", None))
        self.actionSearchKey.setText(
            QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u5173\u952e\u5b57\u641c\u7d22", None))
        # if QT_CONFIG(accessibility)
        self.groupBox.setAccessibleName("")
        # endif // QT_CONFIG(accessibility)
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow",
                                                          u"\u586b\u5199\u5185\u5bb9\u540e\u70b9\u51fb\u5f00\u59cb\u641c\u7d22",
                                                          None))
        self.upLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow",
                                                                      u"\u8bf7\u8f93\u5165\u6587\u4ef6\u8def\u5f84\uff08\u9ed8\u8ba4C:/\uff09",
                                                                      None))
        self.downLineEdit.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u6587\u4ef6\u7c7b\u578b\uff0c\u5217\u5982exe",
                                       None))
        self.downLabel.setText(QCoreApplication.translate("MainWindow", u"\u7c7b\u578b\uff1a", None))
        self.upLabel.setText(QCoreApplication.translate("MainWindow", u"\u8def\u5f84\uff1a", None))
        self.searchButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u641c\u7d22", None))
        self.browseButton.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        ___qtreewidgetitem = self.outputTreeWidget.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MainWindow", u"\u8def\u5f84", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"\u4fee\u6539\u65f6\u95f4", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"\u5927\u5c0f", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"\u7c7b\u578b", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u540d\u79f0", None));
        self.searchMenu.setTitle(QCoreApplication.translate("MainWindow", u"\u641c\u7d22(&S)", None))
        self.toolsMenu.setTitle(QCoreApplication.translate("MainWindow", u"\u5de5\u5177(&T)", None))
        self.helpMenu.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9(&H)", None))
        self.aboutMenu.setTitle(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e(&A)", None))
    # retranslateUi
