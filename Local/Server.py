import sys
import time
import logging
import subprocess
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('./Informations/login.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://nhan-3660d-default-rtdb.firebaseio.com/'
})

"""
This function get/set value on Firebase.
Parameters:
+   Temp            (Type: float)
+   Himid           (Type: float)
+   FireSwitch      (Type: str)     'ON'/'OFF'
+   LightSwitch     (Type: str)     'ON'/'OFF'
+   GAS             (Type: str)     'ON'/'OFF'
+   Fire            (Type: str)     'ON'/'OFF'
Return value:
+   Return list includes two elements, the first is state of FAN, the order is state of LIGHT which is "ON" or "OFF".
NOTE:
    If FAN or LIGHT is not None, they will update ON/OFF state same on web.
"""

def _ONOFF(val):
    if val > 0.0:
        return 'ON'
    return 'OFF'

def ServerSYNCStatus(MYAPP = None, msg = "", ConsoleLog = False):
    if MYAPP is not None:
        MYAPP.ui.ServerConnection_Value.setText(msg)
    if ConsoleLog == True:
        print("ServerSNYC: ", msg)

def ServerSYNC( Temp = None, Humid = None, GAS = None, Fire = None, FireSwitch = None,
                LightSwitch = None, GET = False, MYAPP = None, ConsoleLog = False):
    if Temp is not None:
        ServerSYNCStatus(MYAPP, "Updating Temp...", ConsoleLog)
        db.reference('LivingRoom/nhietdo').set(Temp)
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    if Humid is not None:
        ServerSYNCStatus(MYAPP, "Updating Himid...", ConsoleLog)
        db.reference('LivingRoom/doamkk').set(Humid)
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    if GAS is not None:
        ServerSYNCStatus(MYAPP, "Updating GAS...", ConsoleLog)
        db.reference('LivingRoom/smoke').set(_ONOFF(GAS))
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    if Fire is not None:
        ServerSYNCStatus(MYAPP, "Updating Fire St...", ConsoleLog)
        db.reference('LivingRoom/fire').set(Fire)
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    if FireSwitch is not None:
        ServerSYNCStatus(MYAPP, "Updating Fire Sw...", ConsoleLog)
        db.reference('LivingRoom/fan').set(_ONOFF(FireSwitch))
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    if LightSwitch is not None:
        ServerSYNCStatus(MYAPP, "Updating LightSwitch St...", ConsoleLog)
        db.reference('LivingRoom/light').set(_ONOFF(LightSwitch))
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    if GET == True:
        ServerSYNCStatus(MYAPP, "Getting Fire Sw...", ConsoleLog)
        FireSwitch = db.reference('LivingRoom/fireAlarm').get(False)
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
        ServerSYNCStatus(MYAPP, "Getting LightSwitch Sw...", ConsoleLog)
        LightSwitch = db.reference('LivingRoom/light').get(False)
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
        return [ FireSwitch, LightSwitch ]
    return [None, None]

if __name__ == "__main__":
    print(ServerSYNC(Fire=0, GAS=1, GET=True, ConsoleLog=True))
