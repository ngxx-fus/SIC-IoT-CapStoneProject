import numpy
import time
import subprocess
import RPi.GPIO as IO
from random import randint
from datetime import datetime
from PySide6 import QtGui
from PySide6.QtCore import QSize
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from picamera2 import Picamera2, Preview

from Sensor import GetTemperature, GetHumidity, GetCO2, GetFlame
from Server import ServerSYNC
from Predict import PredictFlaming

############################# FUNCTIONS #################################
"""
Hàm trả về dạng chuỗi của val nếu không âm,ngược lại trả về "--".
Cho phép chèn thêm tiền tố (prefix) và hậu tố (suffix)
"""
def ValueFormat(val, prefix = '', suffix = ''):
    if val >= 0:
        return prefix + str(val) + suffix
    return prefix + '--' + suffix


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

def PeopleDetection(myapp):
    if myapp.camera_streaming_val == False:
        return
    myapp._SetNotification(code=2,msg="PeopleDetection: No longer service!")
    return

############################# CLASSES #################################

"""
Worker class: SensorReadingAndServerStreaming
To read sensor data, update value onto UI, SYNC to server.
"""
class SensorReadingAndServerStreaming(QObject):
    finished = pyqtSignal()
    def __init__(self, myapp):
        super().__init__(parent=None)
        self.myapp = myapp
        self.Temp = 0.0
        self.Humid = 0.0
        self.CO2 = 0.0
        self.Flame = 0.0

    """
    Update self.Temp, self.Humid, self.CO2, self.Flame.
    Return Tuple includes sensor data
    """
    def GetDataSensor(self):
        self.Temp = GetTemperature()
        self.Humid = GetHumidity()
        self.CO2 = GetCO2()
        self.Flame = GetFlame()
        return (self.Temp, self.Humid, self.CO2, self.Flame)

    """
    Update data onto UI.
    """
    def UpdateUI(self):
        self.myapp.ui.temp_value.setText(ValueFormat(self.Temp, suffix=" oC"))
        self.myapp.ui.humid_value.setText(ValueFormat(self.Humid, suffix=" %"))
        self.myapp.ui.CO2_value.setText(ValueFormat(self.CO2, suffix=" %"))

    """
    Server sync.
    """
    def ServerSYNC(self):
        msg = "OK! Sent:"
        msg1 = ValueFormat(self.Temp, "T", "oC, ")
        msg2 = ValueFormat(self.Humid, "H", "%, ")
        msg3 = ValueFormat(self.CO2, "C", "%, ")
        msg4 = ValueFormat(self.Flame, "F")
        self.myapp.ui.ServerConnection_Value.setText(msg+msg1+msg2+msg3+msg4)
        ServerSYNC()

    """
    The conclusion of whether there is a fire or not is based on the values ​​obtained from the sensors and predictions from machine learning.
    """
    def isFlaming(self):
        if self.Flame > 0:
            if self.Temp > 40.0:
                if self.CO2 > 50:
                    return True
                    if self.Humid < 30:
                        if PredictFlaming() > 80:
                            return True
        return False

    """
    Auto set FireAlert based on isFlaming()
    """
    def AutoSetFireAlert(self):
        if self.isFlaming() == True:
            if self.myapp.fire_waring_value == False and self.myapp.auto_start_fire_alert == True:
                self.myapp._SetResetFireWaring(priority_flag=True, priority_setter=True)
        elif self.myapp.fire_waring_value == True and self.myapp.auto_stop_fire_alert == True:
            self.myapp._SetResetFireWaring(priority_flag=True, priority_setter=False)

    """
    Work based on data from sensor.
    """
    def Working(self):
        # Doing and doing
        while True:
            # reading sensor
            self.GetDataSensor()
            time.sleep(1)
            # processing
            if self.myapp.sensor_read_val == True:
                self.UpdateUI()

            if self.myapp.server_streaming_val == True:
                self.ServerSYNC()
            else:
                self.myapp.ui.ServerConnection_Value.setText("Stopped by USER")

            self.AutoSetFireAlert()
        # Send back finished signal !
        self.finished.emit()

"""
Worker class: FireWarning
Running Warning actions.
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
        self.myapp.ui.RebootButton.setEnabled(False)
        self.myapp.ui.Camera_Control.setEnabled(False)
        self.myapp.ui.ServerSyncButton.setEnabled(False)
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
        #IO.cleanup()
        self.myapp.ui.RebootButton.setEnabled(True)
        self.myapp.ui.Camera_Control.setEnabled(True)
        self.myapp.ui.ServerSyncButton.setEnabled(True)
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
Worker class: ServerStreaming
NOTE:
    This class has been deleted after merged two classes
    SensorReading and ServerStreaming into class SensorReadingAndServerStreaming 
    to prevent 'CRASHED' from simultaneously using GPIO BUS.
"""
# class ServerStreaming(QObject):
#     finished = pyqtSignal()
#     def __init__(self, myapp):
#         super().__init__(parent=None)
#         self.myapp = myapp

#     def UpdateData(self):
#         msg = "Sent "
#         while self.myapp.server_streaming_val == True:
#             msg1 = str(GetTemperature()) + " oC "
#             msg2 = str(GetHumidity()) + " % "
#             msg3 = "--"
#             self.myapp.ui.ServerConnection_Value.setText( msg + msg1 + msg2 + msg3)
#             time.sleep(1)
#         self.finished.emit()

"""
Worker class: SensorReading
NOTE:
    This class has been deleted after merged two classes
    SensorReading and ServerStreaming into class SensorReadingAndServerStreaming 
    to prevent 'CRASHED' from simultaneously using GPIO BUS.
"""
# class SensorReading(QObject):
#     finished = pyqtSignal()
#     def __init__(self, myapp):
#         super().__init__(parent=None)
#         self.myapp = myapp

#     def UpdateData(self):
#         while self.myapp.sensor_read_val == True:
#             self.myapp.ui.temp_value.setText(str(GetTemperature()) + " oC")
#             self.myapp.ui.humid_value.setText(str(GetHumidity()) + " %")
#             self.myapp.ui.CO2_value.setText("--")
#             time.sleep(1)
#         self.finished.emit()

