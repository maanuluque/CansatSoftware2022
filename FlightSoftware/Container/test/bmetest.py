import machine
from sensor import bme280_float as bme280
from time import sleep_ms
import os 

i2c1 = machine.I2C(0, scl=machine.Pin(21), sda=machine.Pin(20))
bme = bme280.BME280(i2c=i2c1)

while(True):
    print("Temperature: " + str(bme.values))
    print("Altitude: "  + str(bme.altitude))
    sleep_ms(1000)