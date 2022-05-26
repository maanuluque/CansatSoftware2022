import os
import machine
import eeprom
from sensor import sensors
import time
from rtc import RTC_DS3231
from xbee import uxbee
import ubinascii
from electromechanical import em

#os.remove("journal.txt")
#os.remove("eeprom.json")


# Init
rtc = RTC_DS3231.RTC(port=1, sda_pin=14, scl_pin=15)
xbee = uxbee.Uxbee(channel = 1, tx = 8, rx = 9, timeout = 250)
payload_xbee = uxbee.Uxbee(channel = 0, tx = 16, rx = 17, timeout = 250)
adc = machine.ADC(0)
electro = em.EM()

# Defines
PAYLOAD_DEPLOY_ALTITUDE = 300
APOGEE_ALTITUDE = 670
SECOND_PARACHUTE_ALTITUDE = 400
DELTA_TIME = 1000
DELTA_TIME_PAYLOAD = 250
PAYLOAD_DESCEND_TIME = 20000
TEAM_ID = 1082
ALTITUDES_LIST_SIZE = 10
CONVERSION_FACTOR = 3.3 / 65535
NICROM_TIME_ON = 3000


GROUND_MAC = ubinascii.unhexlify("0013A20041BA29C8")
GROUND_IP = ubinascii.unhexlify("9802")

PAYLOAD_MAC = ubinascii.unhexlify("0013A20041B11802")
PAYLOAD_IP = ubinascii.unhexlify("CC30")

## Startup State - Retrieve all data from EEPROM
eeprom_variables = eeprom.get_all()
send_telemetry = eeprom_variables["send_telemetry"]
package_count = eeprom_variables["package_count"] 
simulation_mode = eeprom_variables["simulation_mode"]
sim_activated = eeprom_variables["sim_activated"]
current_state = eeprom_variables["current_state"]
hasReachApogee = eeprom_variables["hasReachApogee"]
tp_released = eeprom_variables["tp_released"]
send_payload_telemetry = eeprom_variables["send_payload_telemetry"]
tp_is_descending = eeprom_variables["tp_is_descending"]
parachute_deployed = eeprom_variables["parachute_deployed"]

# Useful variables
entry = True
prev_time = time.ticks_ms()
payload_prev_time = time.ticks_ms()
last_command = "None"
last_altitude = None
sim_pressure = None
altitude_list = []
altitude = 0
nicrom_parachute = False
nicrom_payload = False
nicrom_time = 0

pin_led = machine.Pin(25, machine.Pin.OUT)
bool_led = False

def setup():
    sensors.artificial_sea_level()
    if simulation_mode == 'True' and sim_activated == 'True':
        sim_pressure = uxbee.wait_for_simp()
        altitude = sensors.get_sim_altitude(sim_pressure)
    else:
        altitude = sensors.get_altitude()
        time.sleep_ms(1500)
    altitude_list.append(altitude)
        
def get_voltage():
    raw = adc.read_u16()
    volts = raw * CONVERSION_FACTOR
    return volts
        
def set_container_package(altitude):
    separator = ','
    package = []
    package.append(str(TEAM_ID))
    package.append(rtc.DS3231_ReadTime(3))
    package.append(package_count)
    package.append('C')
    if simulation_mode == 'True':
        package.append('S')
    else:
        package.append('F')
    if tp_released == "True":
        package.append('R')
    else:
        package.append('N')
    package.append(str(altitude))
    package.append(str(sensors.get_temperature()))
    package.append(str(get_voltage()))
    #gps_values = gps.get_values()
    # TODO: Sacar valores hardcodeados
    package.append("15:48:02")
    package.append("36.3501")
    package.append("-3.3501")
    package.append("50.3")
    package.append("16")
    # package.append(gps_values[0])
    # package.append(gps_values[1])
    # package.append(gps_values[2])
    # package.append(gps_values[3])
    # package.append(gps_values[4])
    package.append(current_state)
    package.append(last_command)
    
    return separator.join(package)

def set_payload_package(tp_released, tp_is_descending):
    package = []
    package.append(tp_released)
    package.append(tp_is_descending)
    payload_state = ",".join(package)
    package = []
    package.append(rtc.DS3231_ReadTime(3))
    package.append(payload_state)
    return "-".join(package)

def receive_payload_package():
    command = payload_xbee.read_command()
    if command != 0:
        #print('Received from Payload!')
        packet = payload_xbee.wait_for_frame()
        if packet != None:
            frame_type = packet.get_frame_type()
            if (frame_type == 0x90 or frame_type == 0x91):
                #print("Received from Payload: {}".format(packet.output()))
                # Get/Parse something?
                data = packet.get_frame_data()
                # print("Data: {}".format(data))
                # Eeprom modify?
                xbee.send_packet(0, GROUND_MAC, GROUND_IP, data)
                #print("Retransmited PAYLOAD to GROUND")
            

