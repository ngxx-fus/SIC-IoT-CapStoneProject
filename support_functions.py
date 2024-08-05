import numpy
import time
import subprocess
import RPi.GPIO as IO
from datetime import datetime
from PySide6 import QtGui
from  PySide6.QtCore import QSize
from random import randint
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from picamera2 import Picamera2, Preview

"""
Worker class
"""
class FireWarning(QObject):
    finished = pyqtSignal()
    def __init__(self, myapp, BuzzerPin = 21):
        super().__init__(parent=None)
        self.myapp = myapp
        self.BuzzerPin = BuzzerPin
        IO.setmode(IO.BCM)
        IO.setwarnings(False)
        IO.setup(self.BuzzerPin, IO.OUT)

    def FireWarningAction(self):
        msg = "FireWarning"
        dots = "!"
        while self.myapp.fire_waring_value == True:
            self.myapp.ui.FireWarningBar.setVisible(True)
            self.myapp.ui.Notification1_Value.setText(msg + dots)
            dots = dots + "!"
            if len(dots) > 3:
                dots = "!"
            IO.output(self.BuzzerPin, IO.HIGH)
            time.sleep(0.5)
            IO.output(self.BuzzerPin, IO.LOW)
            self.myapp.ui.FireWarningBar.setVisible(False)
            time.sleep(0.5)
        self.myapp.ui.FireWarningBar.setVisible(False)
        IO.cleanup()
        self.finished.emit()
"""
Worker class
"""
class CameraStreaming(QObject):
    finished = pyqtSignal()
    def __init__(self, myapp):
        super().__init__()
        self.myapp = myapp

    def UpdateData(self):
        while self.myapp.camera_streaming_val == True:
            self.myapp.picam2.capture_file("img.jpg")
            self.myapp.pixmap.load("img.jpg")
            self.myapp.ui.Camera_Label.setPixmap(self.myapp.pixmap.scaled(QSize(301, 201)))
            time.sleep(0.041666)
        self.myapp.picam2.stop()
        self.finished.emit()

"""
Worker class
"""
class ServerStreaming(QObject):
    finished = pyqtSignal()
    def __init__(self, myapp):
        super().__init__(parent=None)
        self.myapp = myapp

    def UpdateData(self):
        msg = "Sent "
        while self.myapp.server_streaming_val == True:
            msg1 = str(GetTemperature()) + " oC "
            msg2 = str(GetHumidity()) + " % "
            msg3 = "--"
            self.myapp.ui.ServerConnection_Value.setText( msg + msg1 + msg2 + msg3)
            time.sleep(1)
        self.finished.emit()

"""
Worker class
"""
class SensorReading(QObject):
    finished = pyqtSignal()
    def __init__(self, myapp):
        super().__init__(parent=None)
        self.myapp = myapp

    def UpdateData(self):
        while self.myapp.sensor_read_val == True:
            self.myapp.ui.temp_value.setText(str(GetTemperature()) + " oC")
            self.myapp.ui.humid_value.setText(str(GetHumidity()) + " %")
            self.myapp.ui.CO2_value.setText("--")
            time.sleep(1)
        self.finished.emit()


def FullSceenButtonAction(MYAPP):
    MYAPP.fullscreen_val = ~ MYAPP.fullscreen_val
    if MYAPP.fullscreen_val == True:
        MYAPP.showFullScreen()
    else:
        MYAPP.showNormal()

def RebootButtonAction(myapp):
    sec = 10
    while sec > 0:
        sec = sec - 1
        time.sleep(1)
    subprocess.Popen("sh reboot.sh", shell=True)

def GetTemperature():
    time.sleep(1)
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
