import numpy
import time
import subprocess
from PySide6 import QtGui
from  PySide6.QtCore import QSize
from random import randint
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from picamera2 import Picamera2, Preview


class FireWarning(QObject):
    finished = pyqtSignal()
    def __init__(self, myapp):
        super().__init__(parent=None)
        self.myapp = myapp

    def FireWarningAction(self):
        msg = "FireWarning"
        dots = "!"
        while self.myapp.fire_waring_value == True:
            self.myapp.ui.Notification1_Value.setText(msg + dots)
            dots = dots + "!"
            if len(dots) > 3:
                dots = "!"
            time.sleep(1)
        self.finished.emit()

"""
    TODO: After edit and re-translation f*.ui file, You need add this property again into ui_form.py.
    $ self.pixmap = QPixmap()
    Because QPixmap cannot initialize here!
"""
class CameraStreaming(QObject):
    finished = pyqtSignal()
    def __init__(self, myapp):
        super().__init__()
        self.myapp = myapp

    def UpdateData(self):
        msg = "Running demo mode"
        dots = "."
        while self.myapp.camera_streaming_val == True:
            # self.myapp.ui.Camera_Label.setText(msg + dots)
            # dots = dots + "."
            # if len(dots) > 10:
            #     dots = "."

            self.myapp.picam2.capture_file("img.jpg")
            self.myapp.pixmap.load("img.jpg")
            self.myapp.ui.Camera_Label.setPixmap(self.myapp.pixmap.scaled(QSize(301, 201)))

            time.sleep(0.05)
        self.finished.emit()

class ServerStreaming(QObject):
    finished = pyqtSignal()
    def __init__(self, myapp):
        super().__init__(parent=None)
        self.myapp = myapp

    def UpdateData(self):
        msg = "Running demo mode"
        dots = "."
        while self.myapp.server_streaming_val == True:
            self.myapp.ui.ServerConnection_Value.setText( msg + dots)
            dots = dots + "."
            if len(dots) > 3:
                dots = "."
            time.sleep(1)
        self.finished.emit()

class SensorReading(QObject):
    finished = pyqtSignal()
    def __init__(self, myapp):
        super().__init__(parent=None)
        self.myapp = myapp

    def UpdateData(self):
        while self.myapp.sensor_read_val == True:
            self.myapp.ui.temp_value.setText(str(GetTemperature()) + " oC")
            self.myapp.ui.humid_value.setText(str(GetHumidity()) + " %")
            self.myapp.ui.CO2_value.setText(str(GetCO2()) + " %")
            time.sleep(1)
        self.finished.emit()


def FullSceenButtonAction(MYAPP):
    MYAPP.fullscreen_val = ~ MYAPP.fullscreen_val
    if MYAPP.fullscreen_val == True:
        MYAPP.showFullScreen()
    else:
        MYAPP.showNormal()

def RebootButtonAction(myapp):
    msg = "Reboot after "
    sec = 10
    while sec > 0:
        myapp._SetNotification(code=2,msg=msg + str(sec) + "s")
        sec = sec - 1
        time.sleep(1)
    subprocess.Popen("sh reboot.sh", shell=True)

def GetTemperature():
    return randint(17, 50)

def GetHumidity():
    return randint(30, 70)

def GetCO2():
    return randint(10, 30)

def PeopleDetection(myapp):
    if myapp.camera_streaming_val == False:
        return
    myapp._SetNotification(code=2,msg="PeopleDetection: No longer service!")
    return
