import machine
import bme280_float as bme280
from time import sleep_ms

i2c = machine.I2C(1, scl=machine.Pin(11), sda=machine.Pin(10))
bme = bme280.BME280(i2c=i2c)

total_altitude = bme.altitude
counter = 1
while(True):
    counter = counter + 1
    total_altitude = total_altitude + bme.altitude
    avg = total_altitude / counter
    sleep_ms(1000)
    #print(bme.values)
    #print("Altitude: " + str(bme.altitude))
    #sleep_ms(1000)