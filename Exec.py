import RPi.GPIO as IO
from time import sleep

class Exec:
    def __init__(self):
        IO.setmode(IO.BCM)
        #IO.setwarnings(False)
        self.BuzzerPin = 21
        self.LightPin  = 20
        IO.setup(self.BuzzerPin, IO.OUT)
        IO.setup(self.LightPin, IO.OUT)

    def _HL(self, var):
        if var > 0.0:
            return IO.HIGH
        return IO.LOW

    def BuzzerSet(self, state):
        IO.output(self.BuzzerPin, self._HL(state))

    def BuzzerSquaredPulse(self, time=1):
        IO.output(self.BuzzerPin, self._HL(1))
        sleep(time/2)
        IO.output(self.BuzzerPin, self._HL(0))
        sleep(time/2)

    def LightSet(self, state):
        IO.output(self.LightPin, self._HL(state))
