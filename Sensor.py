import sys
import time
import logging
import numpy
import time
import subprocess
import RPi.GPIO as IO
from random import randint
from datetime import datetime

class Sensor:
    def __init__(self):
        ###### set up RPi.GPIO ######
        #IO.setwarnings(False)
        IO.setmode(IO.BCM)
        
        ###### set up vars ######
        self.Temp = 0.0
        self.Humid = 0.0
        self.GAS = False
        self.Flame = False
        
        ###### setup pins ######
        IO.DTH11_OutPin = 26
        IO.GAS_OutPin = 16
        IO.setup(self.DTH11_OutPin, IO.IN, pull_up_down=IO.PUD_DOWN)
        
        ###### lambda functions ######
        self.GetTemperature = lambda: self.Temp
        self.GetHumidity    = lambda: self.Humid
        self.GetGAS         = lambda: self.GAS
        self.GetFlame       = lambda: self.Flame

    def Read(self):
        self.Temp, self.Humid = (randint(24, 33), randint(60,70))
        self.Flame = bool(randint(0,100) < 50)
        self.GAS   = bool(randint(0,100) < 50)

