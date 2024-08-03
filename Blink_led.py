from gpiozero import LED # type: ignore
from signal import pause

red = LED(16)

red.blink()
pause()