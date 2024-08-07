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

from Sensor import GetTemperature, GetHumidity, GetGAS, GetFlame
from Server import ServerSYNC
from Predict import PredictFlaming
from Exec   import Exec
from Sensor import Sensor

############################# GLOBAL VARS #################################



############################# GLOBAL FUNCTIONS #################################
"""
"""
def ValueFormat(val, prefix = '', suffix = ''):
    if val >= 0:
        return prefix + str(val) + suffix
    return prefix + '--' + suffix

"""
"""
def FullSceenButtonAction(MYAPP):
    MYAPP.fullscreen_val = ~ MYAPP.fullscreen_val
    if MYAPP.fullscreen_val == True:
        MYAPP.showFullScreen()
    else:
        MYAPP.showNormal()

"""
"""
def RebootButtonAction(myapp):
    sec = 10
    while sec > 0:
        sec = sec - 1
        time.sleep(1)
    subprocess.Popen("sh reboot.sh", shell=True)

"""
"""
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
        requests.head("https://trankhanhnhan.github.io/sic-iot/Home.html", timeout=1)
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
        self.Sensor = Sensor()
        self.LightSwitch = False
        self.FireSwitch  = False

    # 'ON' / 'OFF'
    def _ONOFF(self, var):
        if vaf > 0.0:
            return 'ON'
        return 'OFF'

    # XNOR
    def _xnor(self, A, B):
        if A == B:
            return True
        return False

    """
    The conclusion of whether there is a fire or not is based on the values obtained from the sensors and predictions from machine learning.
    TODO: rewrite condition
    """
    def isFlaming(self):
        if self.Sensor.Flame == 0:
            if self.Sensor.Temp < 45.0:
                if self.Sensor.GAS == 0:
                    return True
        return False

    """
    Update data onto UI.
    """
    def UpdateUI(self):
        self.myapp.ui.temp_value.setText(ValueFormat(self.Sensor.Temp, suffix=" oC"))
        self.myapp.ui.humid_value.setText(ValueFormat(self.Sensor.Humid, suffix=" %"))
        self.myapp.ui.GAS_value.setText(ValueFormat(self.Sensor.GAS, suffix=""))

    """
    Server sync.
    """
    def ServerSYNC(self):
        self.LightSwitch, self.FireSwitch = ServerSYNC( 
            Temp=self.Sensor.Temp, 
            Humid=self.Sensor.Humid,
            GAS=self.Sensor.GAS,
            Fire=self._ONOFF(self.myapp.fire_waring_value),
            MYAPP=self.myapp, 
            GET=True
        )

    def SetResetLightState(self):
        FinalLightState = self._xnor(
            self.myapp.light_switch_value,
            self.LightSwitch
        )
        Exec.LightSet(_xnor(FinalLightState))

    """
    Auto set FireAlert based on isFlaming()
    """
    def AutoSetFireAlert(self):
        FireState_Auto = False
        FireState_Switch_Web = False
        FireState_Switch_Local = self.myapp.fire_switch_value
        # Check SYNCSERVER is enble
        if self.myapp.server_streaming_val == True:
            FireState_Switch_Web = bool(self.FireSwitch == 'ON')
        # Detected flaming
        if self.isFlaming() == True and self.myapp.auto_start_fire_alert == True:
            FireState_Auto = True
        # Combination
        FinalFireState =  FireState_Auto or FireState_Switch_Web or FireState_Switch_Local
        print(FinalFireState,   FireState_Auto, FireState_Switch_Web, FireState_Switch_Local)
        if FinalFireState != self.myapp.fire_waring_value:
            self.myapp._SetResetFireWaring(priority_flag=True, priority_setter=FinalFireState)
        # time.sleep(1)

    """
    Work based on data from sensor.
    """
    def Working(self):
        # Doing and doing
        while True:
            # reading sensor
            self.Sensor.Read()
            # processing based on SensorData
            self.AutoSetFireAlert()
            # Start/Stop update Temp/Humid/CO2 on UI
            if self.myapp.sensor_read_val == True:
                self.UpdateUI()
            # SYNC to server
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

########################################################################
"""
Worker class: FireWarning
Running Warning actions.
"""
class FireWarning(QObject):
    finished = pyqtSignal()
    def __init__(self, myapp):
        super().__init__(parent=None)
        self.myapp = myapp
        self.Exec = Exec()


    def FireWarningAction(self):
        print("[INFO] FireWarning.FireWarningAction: ", self.myapp.fire_waring_value)
        # if self.myapp.fire_waring_value:
        #     return
        self.myapp.ui.RebootButton.setEnabled(False)
        self.myapp.ui.Camera_Control.setEnabled(False)
        self.myapp.ui.ServerSyncButton.setEnabled(False)
        self.myapp.ui.FireWarningBar.setVisible(True)
        msg = "FireWarning"
        dots = "!"
        while self.myapp.fire_waring_value == True:
            print("[[INFO] FireWarning.FireWarningAction.Loop: ", self.myapp.fire_waring_value)
            self.myapp.ui.FireWarningBar.setVisible(True)
            self.myapp.ui.Notification1_Value.setText(msg + dots)
            dots = dots + "!"
            if len(dots) > 3:
                dots = ""
            self.Exec.BuzzerSquaredPulse(0.25)
            self.myapp.ui.FireWarningBar.setVisible(False)
            self.Exec.BuzzerSquaredPulse(0.25)

        self.myapp.fire_waring_value = False
        self.myapp.ui.FireWarningBar.setVisible(False)
        self.myapp.ui.RebootButton.setEnabled(True)
        self.myapp.ui.Camera_Control.setEnabled(True)
        self.myapp.ui.ServerSyncButton.setEnabled(True)
        
        self.finished.emit()

########################################################################
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
