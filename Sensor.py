import sys
import time
import time
import board
import logging
import numpy
import subprocess
import adafruit_dht
import RPi.GPIO as IO
from random import randint
from datetime import datetime

DHT11 = adafruit_dht.DHT11(board.D3)
time.sleep(1)
print(adafruit_dht.__file__)

class Sensor:
    def __init__(self):
        ###### set up RPi.GPIO ######
        #IO.setwarnings(False)
        IO.setmode(IO.BCM)


        ###### setup pins ######
        self.DHT11_OutPin = 26
        self.GAS_OutPin = 16
        # IO.setup(self.DHT11_OutPin, IO.IN, pull_up_down=IO.PUD_DOWN)
        # IO.setup(self.GAS_OutPin, IO.IN, pull_up_down=IO.PUD_DOWN)

        ###### set up vars ######
        self.Temp = 0.0
        self.Humid = 0.0
        self.GAS = False
        self.Flame = False

        ###### lambda functions ######
        self.GetTemperature = lambda: self.Temp
        self.GetHumidity    = lambda: self.Humid
        self.GetGAS         = lambda: self.GAS
        self.GetFlame       = lambda: self.Flame

    def Read(self):
        time.sleep(1)
        self.Temp, self.Humid = (randint(24, 33), randint(60,70))
        # self.Temp, self.Humid = (DHT11.temperature, DHT11.humidity)
        self.Flame = bool(randint(0,100) < 50)
        self.GAS   = bool(randint(0,100) < 50)


if __name__ == '__main__':
    try:
        while True:
            DHT11.measure()
            print(DHT11.temperature, DHT11.humidity)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped!")
