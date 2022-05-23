import os
import eeprom
from sensor import sensors
import time
from xbee import uxbee
from electromechanical import em
import ubinascii

# Init
xbee = uxbee.Uxbee(tx = 16, rx = 17, timeout = 250)
electro = em.EM()

# Defines
TEAM_ID = 1082
ALTITUDES_LIST_SIZE = 10


CONTAINER_MAC = ubinascii.unhexlify("0013A20041BA3838")
CONTAINER_IP = ubinascii.unhexlify("0000")

## Startup State - Retrieve all data from EEPROM
eeprom_variables = eeprom.get_all()
package_count = eeprom_variables["package_count"] 

# Useful variables
entry = True
prev_time = time.ticks_ms()
altitude_list = []

def set_payload_package():
    separator = ','
    package = []
    package.append(str(TEAM_ID))
    package.append("HH:MM:SS")
    package.append(package_count)
    package.append('P')
    package.append(str(sensors.get_altitude()))
    package.append(sensors.get_temperature())
        # package.append(VOLTAJE) ???
    mpu_data = sensors.get_gyro_data
    # Mpu gyro
    package.append(mpu_data[0])
    # Mpu acceleration
    package.append(mpu_data[1])
    # Mpu magn
    package.append(mpu_data[2])
    package.append("0 SOUTH")
    # TODO: ADD STATE IN CONTAINER
    
    return separator.join(package)

while True:
    if xbee.read_command() != 0:
        print("Sending packet to container")
        package = set_payload_package()
        eeprom.store_journal(package)
        eeprom.update_pc()
        xbee.send_packet(0, CONTAINER_MAC, CONTAINER_IP, package)
    # stabilize
