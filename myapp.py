# This Python file uses the following encoding: utf-8
import sys
import time
import PySide6.QtGui

from picamera2 import Picamera2, Preview
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtCore import QTimer, QThread
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from support_functions import *

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QGroupBox, QLabel,
    QPushButton, QSizePolicy, QWidget)

from ui_form import Ui_MYAPP


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

class MYAPP(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MYAPP()
        self.ui.setupUi(self)
        self.fullscreen_val = True
        self.sensor_read_val = True
        # for CameraStreaming
        self.picam2 = Picamera2()
        self.picam2.start()
        self.pixmap = QPixmap("img.jpg")
        self.camera_streaming_val = True
        self.server_streaming_val = True
        self.people_detection_val = False
        self.fire_waring_value = False
        self.fire_waring_clicked_count = 0
        self._SensorReading()
        self._CameraStreaming()
        self._ServerStreaming()
        # button connect
        self.ui.FullScreenButton.clicked.connect(self._FullSceenButtonAction)
        self.ui.RebootButton.clicked.connect(self._RebootButtonAction)
        self.ui.RefreshButton.clicked.connect(self._RefreshButtonAction)
        self.ui.Camera_Control.clicked.connect(self._StartStopCameraButtonAction)
        self.ui.People_Detection.clicked.connect(self._StartStopPeopleDetection)
        self.ui.ServerSyncButton.clicked.connect(self._StartStopServerSync)
        self.ui.ClearNotiButton.clicked.connect(self._ClearAllNotification)
        self.ui.SetResetFireAlert_Button.clicked.connect(self._SetResetFireWaring)

    def _FullSceenButtonAction(self):
        FullSceenButtonAction(self)

    def _RebootButtonAction(self):
        RebootButtonAction(self)
    def _ClearAllNotification(self):
        self.ui.Notification1_Value.setText("<Notification 1>")
        self.ui.Notification2_Value.setText("<Notification 2>")
    """
    Code - Choose index 1 or 2 to be cleared:
        + 01B:  Notification 1
        + 10B:  Notification 2
        + 11B:  Notification 1 & 2
    """
    def _ClearNotification(self, code = 3):
        if code & 1 != 0:
            self.ui.Notification1_Value.setText("<Notification 1>")
        if code & 2 != 0:
            self.ui.Notification2_Value.setText("<Notification 2>")

    """
    code - Choose index 1 or 2 to be displayed:
        + 01B:  Notification 1
        + 10B:  Notification 2
        + 11B:  Notification 1 & 2
    msg  - The message:
        + The message must less than 20 characters!
    """
    def _SetNotification(self, code = 1, msg = ""):
        if code & 1 != 0:
            self.ui.Notification1_Value.setText(msg)
        if code & 2 != 0:
            self.ui.Notification2_Value.setText(msg)
    def _StartStopCameraButtonAction(self):
        if self.camera_streaming_val == True:
            self.thread1.exit()
            self.picam2.stop()
            self.ui.Camera_Label.setText("Stopped camera streaming")
        self.camera_streaming_val = ~ self.camera_streaming_val
        if self.camera_streaming_val == True:
            # self.thread1.start()
            self.picam2.start()
            time.sleep(2) # warn-up time
            self._CameraStreaming()
    def _StartStopPeopleDetection(self):
        if self.people_detection_val == True:
            self.people_detection_val= False
        else:
            self.people_detection_val = True

        if self.people_detection_val == True:
            self._PeopleDetection()
    def _PeopleDetection(self):
        PeopleDetection(self)
    def _CameraStreaming(self):
        self.thread1 = QThread()
        self.CameraStreaming = CameraStreaming(self)
        self.CameraStreaming.moveToThread(self.thread1)
        self.thread1.started.connect(self.CameraStreaming.UpdateData)
        self.CameraStreaming.finished.connect(self.thread1.quit)
        self.CameraStreaming.finished.connect(self.CameraStreaming.deleteLater)
        self.thread1.finished.connect(self.thread1.deleteLater)
        self.thread1.start()
    def _StartStopServerSync(self):
        if self.server_streaming_val == True:
            self.thread2.exit()
        self.server_streaming_val = ~ self.server_streaming_val
        if self.server_streaming_val == True:
            # self.thread2.start()
            self._ServerStreaming()
            self.ui.ServerConnection_Value.setText("Connected")
        else:
            self.ui.ServerConnection_Value.setText("Disconnected")
    def _ServerStreaming(self):
        self.ui.ServerConnection_Value.setText("Connected")
        self.thread2 = QThread()
        self.ServerStreaming = ServerStreaming(self)
        self.ServerStreaming.moveToThread(self.thread2)
        self.thread2.started.connect(self.ServerStreaming.UpdateData)
        self.ServerStreaming.finished.connect(self.thread2.quit)
        self.ServerStreaming.finished.connect(self.ServerStreaming.deleteLater)
        self.thread2.finished.connect(self.thread2.deleteLater)
        self.thread2.start()
    def _SetResetFireWaring(self):
        self.fire_waring_clicked_count = self.fire_waring_clicked_count + 1
        if self.fire_waring_clicked_count < 10:
            self.ui.SetResetFireAlert_Button.setText("Set/Reset FireAlert(" + str(self.fire_waring_clicked_count) + ")")
            return

        self.fire_waring_clicked_count = 0
        self.ui.SetResetFireAlert_Button.setText("Set/Reset FireAlert")

        if self.fire_waring_value == True:
            self.thread3.exit()
            self._ClearNotification(code=1)

        if self.fire_waring_value == True:
            self.fire_waring_value = False
        else:
            self.fire_waring_value = True

        if self.fire_waring_value == True:
            # stopped ML bcz resource of the host
            # if self.people_detection_val == True:
            #     self._StartStopPeopleDetection()
            # stopped sensor reading bcz resource of the host
            # if self.sensor_read_val == True:
            #     self._RefreshButtonAction()
            # set color background
            #self.setStyleSheet('background-color: red;')
            # fire warning
            self._FireWaring()
    def _FireWaring(self):
        self.thread3 = QThread()
        self.FireWarning = FireWarning(self)
        self.FireWarning.moveToThread(self.thread3)
        self.thread3.started.connect(self.FireWarning.FireWarningAction)
        self.FireWarning.finished.connect(self.thread3.quit)
        self.FireWarning.finished.connect(self.FireWarning.deleteLater)
        self.thread3.finished.connect(self.thread3.deleteLater)
        self.thread3.start()
    def _RefreshButtonAction(self):
        self.ui.temp_value.setText(str(GetTemperature()) + " oC")
        self.sensor_read_val = ~ self.sensor_read_val
        if self.sensor_read_val == True:
            self._SensorReading()
        else:
            self.thread0.exit()
    def _SensorReading(self):
        self.thread0 = QThread()
        self.SensorReading = SensorReading(self)
        self.SensorReading.moveToThread(self.thread0)
        self.thread0.started.connect(self.SensorReading.UpdateData)
        self.SensorReading.finished.connect(self.thread0.quit)
        self.SensorReading.finished.connect(self.SensorReading.deleteLater)
        self.thread0.finished.connect(self.thread0.deleteLater)
        self.thread0.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MYAPP()
    #widget.showFullScreen()
    widget.showNormal()
    sys.exit(app.exec())
