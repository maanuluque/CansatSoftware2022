##########################
#     Container FSW      #
##########################

import eeprom
import xbee
import bme280
from mpu9250 import MPU9250

## STARTUP

# Initialize sensors

# Recover data from eeprom
if "eeprom.json" not in os.listdir():
    eeprom.create()
eeprom_variables = eeprom.get_variables()

current_state = eeprom_variables["current_state"]
send_telemetry = eeprom_variables["send_telemetry"]
send_payload_telemetry = eeprom_variables["send_payload_telemetry"]
simulation_mode = eeprom_variables["sim_mode"]
package_count = int(eeprom_variables["package_count"])

while(True):
    switch(current_state):
        case "PRE-DEPLOY":
            if simulation_mode == "False":
                # Measure altitude
                # if altitude < 300:
                #   current_state = DEPLOY
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
            ## todo: check equality
            if send_payload_telemetry == "True":
                send_payload_telemetry = "False"
            else:
                send_payload_telemetry = "True"
            eeprom.modify("send_payload_telemetry", send_payload_telemetry)
