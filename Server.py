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
def ServerSYNC(Temp = None, Humid = None, Smoke = None, Fire = None, Fan = None, Light = None):
    if Temp is not None:
        db.reference('LivingRoom/nhietdo').set(Temp)
    if Humid is not None:
        db.reference('LivingRoom/doamkk').set(Humid)
    if Smoke is not None:
        db.reference('LivingRoom/smoke').set(Smoke)
    if Fire is not None:
        db.reference('LivingRoom/fire').set(Fire)
    if Fan is not None:
        db.reference('LivingRoom/fan').set(Fan)
    if Light is not None:
        db.reference('LivingRoom/light').set(Light)
    return [db.reference('LivingRoom/light').get(False),
            db.reference('LivingRoom/fan').get(False)]

if __name__ == "__main__":
    print(ServerSYNC(1, 1, 'OFF', 'OFF', 'OFF', 'OFF'))