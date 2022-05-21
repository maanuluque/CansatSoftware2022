## Payload state entry - Retrieve all data from EEPROM

# TODO: Crear un archivo para almacenar estas variables
#package_count = eeprom_variables["tp_package_count"]
#send_payload_telemetry = eeprom_variables["tp_send_payload_telemetry"]
#package_count = eeprom_variables["package_count"]

## Defines
TEAM_ID = 1082

# Loading Modules
tpSensorModule = TpSensorModule()

while True:
    # command = xbee.tp_read_command() - check for commands
    # if command is not None:
        # last_command = command
        # do something
    #if send_telemetry == 'True':
    #print(tpSensorModule.get_altitude())