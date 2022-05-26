# Main Sensor Module - Contains all methods for sensors usage

import machine
from sensor import bme280_float as bme280
from sensor import mpu9250
from time import sleep_ms

## Initialization
DELTA_ALT = 0.5
MAX_PRESSURE_VALUES = 20

# BME
i2c = machine.I2C(0, scl=machine.Pin(21), sda=machine.Pin(20))
bme = bme280.BME280(i2c=i2c)

def altitude_is_equal(alt1, alt2):
    diff = alt1 - alt2
    if abs(diff) < DELTA_ALT:
        return True
    return False

def flight_state(altitude_list):
    diff = altitude_list[-1] - altitude_list[0]
    if abs(diff) > DELTA_ALT:
        # Rocket altitude changed
        if diff > 0:
            return "ascending"
        else:
            return "descending"
    return "launch"

def is_ascending(altitude_list):
    diff = altitude_list[-1] - altitude_list[0]
    if abs(diff) > DELTA_ALT:
        # Rocket altitude changed
        if diff > 0:
            return True
    return False

def check_for_landed(altitude_list):
    return altitude_is_equal(altitude_list[-1], altitude_list[0])

def get_altitude():
    return bme.altitude

def get_sim_altitude(pressure):
    return bme.sim_altitude(pressure)

def get_temperature():
    return bme.values[0]

def artificial_sea_level():
    added = 0
    for _ in range(MAX_PRESSURE_VALUES):
        added += bme.read_compensated_data()[1]
    ans = added / MAX_PRESSURE_VALUES
    print("NEW SEA LEVEL {}".format(ans))
    bme.sealevel = ans