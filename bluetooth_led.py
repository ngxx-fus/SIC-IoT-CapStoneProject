import RPi.GPIO as gpio
import serial
led = 21
gpio.setmode(gpio.BCM)
gpio.setup(led, gpio.OUT)
gpio.setwarnings(False)

ser = serial.Serial('/dev/rfcomm0', 115200)
ser.close()
ser.open()
text = b'Bluetooth LED Control\r\n'
n = ser.write(text)
try:
	while True:
		print("Waiting for sender...")
		print("Readable is ", ser.readable())
		if ser.readable():
			resp = ser.readline()
			print("Readline successful!")
			print("Received text: ", resp)
			if resp.find(b'ON') != -1:
				gpio.output(led, True)
			elif resp.find(b'OFF') != -1:
				gpio.output(led, False)
except KeyboardInterrupt:
	pass
finally:
	ser.close()
