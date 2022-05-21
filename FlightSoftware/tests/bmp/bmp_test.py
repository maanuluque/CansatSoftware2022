import machine
import bme280_float as bme280
from time import sleep_ms

i2c = machine.I2C(1, scl=machine.Pin(11), sda=machine.Pin(10))
bme = bme280.BME280(i2c=i2c)

while(True):
    temp = bme.values[0]
    pres = bme.values[1]
    hum = bme.values[2]
    print(bme.values)
    sleep_ms(1000)