import os
import eeprom
from sensor import sensors
import time
from xbee import uxbee
from electromechanical import em
import ubinascii

# Init
xbee = uxbee.Uxbee(channel = 0, tx = 0, rx = 1, timeout = 250)
electro = em.EM()

# Defines
TEAM_ID = 1082
ALTITUDES_LIST_SIZE = 10


CONTAINER_MAC = ubinascii.unhexlify("0013A2004191C55C")
CONTAINER_IP = ubinascii.unhexlify("FB11")

## Startup State - Retrieve all data from EEPROM
eeprom_variables = eeprom.get_all()
package_count = eeprom_variables["package_count"] 

# Useful variables
entry = True
prev_time = time.ticks_ms()
altitude_list = []
bool_led = True

def set_payload_package(time, payload_state):
    separator = ','
    package = []
    package.append(str(TEAM_ID))
    package.append(time)
    package.append(package_count)
    package.append('P')
    package.append(str(sensors.get_altitude()))
    package.append(str(sensors.get_temperature()))
        # package.append(VOLTAJE) ???
    mpu_data = sensors.get_gyro_data()
    # Mpu gyro
    package.append(str(mpu_data[0][0]))
    package.append(str(mpu_data[0][1]))
    package.append(str(mpu_data[0][2]))
    # Mpu acceleration
    package.append(str(mpu_data[1][0]))
    package.append(str(mpu_data[1][1]))
    package.append(str(mpu_data[1][2]))
    # Mpu magn
    package.append(str(mpu_data[2][0]))
    package.append(str(mpu_data[2][1]))
    package.append(str(mpu_data[2][2]))
    package.append("0 SOUTH")
    
    payload_state_split = payload_state.split(',')
    if (payload_state_split[0] == 'False'):
        package.append('STANDBY')
    else:
        if (payload_state_split[1] == 'False'):
            package.append('RELEASED')
        else:
            package.append('DESCENDING')
    
    return separator.join(package)

while True:
    time.sleep(1)
    if (bool_led == True):
        pin_led.high()
        bool_led = False
    else:
        pin_led.low()
        bool_led = True
    if xbee.read_command() != 0:
        packet = xbee.wait_for_frame()
        frame_type = packet.get_frame_type()
        if (frame_type == 0x90 or frame_type == 0x91):
            data = packet.get_frame_data()
            data_split = data.split('-')
            package = set_payload_package(data_split[0], data_split[1])
            eeprom.store_journal(package)
            eeprom.update_pc()
            xbee.send_packet(0, CONTAINER_MAC, CONTAINER_IP, package)
    # stabilize


