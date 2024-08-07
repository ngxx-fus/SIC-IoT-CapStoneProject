import RPi.GPIO as GPIO
from time import sleep

class Exec:
    def __init__(self):
        self.IO = GPIO
        self.IO.setmode(IO.BCM)
        #self.IO.setwarnings(False)
        self.BuzzerPin = 21
        self.LightPin  = 20
        self.IO.setup(self.BuzzerPin, IO.OUT)
        self.IO.setup(self.LightPin, IO.OUT)

    def _HL(self, var):
        if var > 0.0:
            return IO.HIGH
        return IO.LOW

    def BuzzerSet(self, state):
        IO.output(self.BuzzerPin, self._HL(state))

    def BuzzerPulse(self, time=1):
        IO.output(self.BuzzerPin, self._HL(1))
        sleep(time)
        IO.output(self.BuzzerPin, self._HL(0))

    def LightSet(self, state):
        IO.output(self.LightPin, self._HL(state))
    
    def __del__(self):
        IO.cleanup()