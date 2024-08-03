from gpiozero import LED # type: ignore
from gpiozero import DistanceSensor # type: ignore

import time

sensor = DistanceSensor(echo = 14, trigger = 15)
led = LED(18)

while True:
    distance = sensor.distance * 100
    print("distance : ", distance)
    if distance < 10:
        led.on()
    else:
        led.off()
    time.sleep(0.5)
        
    