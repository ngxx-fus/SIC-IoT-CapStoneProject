import RPi.GPIO as GPIO
from time import sleep

class Exec:
    def __init__(self):
        self.self.IO = GPIO
        self.self.IO.setmode(self.IO.BCM)
        #self.self.IO.setwarnings(False)
        self.BuzzerPin = 21
        self.LightPin  = 20
        self.self.IO.setup(self.BuzzerPin, self.IO.OUT)
        self.self.IO.setup(self.LightPin, self.IO.OUT)

    def _HL(self, var):
        if var > 0.0:
            return self.IO.HIGH
        return self.IO.LOW

    def BuzzerSet(self, state):
        self.IO.output(self.BuzzerPin, self._HL(state))

    def BuzzerSquaredPulse(self, time=1):
        self.IO.output(self.BuzzerPin, self._HL(1))
        sleep(time/2)
        self.IO.output(self.BuzzerPin, self._HL(0))
        sleep(time/2)

    def LightSet(self, state):
        self.IO.output(self.LightPin, self._HL(state))
    
    def __del__(self):
        self.IO.cleanup()