import machine
#from sensor import bme280_float as bme280
from sensor import sensors
from time import sleep_ms
import os 

#i2c1 = machine.I2C(0, scl=machine.Pin(21), sda=machine.Pin(20))
#bme = bme280.BME280(i2c=i2c1)

sensors.artificial_sea_level()

while(True):
    print("Altitude: "  + str(sensors.get_altitude()))
    sleep_ms(1000)