from External import IO
from time import sleep

class Exec:
    """
    + Set/Reset GPIO
    + Control GPIO
    """
    def __init__(self):
        self.BuzzerPin = 21
        self.LightPin  = 20
        IO.setup(self.BuzzerPin, IO.OUT)
        IO.setup(self.LightPin, IO.OUT)

    def _HL(self, var):
        """
        Return GPIO.HIGH/GPIO.LOW based on logic value of var.
        """
        if var > 0.0:
            return IO.HIGH
        return IO.LOW

    def BuzzerSet(self, state):
        """
        Set GPIO connected to Buzzer HIGH/LOW based on logic value of state.
        """
        IO.output(self.BuzzerPin, self._HL(state))

    def BuzzerSquaredPulse(self, time=1):
        """
        Make a spared pulse off Buzzer with timeon = timeoff = time/2 (second).
        """
        IO.output(self.BuzzerPin, self._HL(1))
        sleep(time/2)
        IO.output(self.BuzzerPin, self._HL(0))
        sleep(time/2)

    def LightSet(self, state):
        """
        Set GPIO connected to Light HIGH/LOW based on logic value of state.
        """
        IO.output(self.LightPin, self._HL(state))
