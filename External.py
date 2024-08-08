import time
import board
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
IO = GPIO

DHT11 = adafruit_dht.DHT11(board.D3)
time.sleep(3)