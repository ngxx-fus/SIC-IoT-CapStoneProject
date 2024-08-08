import sys
import time
import logging
import numpy
import time
import board
import busio
import digitalio
import adafruit_dht
import subprocess
import RPi.GPIO as IO
from random import randint
from datetime import datetime

dht_device = adafruit_dht.DHT11(board.D16)

FLAME_PIN = 26
IO.setmode(IO.BCM)
IO.setup(FLAME_PIN, IO.IN)
MQ2_PIN = 12
IO.setup(MQ2_PIN, IO.IN)

def GetTemperature():
    try:
        temperature = dht_device.temperature
        if temperature is not None:
            return round(temperature, 2)
        else:
            print("Failed to retrieve data from temperature sensor")
            return None
    except RuntimeError as error:
        print(error.args[0])
        return -1

def GetHumidity():
    try:
        humidity = dht_device.humidity
        if humidity is not None:
            return round(humidity, 2)
        else:
            print("Failed to retrieve data from humidity sensor")
            return None
    except RuntimeError as error:
        print(error.args[0])
        return -1

def GetGAS():
    return int(IO.input(MQ2_PIN) == IO.HIGH)

def GetFlame():
    return int(IO.input(FLAME_PIN) == IO.HIGH)

class Sensor:
    def __init__(self):
        ###### set up RPi.IO ######
        #IO.setwarnings(False)
        IO.setmode(IO.BCM)
        
        ###### set up vars ######
        self.Temp = 0.0
        self.Humid = 0.0
        self.GAS = False
        self.Flame = False
        
    def Read(self):
        self.Temp  = GetTemperature()
        self.Humid = GetHumidity()
        self.Flame = GetFlame()
        self.GAS   = GetGAS()
