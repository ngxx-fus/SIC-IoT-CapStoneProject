import sys
import time
import board
import logging
import numpy
import subprocess
import adafruit_dht
from External import IO
from External import DHT11
from random import randint
from datetime import datetime

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

    def DHT11Reading(self):
        while True:
            try:
                self.Temp = DHT11.temperature
                self.Humid = DHT11.humidity
                return
            except RuntimeError as error:
                print([ERROR], print(error.args[0]))
                continue
            except Exception as error:
                dhtDevice.exit()
                raise error
        return (-1, -1)

    def Read(self):
        time.sleep(1)
        self.Temp, self.Humid = self.DHT11Reading()
        # self.Temp, self.Humid = (DHT11.temperature, DHT11.humidity)
        self.Flame = bool(randint(0,100) < 50)
        self.GAS   = bool(randint(0,100) < 50)


if __name__ == '__main__':
    Sensor = Sensor()
    try:
        while True:
            DHT11.measure()
            print("Sensor.DHT11Reading: ", Sensor.DHT11Reading())
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped!")
