# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QGroupBox, QLabel,
    QPushButton, QSizePolicy, QWidget)

class Ui_MYAPP(object):
    def setupUi(self, MYAPP):
        if not MYAPP.objectName():
            MYAPP.setObjectName(u"MYAPP")
        MYAPP.resize(800, 600)
        self.SAMSUNGLOGO = QLabel(MYAPP)
        self.SAMSUNGLOGO.setObjectName(u"SAMSUNGLOGO")
        self.SAMSUNGLOGO.setGeometry(QRect(0, 0, 161, 41))
        self.SAMSUNGLOGO.setPixmap(QPixmap(u"SAMSUNG_LOGO_w128.png"))
        self.SIC_LOGO = QLabel(MYAPP)
        self.SIC_LOGO.setObjectName(u"SIC_LOGO")
        self.SIC_LOGO.setGeometry(QRect(10, 30, 151, 16))
        font = QFont()
        font.setBold(True)
        self.SIC_LOGO.setFont(font)
        self.groupBox = QGroupBox(MYAPP)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 50, 721, 31))
        self.project_name = QLabel(self.groupBox)
        self.project_name.setObjectName(u"project_name")
        self.project_name.setGeometry(QRect(10, 0, 631, 31))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setUnderline(False)
        self.project_name.setFont(font1)
        self.Widget = QGroupBox(MYAPP)
        self.Widget.setObjectName(u"Widget")
        self.Widget.setGeometry(QRect(390, 90, 341, 261))
        self.calendarWidget = QCalendarWidget(self.Widget)
        self.calendarWidget.setObjectName(u"calendarWidget")
        self.calendarWidget.setGeometry(QRect(20, 30, 301, 161))
        self.temp_title = QLabel(self.Widget)
        self.temp_title.setObjectName(u"temp_title")
        self.temp_title.setGeometry(QRect(20, 200, 91, 16))
        self.temp_title.setFont(font)
        self.humid_title = QLabel(self.Widget)
        self.humid_title.setObjectName(u"humid_title")
        self.humid_title.setGeometry(QRect(20, 220, 81, 16))
        self.humid_title.setFont(font)
        self.temp_value = QLabel(self.Widget)
        self.temp_value.setObjectName(u"temp_value")
        self.temp_value.setGeometry(QRect(120, 200, 91, 16))
        font2 = QFont()
        font2.setBold(False)
        self.temp_value.setFont(font2)
        self.humid_value = QLabel(self.Widget)
        self.humid_value.setObjectName(u"humid_value")
        self.humid_value.setGeometry(QRect(120, 220, 91, 16))
        self.humid_value.setFont(font2)
        self.CO2_value = QLabel(self.Widget)
        self.CO2_value.setObjectName(u"CO2_value")
        self.CO2_value.setGeometry(QRect(120, 240, 91, 16))
        self.CO2_value.setFont(font2)
        self.CO2_title = QLabel(self.Widget)
        self.CO2_title.setObjectName(u"CO2_title")
        self.CO2_title.setGeometry(QRect(20, 240, 81, 16))
        self.CO2_title.setFont(font)
        self.FullScreenButton = QPushButton(self.Widget)
        self.FullScreenButton.setObjectName(u"FullScreenButton")
        self.FullScreenButton.setGeometry(QRect(240, 230, 81, 22))
        self.RefreshButton = QPushButton(self.Widget)
        self.RefreshButton.setObjectName(u"RefreshButton")
        self.RefreshButton.setGeometry(QRect(240, 200, 80, 22))
        self.groupBox_3 = QGroupBox(MYAPP)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 90, 361, 281))
        self.Camera_Label = QLabel(self.groupBox_3)
        self.Camera_Label.setObjectName(u"Camera_Label")
        self.Camera_Label.setGeometry(QRect(30, 30, 301, 211))
        font3 = QFont()
        font3.setUnderline(False)
        self.Camera_Label.setFont(font3)
        self.People_Detection = QPushButton(self.groupBox_3)
        self.People_Detection.setObjectName(u"People_Detection")
        self.People_Detection.setGeometry(QRect(20, 250, 131, 22))
        self.Camera_Control = QPushButton(self.groupBox_3)
        self.Camera_Control.setObjectName(u"Camera_Control")
        self.Camera_Control.setGeometry(QRect(210, 250, 131, 22))
        self.Announcement = QGroupBox(MYAPP)
        self.Announcement.setObjectName(u"Announcement")
        self.Announcement.setGeometry(QRect(10, 380, 361, 91))
        self.Announcement.setAutoFillBackground(True)
        self.Notification1_Value = QLabel(self.Announcement)
        self.Notification1_Value.setObjectName(u"Notification1_Value")
        self.Notification1_Value.setGeometry(QRect(10, 40, 311, 21))
        self.ServerConnection_Title = QLabel(self.Announcement)
        self.ServerConnection_Title.setObjectName(u"ServerConnection_Title")
        self.ServerConnection_Title.setGeometry(QRect(10, 20, 101, 16))
        self.ServerConnection_Title.setFont(font)
        self.ServerConnection_Value = QLabel(self.Announcement)
        self.ServerConnection_Value.setObjectName(u"ServerConnection_Value")
        self.ServerConnection_Value.setGeometry(QRect(110, 20, 241, 16))
        self.Notification2_Value = QLabel(self.Announcement)
        self.Notification2_Value.setObjectName(u"Notification2_Value")
        self.Notification2_Value.setGeometry(QRect(10, 60, 311, 21))
        self.sysconf = QGroupBox(MYAPP)
        self.sysconf.setObjectName(u"sysconf")
        self.sysconf.setGeometry(QRect(390, 360, 341, 111))
        self.SetResetFireAlert_Button = QPushButton(self.sysconf)
        self.SetResetFireAlert_Button.setObjectName(u"SetResetFireAlert_Button")
        self.SetResetFireAlert_Button.setGeometry(QRect(180, 50, 151, 22))
        self.ClearNotiButton = QPushButton(self.sysconf)
        self.ClearNotiButton.setObjectName(u"ClearNotiButton")
        self.ClearNotiButton.setGeometry(QRect(20, 50, 141, 22))
        self.AutoStartFireAlert = QPushButton(self.sysconf)
        self.AutoStartFireAlert.setObjectName(u"AutoStartFireAlert")
        self.AutoStartFireAlert.setGeometry(QRect(20, 80, 141, 22))
        self.AutoStopFireAlert = QPushButton(self.sysconf)
        self.AutoStopFireAlert.setObjectName(u"AutoStopFireAlert")
        self.AutoStopFireAlert.setGeometry(QRect(180, 80, 151, 22))
        self.ServerSyncButton = QPushButton(self.sysconf)
        self.ServerSyncButton.setObjectName(u"ServerSyncButton")
        self.ServerSyncButton.setGeometry(QRect(20, 20, 141, 22))
        self.RebootButton = QPushButton(self.sysconf)
        self.RebootButton.setObjectName(u"RebootButton")
        self.RebootButton.setGeometry(QRect(180, 20, 151, 22))
        self.FireWarningBar = QLabel(MYAPP)
        self.FireWarningBar.setObjectName(u"FireWarningBar")
        self.FireWarningBar.setGeometry(QRect(180, 10, 551, 31))
        self.FireWarningBar.setPixmap(QPixmap(u"red.jpg"))

        self.retranslateUi(MYAPP)

        QMetaObject.connectSlotsByName(MYAPP)
    # setupUi

    def retranslateUi(self, MYAPP):
        MYAPP.setWindowTitle(QCoreApplication.translate("MYAPP", u"SIC IoT - CapstoneProjectApp", None))
        self.SAMSUNGLOGO.setText("")
        self.SIC_LOGO.setText(QCoreApplication.translate("MYAPP", u"INNOVATION CAMPUS", None))
        self.groupBox.setTitle("")
        self.project_name.setText(QCoreApplication.translate("MYAPP", u"H\u1ec6 TH\u1ed0NG GI\u00c1M S\u00c1T V\u00c0 C\u1ea2NH B\u00c1O CH\u00c1Y CHO C\u0102N H\u1ed8 CHUNG C\u01af.", None))
        self.Widget.setTitle(QCoreApplication.translate("MYAPP", u"Widget", None))
        self.temp_title.setText(QCoreApplication.translate("MYAPP", u"Temperature:", None))
        self.humid_title.setText(QCoreApplication.translate("MYAPP", u"Humidity:", None))
        self.temp_value.setText(QCoreApplication.translate("MYAPP", u"n/a", None))
        self.humid_value.setText(QCoreApplication.translate("MYAPP", u"n/a", None))
        self.CO2_value.setText(QCoreApplication.translate("MYAPP", u"n/a", None))
        self.CO2_title.setText(QCoreApplication.translate("MYAPP", u"CO2:", None))
        self.FullScreenButton.setText(QCoreApplication.translate("MYAPP", u"Full Screen", None))
        self.RefreshButton.setText(QCoreApplication.translate("MYAPP", u"Refresh", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MYAPP", u"Camera", None))
        self.Camera_Label.setText(QCoreApplication.translate("MYAPP", u"No video", None))
        self.People_Detection.setText(QCoreApplication.translate("MYAPP", u"People Detection", None))
        self.Camera_Control.setText(QCoreApplication.translate("MYAPP", u"Start/Stop Camera", None))
        self.Announcement.setTitle(QCoreApplication.translate("MYAPP", u"System Status", None))
        self.Notification1_Value.setText(QCoreApplication.translate("MYAPP", u"<notification 1>", None))
        self.ServerConnection_Title.setText(QCoreApplication.translate("MYAPP", u"Server Status:", None))
        self.ServerConnection_Value.setText(QCoreApplication.translate("MYAPP", u"Disconnected", None))
        self.Notification2_Value.setText(QCoreApplication.translate("MYAPP", u"<notification 2>", None))
        self.sysconf.setTitle(QCoreApplication.translate("MYAPP", u"System configuration", None))
        self.SetResetFireAlert_Button.setText(QCoreApplication.translate("MYAPP", u"Set/Reset FireAlert", None))
        self.ClearNotiButton.setText(QCoreApplication.translate("MYAPP", u"Clear Notification", None))
        self.AutoStartFireAlert.setText(QCoreApplication.translate("MYAPP", u"Auto Start Fire Alert", None))
        self.AutoStopFireAlert.setText(QCoreApplication.translate("MYAPP", u"Auto Stop Fire Alert", None))
        self.ServerSyncButton.setText(QCoreApplication.translate("MYAPP", u"Server SYNC", None))
        self.RebootButton.setText(QCoreApplication.translate("MYAPP", u"Reboot", None))
        self.FireWarningBar.setText("")
    # retranslateUi

