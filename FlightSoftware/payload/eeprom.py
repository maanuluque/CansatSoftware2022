##################################
# Module to interact with EEPROM #
##################################
import os
import json
import time 

def store_journal(package):
    journal = open("journal.txt" ,"a")
    journal.write(package)
    journal.write('\n')
    journal.close()

    
## EEPROM methods    
def create():
    variables = {
        "package_count": "0",
    }
    store(variables)

def store(variables):
    if "eeprom.json" in os.listdir():
        os.remove("eeprom.json")
    eeprom = open("eeprom.json", "w")
    json_variables = json.dumps(variables)
    json.dump(json_variables, eeprom)
    eeprom.close()
    
def modify(field, value):
    with open("eeprom.json", "r") as eeprom:
        json_variables = json.load(eeprom)
    variables = json.loads(json_variables)
    variables[field] = value
    json_variables = json.dumps(variables)
    os.remove("eeprom.json")
    with open("eeprom.json", "w") as eeprom:
        json.dump(json_variables, eeprom)
        
def get(field):
    with open("eeprom.json", "r") as eeprom:
        json_variables = json.load(eeprom)
    variables = json.loads(json_variables)
    return variables[field]

def get_all():
    if "eeprom.json" not in os.listdir():
        create()
    with open("eeprom.json", "r") as eeprom:
        json_variables = json.load(eeprom)
    variables = json.loads(json_variables)
    return variables

def update_pc():
    pc = int(get("package_count"))
    modify("package_count", str(pc+1))

