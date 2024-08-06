import RPi.GPIO as GPIO
import time
import board
import busio
import digitalio
import adafruit_dht
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate('/home/pi/project.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://nhan-3660d-default-rtdb.firebaseio.com/'
})


dht_device = adafruit_dht.DHT11(board.D16)


FLAME_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_PIN, GPIO.IN)


MQ2_PIN = 12
GPIO.setup(MQ2_PIN, GPIO.IN)

def GetTemperature():
    print("Called: Sensor.GetTemperature")
    try:
        temperature = dht_device.temperature
        if temperature is not None:
            return round(temperature, 2)
        else:
            print("Failed to retrieve data from temperature sensor")
            return None
    except RuntimeError as error:
        print(error.args[0])
        return None

def GetHumidity():
    print("Called: Sensor.GetHumidity")
    try:
        humidity = dht_device.humidity
        if humidity is not None:
            return round(humidity, 2)
        else:
            print("Failed to retrieve data from humidity sensor")
            return None
    except RuntimeError as error:
        print(error.args[0])
        return None

def GetCO2():
    print("Called: Sensor.GetCO2")

    if GPIO.input(MQ2_PIN) == GPIO.HIGH:
        return "Gas Detected"
    else:
        return "No Gas"

def GetFlame():
    print("Called: Sensor.GetFlame")

    return GPIO.input(FLAME_PIN)

def upload_data():
    temperature = GetTemperature()
    humidity = GetHumidity()
    co2_status = GetCO2()
    flame_status = GetFlame()

    try:
        if temperature is not None and humidity is not None:
          
            temp_ref = db.reference('LivingRoom/nhietdo')
            temp_ref.set(temperature)
            print(f"Uploaded temperature: {temperature} oC")

            
            humidity_ref = db.reference('LivingRoom/doamkk')
            humidity_ref.set(humidity)
            print(f"Uploaded humidity: {humidity} %")

        
        co2_ref = db.reference('LivingRoom/co2')
        co2_ref.set(co2_status)
        print(f"Uploaded CO2 status: {co2_status}")

        
        flame_ref = db.reference('LivingRoom/flame')
        flame_ref.set(flame_status)
        print(f"Uploaded flame sensor status: {flame_status}")

    except Exception as e:
        print(f"Failed to upload data to Firebase: {e}")

def main():
    try:
        while True:
            upload_data()
            time.sleep(5)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
