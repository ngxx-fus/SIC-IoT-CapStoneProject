import numpy
import time
import requests
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
HĂ m tráº£ vá» dáº¡ng chuá»—i cá»§a val náº¿u khĂ´ng Ă¢m,ngÆ°á»£c láº¡i tráº£ vá» "--".
Cho phĂ©p chĂ¨n thĂªm tiá»n tá»‘ (prefix) vĂ  háº­u tá»‘ (suffix)
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

"""
This function to check the Internet connection.
Parameters:
    NONE
Return value:
    True  : if device have connection to Internet
    False : otherwise
"""
def InternetConnectionCheck():
    try:
        requests.head("http://www.google.com/", timeout=1)
        # Do something
        return True
    except requests.ConnectionError:
        # Do something
        return False
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
        self.Smoke = 0.0

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
    The conclusion of whether there is a fire or not is based on the values â€‹â€‹obtained from the sensors and predictions from machine learning.
    TODO: rewrite condition
    """
    def isFlaming(self):
        if self.Flame == 0:
            if self.Temp < 45.0:
                if self.CO2 == 0:
                    return True
        return False

    """
    Update data onto UI.
    """
    def UpdateUI(self):
        self.myapp.ui.temp_value.setText(ValueFormat(self.Temp, suffix=" oC"))
        self.myapp.ui.humid_value.setText(ValueFormat(self.Humid, suffix=" %"))
        self.myapp.ui.CO2_value.setText(ValueFormat(self.CO2, suffix=""))

    """
    Server sync.
    """
    def ServerSYNC(self):
        self.myapp.ui.ServerConnection_Value.setText("Updating data...")
        Sending_Smoke = 'OFF'
        if self.CO2 > 0.0:
            Sending_Smoke = 'ON'
        FireSwtich, LightSet = ServerSYNC(Temp=self.Temp, Humid=self.Humid, Smoke=Sending_Smoke, MYAPP=self.myapp)
        print(FireSwtich, " - ", self.myapp.fire_waring_value)
        if (FireSwtich == 'ON') and (self.myapp.fire_waring_value == False):
            self.myapp._SetResetFireWaring(priority_flag=True, priority_setter=True)
        elif ((FireSwtich == 'OFF')) and (self.myapp.fire_waring_value == True):
            self.myapp._SetResetFireWaring(priority_flag=True, priority_setter=False)
        self.myapp.ui.ServerConnection_Value.setText("Done!")

    """
    Auto set FireAlert based on isFlaming()
    """
    def AutoSetFireAlert(self):
        if self.isFlaming() == True:
            if self.myapp.fire_waring_value == False and self.myapp.auto_start_fire_alert == True:
                self.myapp._SetResetFireWaring(priority_flag=True, priority_setter=True)
                if self.myapp.server_streaming_val == True:
                    ServerSYNC(Fire='ON', MYAPP=self.myapp)
        elif self.myapp.fire_waring_value == True and self.myapp.auto_stop_fire_alert == True:
            self.myapp._SetResetFireWaring(priority_flag=True, priority_setter=False)
            if self.myapp.server_streaming_val == True:
                ServerSYNC(Fire='OFF', MYAPP=self.myapp)

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
            self.AutoSetFireAlert()

            if self.myapp.sensor_read_val == True:
                self.UpdateUI()

            if self.myapp.server_streaming_val == True:
                if InternetConnectionCheck() == False:
                    self.myapp._SetNotification(2, "Internet lost!")
                    self.myapp._StartStopServerSync()
                else:
                    self.ServerSYNC()
            else:
                self.myapp.ui.ServerConnection_Value.setText("Disconnected!")

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
        # if self.myapp.server_streaming_val == False:
            # self.myapp._StartStopServerSync()
            # self.myapp._SetNotification(code=2, msg="Auto turn-on server SYNC!")
        self.myapp.ui.RebootButton.setEnabled(False)
        self.myapp.ui.Camera_Control.setEnabled(False)
        self.myapp.ui.ServerSyncButton.setEnabled(False)
        self.myapp.ui.FireWarningBar.setVisible(True)
        msg = "FireWarning"
        dots = "!"
        if self.myapp.server_streaming_val == True:
            FireSwtich, LightSet = ServerSYNC(Fire='ON') #'Fire' meaning FireState (Detected or Not)
            if FireSwtich == 'OFF':
                ServerSYNC(Fan='ON')
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
        if self.myapp.server_streaming_val == True:
            FireSwtich, LightSet = ServerSYNC(Fire='OFF', MYAPP=self.myapp) #'Fire' meaning FireState (Detected or Not)
            if FireSwtich == 'ON':
                ServerSYNC(Fan='OFF', MYAPP=self.myapp)
        self.myapp.ui.FireWarningBar.setVisible(False)
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
            self.myapp.picam2.capture_file("./Imgs/img.jpg")
            self.myapp.pixmap.load("./Imgs/img.jpg")
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
