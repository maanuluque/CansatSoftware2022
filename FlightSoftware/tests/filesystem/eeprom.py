import os
import json
import time 

# Packages storage
def store_journal_data(team_id, mission_time, packet_type, mode, altitude, temp, first):
    # remove should be erased
    if "journal.txt" in os.listdir() and first:
        os.remove("journal.txt")
    journal = open("journal.txt" ,"a")
    journal.write(str(team_id) + ','  + str(mission_time) + ','  + str(packet_type) + ','  + str(mode) + ','  + str(altitude) + ','  + str(temp) + '\n')
    journal.close()
    
    
# EEPROM methods
def create():
    control_variables = {
        "current_state": "PRE-DEPLOY",
        "send_telemetry": "True",
        "send_payload_telemetry": "False",
        "package_count": "0",
        "simulation_mode": "False",
        "descend_payload": "null",
        "tp_deploy_time": "null",
        "hasReachApogee": "False"
    }
    with open("eeprom.json", "a") as eeprom:
        eeprom.store(control_variables)
        
def store(variables):
    if "eeprom.json" not in os.listdir():
        # Throw error
    eeprom = open("eeprom.json", "a")
    json_variables = json.dumps(variables)
    json.dump(json_variables, eeprom)
    eeprom.close()
    
def modify(field, value):
    with open("eeprom.json", "r") as eeprom:
        json_variables = json.load(eeprom)
    print("Before changing: " + json_variables)
    variables = json.loads(json_variables)
    variables[field] = value
    json_variables = json.dumps(variables)
    print("After changing: " + json_variables)
    os.remove("eeprom.json")
    with open("eeprom.json", "w") as eeprom:
        json.dump(json_variables, eeprom)

def get_control_variables():
    with open("eeprom.json", "r") as eeprom:
        json_variables = json.load(eeprom)
    control_variables = json.loads(json_variables)
    return control_variables

# Journal data
team_id = 1082
mission_time = "00:00:12"
packet_type = "C"
mode = "F"
altitude = 500
temp = 26.6
store_journal_data(team_id, mission_time, packet_type, mode, altitude, temp, True)

print("Raspberry flash memory test starting...")
print()
start_time = time.ticks_ms()
store_journal_data(team_id, mission_time, packet_type, mode, altitude, temp, False)
print("Telemetry store time: " + str(time.ticks_ms() - start_time) + " miliseconds")
start_time = time.ticks_ms()
eeprom_store(variables, True)
print("EEPROM store time: " + str(time.ticks_ms() - start_time) + " miliseconds")
start_time = time.ticks_ms() 
eeprom_modify("current_state", "DEPLOY")
print("EEPROM modifying time: " + str(time.ticks_ms() - start_time) + " miliseconds")

