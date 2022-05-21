##########################
#     Container FSW      #
##########################

import eeprom
import xbee
import bme280_float as bme280
from mpu9250 import MPU9250

## STARTUP STAGE

# Initialize DEFINES
FIRST_PARACHUTE_ALTITUDE = 670
SECOND_PARACHUTE_ALTITUDE = 400
PAYLOAD_DEPLOY_ALTITUDE = 300
DELTA_ALT_ERROR = 0.8

# Initialize sensors
i2c_mpu = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
mpu = MPU9250(i2c_mpu)
i2c_bme = machine.I2C(1, scl=machine.Pin(11), sda=machine.Pin(10))
bme = bme280.BME280(i2c=i2c_bme)

# Recover data from eeprom
if "eeprom.json" not in os.listdir():
    eeprom.create()
eeprom_variables = eeprom.get_control_variables()

current_state = eeprom_variables["current_state"]
send_telemetry = eeprom_variables["send_telemetry"]
send_payload_telemetry = eeprom_variables["send_payload_telemetry"]
simulation_mode = eeprom_variables["simulation_mode"]
package_count = int(eeprom_variables["package_count"])
has_reach_apogee = eeprom_variables["hasReachApogee"]

# Initialize useful variables
last_altitude = None
first_altitude_measure = True

while(True):
    switch(current_state):
        case "PRE-DEPLOY":
            if simulation_mode == "False":
                altitude = bme.altitude
            else:
                # altitude = get_altitude_from_pressure() --> calculate altitude from sim barometric values
            if last_altitude is None:
                last_altitude = altitude
                sleep_ms(500)
                if simulation_mode == "False":
                    altitude = bme.altitude
                else:
                    # altitude = get_altitude_from_pressure() --> calculate altitude from sim barometric values
            if altitude < PAYLOAD_DEPLOY_ALTITUDE and has_reach_apogee == 'True':
                # Initiate payload's descend
                current_state = DEPLOY
                eeprom.modify("current_state", "PAYLOAD_DEPLOY")
                #   if descend_payload == 'null':
                #     activate_payload_descend()
                #     eeprom.modify("tp_deploy_time", RTC.current_time())
                #     eeprom.modify("descend_payload", "True")
                #   else:
                #     tp_deploy_time = eeprom.get("tp_deploy_time")
                # if delta_time > 1 and send_telemetry == 'True' and simulation_mode == 'False':
                #    package = takeMeasurementsAndStoreInEEPROM()
                #    xbee.sendTelemetryToGround(package)
                #    eeprom.modify("package_count", 1)
            #if delta_time > 1 and send_telemetry == 'True':
            #    package = takeMeasurementsAndStoreInEEPROM()
            #    xbee.sendTelemetryToGround(package)
            #    eeprom.modify("package_count", 1)
        case "PAYLOAD_DEPLOY":
            # if RTC.current_time() - tp_deploy_time < 20seg and descend_payload == 'True':
            #    eeprom.modify("descend_payload", "False")
            # if delta_time_tp > 0.25 seg:
            #    package = xbee.retrieve_payload_data()
            #    xbee.send_telemetry_to_ground(package)
            #    eeprom.modify("package_count", 1)
            # if altitude is constant:
            #    current_state = "LANDED"
            #    send_telemetry = 'False'
            #    eeprom.modify("send_telemetry", send_telemetry)
            #    audio.on
            #    package = xbee.retrieve_payload_data()
            #    xbee.send_telemetry_to_ground(package)
            #    eeprom.modify("package_count", 1)
            #    send_payload_telemetry = "False"
            #    xbee.send_telemetry_to_payload("TPX", send_payload_telemetry)
            #    eeprom.modify("send_payload_telemetry", send_payload_telemetry)
            # elif delta_time > 1 seg and send_telemetry == 'True' and simulation_mode == 'False':
            #    package = takeMeasurementsAndStoreInEEPROM()
            #    xbee.sendTelemetryToGround(package)
            pass
        # TODO: nunca debiera llegar al default --> nunca deberia ser null. chequear
        case default:
            current_state = "PRE_DEPLOY"
            pass
    # check for commands
    command = xbee.check_for_commands()
    switch(command):
        case "CX":
            ## todo: check equality
            if send_telemetry == "True":
                send_telemetry = "False"
            else:
                send_telemetry = "True"
            eeprom.modify("send_telemetry", send_telemetry)
        case "ST":
            pass
        case "SIM":
            pass
        case "SIMP":
            pass
        case "TPX":
            if send_payload_telemetry == "True":
                send_payload_telemetry = "False"
            else:
                send_payload_telemetry = "True"
            eeprom.modify("send_payload_telemetry", send_payload_telemetry)
