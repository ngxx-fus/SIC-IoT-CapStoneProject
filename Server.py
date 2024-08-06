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
+   Temp    (Type: float)
+   Himid   (Type: float)
+   Fan     (Type: str)     'ON'/'OFF'
+   Light   (Type: str)     'ON'/'OFF'
+   Smoke   (Type: str)     'ON'/'OFF'
+   Fire    (Type: str)     'ON'/'OFF'
Return value:
+   Return list includes two elements, the first is state of FAN, the order is state of LIGHT which is "ON" or "OFF".
NOTE:
    If FAN or LIGHT is not None, they will update ON/OFF state same on web.
"""

def ServerSYNCStatus(MYAPP = None, msg = "", ConsoleLog = False):
    if MYAPP is not None:
        MYAPP.ui.ServerConnection_Value.setText(msg)
    if ConsoleLog == True:
        print("ServerSNYC: ", msg)

def ServerSYNC(Temp = None, Humid = None, Smoke = None, Fire = None, Fan = None, Light = None, MYAPP = None, ConsoleLog = False):
    if Temp is not None:
        ServerSYNCStatus(MYAPP, "Updating Temp...", ConsoleLog)
        db.reference('LivingRoom/nhietdo').set(Temp)
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    if Humid is not None:
        ServerSYNCStatus(MYAPP, "Updating Himid...", ConsoleLog)
        db.reference('LivingRoom/doamkk').set(Humid)
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    if Smoke is not None:
        ServerSYNCStatus(MYAPP, "Updating Smoke...", ConsoleLog)
        db.reference('LivingRoom/smoke').set(Smoke)
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    if Fire is not None:
        ServerSYNCStatus(MYAPP, "Updating Fire St...", ConsoleLog)
        db.reference('LivingRoom/fire').set(Fire)
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    if Fan is not None:
        ServerSYNCStatus(MYAPP, "Updating Fire Sw...", ConsoleLog)
        db.reference('LivingRoom/fan').set(Fan)
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    if Light is not None:
        ServerSYNCStatus(MYAPP, "Updating Light St...", ConsoleLog)
        db.reference('LivingRoom/light').set(Light)
        ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    ServerSYNCStatus(MYAPP, "Getting Fire Sw...", ConsoleLog)
    FireSwitch = db.reference('LivingRoom/light').get(False)
    ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    ServerSYNCStatus(MYAPP, "Getting Light Sw...", ConsoleLog)
    LightSwitch = db.reference('LivingRoom/fan').get(False)
    ServerSYNCStatus(MYAPP, "Done!", ConsoleLog)
    return [ FireSwitch, LightSwitch ]

if __name__ == "__main__":
    print(ServerSYNC(Fire='ON'))
