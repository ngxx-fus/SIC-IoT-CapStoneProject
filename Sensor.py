import sys
import time
import logging
import numpy
import time
import subprocess
import RPi.GPIO as IO
from random import randint
from datetime import datetime

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(20, IO.IN, pull_up_down=IO.PUD_DOWN)

def GetTemperature():
    msg = """
        This function is gonna to be dev soon
        Try latter!
    """
    print("Called: Sensor.GetTemperature")
    # print(msg)
    if IO.input == IO.HIGH:
        randint(17, 30)
    return randint(17, 50)

def GetHumidity():
    msg = """
        This function is gonna to be dev soon.
        Plase try again latter!
    """
    print("Called: Sensor.GetHumidity")
    # print(msg)
    return randint(30, 70)

def GetCO2():
    msg = """
        This function is gonna to be dev soon.
        Plase try again latter!
    """
    print("Called: Sensor.GetCO2")
    # print(msg)
    return randint(10, 30)

def GetFlame():
    msg = """
        This function is gonna to be dev soon.
        Plase try again latter!
    """
    print("Called: Sensor.GetFlame")
    # print(msg)
    return randint(0, 1)