def recieve_command():
    global send_telemetry
    global simulation_mode
    global sim_pressure
    global send_payload_telemetry
    command = xbee.read_command()
    if command != 0:
        packet = xbee.wait_for_frame()
        if packet != None:
            #print("PACKET --> {}".format(packet.get_frame_data()))
            frame_type = packet.get_frame_type()
            if (frame_type == 0x90 or frame_type == 0x91):
                data = packet.get_frame_data().split(',')
                # Check if command / simp
                packet_type = data[0]
                if packet_type == 'CMD':
                    last_command = data[2]
                    #print("RECIEVED " + str(last_command) + " from GROUND")

                    if last_command == 'CX':
                        if send_telemetry == 'False':
                            send_telemetry = 'True'
                        elif send_telemetry == 'True':
                            send_telemetry = 'False'
                        eeprom.modify('send_telemetry', send_telemetry)
                    
                    elif last_command == 'ST':
                        time = data[3]
                        rtc.DS3231_SetTime(NowTime = time)
                
                    elif last_command == 'SIM':
                        sim_command = data[3]
                        if sim_command == "ENABLE":
                            simulation_mode = 'True'
                        elif sim_command == 'ACTIVATE':
                            sim_activated = 'True'
                        elif sim_command == 'DISABLE':
                            simulation_mode = 'False'
                            sim_activated = 'False'
                        eeprom.modify('simulation_mode', simulation_mode)
                        eeprom.modify('sim_activated', sim_activated)

                    elif last_command == 'SIMP':
                        #print("READING FROM SIMP")
                        sim_pressure = data[3]
                
                    elif last_command == 'TPX':
                        if send_payload_telemetry == 'False':
                            send_payload_telemetry = 'True'
                        elif send_payload_telemetry == 'True':
                            send_payload_telemetry = 'False'
                        eeprom.modify('send_payload_telemetry', send_payload_telemetry)
    
setup()
while(True):
    if (bool_led == True):
        pin_led.high()
        bool_led = False
    else:
        pin_led.low()
        bool_led = True
    recieve_command()
    
    if send_payload_telemetry == "True":
        receive_payload_package()
        
    last_altitude = altitude
    
    if simulation_mode == 'True' and sim_activated == 'True':
        altitude = sensors.get_sim_altitude(sim_pressure)
    else:
        altitude = sensors.get_altitude()
    altitude_list.append(altitude)
    if len(altitude_list) > ALTITUDES_LIST_SIZE:
        altitude_list.pop(0)
    
    if altitude > APOGEE_ALTITUDE and hasReachApogee == "False":
        hasReachApogee = True
        eeprom.modify("hasReachApogee", "True")
        
    #print(sensors.flight_state(altitude_list))
    
    if current_state == "PRE-DEPLOY":
        #print("PRE-DEPLOY state")        
        if parachute_deployed == "False" and altitude < SECOND_PARACHUTE_ALTITUDE and sensors.flight_state(altitude_list) == "descending" and hasReachApogee == "True":
            parachute_deployed = "True"
            eeprom.modify("parachute_deployed", "True")
            electro.parachute_nicrom_on()
            nicrom_parachute = True
            nicrom_time = time.ticks_ms()
        
        if nicrom_parachute == True:
            current_time = time.ticks_ms()
            if ((current_time - nicrom_time) > NICROM_TIME_ON):
                electro.parachute_nicrom_off()
                nicrom_parachute = False

        if altitude < PAYLOAD_DEPLOY_ALTITUDE and sensors.flight_state(altitude_list) == "descending" and hasReachApogee == "True" and nicrom_payload == False:
            electro.payload_nicrom_on()
            nicrom_payload = True
            nicrom_time = time.ticks_ms()
         
        if nicrom_payload == True:
            current_time = time.ticks_ms()
            if ((current_time - nicrom_time) > NICROM_TIME_ON):
                electro.payload_nicrom_off()
                nicrom_payload = False 
                entry = True
                current_state = "DEPLOY"
                eeprom.modify("current_state", "DEPLOY")

    elif current_state == "DEPLOY":
        #print("DEPLOY state")
        if entry and eeprom.get("tp_is_descending") == "False":
            # activar servo para desenrollar payload
            electro.start_motor()
            entry = False
            tp_deploy_time = time.ticks_ms()
            tp_released = "True"
            tp_is_descending = "True"
            eeprom.modify("tp_released", "True")
            eeprom.modify("tp_deploy_time", str(tp_deploy_time))
            eeprom.modify("tp_is_descending", "True")
        
        if (tp_is_descending == "True" and ((time.ticks_ms() - tp_deploy_time) > PAYLOAD_DESCEND_TIME)):
            # stop servo
            electro.stop_motor()
            tp_is_descending = "False"
            eeprom.modify("tp_is_descending", "False")
            
        # Check for LANDED state
        landed = sensors.check_for_landed(altitude_list)
        if landed:
            current_state = "LANDED"
            eeprom.modify("current_state", "LANDED")
        
    elif current_state == "LANDED":
        #print("LANDED state")
        send_telemetry = "False"
        send_payload_telemetry = "False"
        eeprom.modify("send_telemetry", "False")
        eeprom.modify("send_payload_telemetry", "False")
        # power on audio beacon
        exit()

    current_time = time.ticks_ms()
    
    if (send_payload_telemetry == "True" and (current_time - payload_prev_time > DELTA_TIME_PAYLOAD)):
        # Poll and relay payload telemetry
        payload_prev_time = current_time
        package = set_payload_package(tp_released, tp_is_descending)
        #print("Polling to PAYLOAD... {}".format(package))
        # Store in eeprom?
        payload_xbee.send_packet(0, PAYLOAD_MAC, PAYLOAD_IP, package)
            
            
    #print("Time passed: " + str(current_time - prev_time))
    # print(current_time - prev_time > DELTA_TIME)
    if (send_telemetry == "True" and (current_time - prev_time > DELTA_TIME)):
        prev_time = current_time
        package = set_container_package(altitude)
        #print("SENDING TO GROUND... {}".format(package))
        #print("Altitude is: " + str(altitude))
        eeprom.store_journal(package)
        eeprom.update_pc()
        xbee.send_packet(0, GROUND_MAC, GROUND_IP, package)
        #print("Transmited from CONTAINER to GROUND")
