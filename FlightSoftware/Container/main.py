import os
from machine import Timer, Pin, ADC
import eeprom
from sensor import sensors
import time
from rtc import RTC_DS3231
from xbee import uxbee
import ubinascii
from electromechanical import em
import _thread
from PID import PID
from gps import gps_spio

#os.-+remove("journal.txt")
#os.remove("eeprom.json")

## SIM VALUES
plist = [101000,101000,101000,100936,100872,100808,100744,100680,100616,100552,100488,100424,100360,100296,100232,100168,100104,100040,99976,99912,99848,99784,99720,99656,99592,99528,99464,99400,99336,99272,99208,99144,99080,99016,98952,98888,98824,98760,98696,98632,98568,98504,98440,98376,98312,98248,98184,98120,98056,97992,97928,97864,97800,97736,97672,97608,97544,97480,97416,97352,97288,97224,97160,97096,97032,96968,96904,96840,96776,96712,96648,96584,96520,96456,96392,96328,96264,96200,96136,96072,96008,95944,95880,95816,95752,95688,95624,95560,95496,95432,95368,95304,95240,95176,95112,95048,94984,94920,94856,94792,94728,94664,94600,94536,94472,94408,94344,94280,94216,94152,94088,94024,93960,93896,93832,93768,93704,93640,93576,93512,93448,93384,93320,93256,93192,93128,93064,93000,92936,92872,92808,92744,92760,92776,92792,92808,92824,92840,92856,92872,92888,92904,92920,92936,92952,92968,92984,93000,93016,93032,93048,93064,93080,93096,93112,93128,93144,93160,93176,93192,93208,93224,93240,93256,93272,93288,93304,93320,93336,93352,93368,93384,93400,93416,93432,93448,93464,93480,93496,93512,93528,93544,93560,93576,93592,93608,93624,93640,93656,93672,93688,93704,93720,93736,93752,93768,93784,93800,93816,93832,93848,93864,93880,93896,93912,93928,93944,93960,93976,93992,94008,94024,94040,94056,94072,94088,94104,94120,94136,94152,94168,94184,94200,94216,94232,94248,94264,94280,94296,94312,94328,94344,94360,94376,94392,94408,94424,94440,94456,94472,94488,94504,94520,94536,94552,94568,94584,94600,94616,94632,94648,94664,94680,94696,94712,94728,94744,94760,94776,94792,94808,94824,94840,94856,94872,94888,94904,94920,94936,94952,94968,94984,95000,95016,95032,95048,95064,95080,95096,95112,95128,95144,95160,95176,95192,95208,95224,95240,95256,95272,95288,95304,95320,95336,95352,95368,95384,95400,95416,95432,95448,95464,95480,95496,95512,95528,95544,95560,95576,95592,95608,95624,95640,95656,95672,95688,95704,95720,95736,95752,95768,95784,95800,95816,95832,95848,95864,95880,95896,95912,95928,95944,95960,95976,95992,96008,96024,96040,96056,96072,96088,96104,96120,96136,96152,96168,96184,96200,96216,96232,96248,96264,96280,96296,96312,96328,96344,96360,96376,96392,96408,96424,96440,96456,96472,96488,96504,96520,96536,96552,96568,96584,96600,96616,96632,96648,96664,96680,96696,96712,96728,96744,96760,96776,96792,96808,96824,96840,96856,96872,96888,96904,96920,96936,96952,96968,96984,97000,97016,97032,97048,97064,97080,97096,97112,97128,97144,97160,97176,97192,97208,97224,97240,97256,97272,97288,97304,97320,97336,97352,97368,97384,97400,97416,97432,97448,97464,97480,97496,97512,97528,97544,97560,97576,97592,97608,97624,97640,97656,97672,97688,97704,97720,97736,97752,97768,97784,97800,97816,97832,97848,97864,97880,97896,97912,97928,97944,97960,97976,97992,98008,98024,98040,98056,98072,98088,98104,98120,98136,98152,98168,98184,98200,98216,98232,98248,98264,98280,98296,98312,98328,98344,98360,98376,98392,98408,98424,98440,98456,98472,98488,98504,98520,98536,98552,98568,98584,98600,98616,98632,98648,98664,98680,98696,98712,98728,98744,98760,98776,98792,98808,98824,98840,98856,98872,98888,98904,98920,98936,98952,98968,98984,99000,99016,99032,99048,99064,99080,99096,99112,99128,99144,99160,99176,99192,99208,99224,99240,99256,99272,99288,99304,99320,99336,99352,99368,99384,99400,99416,99432,99448,99464,99480,99496,99512,99528,99544,99560,99576,99592,99608,99624,99640,99656,99672,99688,99704,99720,99736,99752,99768,99784,99800,99816,99832,99848,99864,99880,99896,99912,99928,99944,99960,99976,99992,100008,100024,100040,100056,100072,100088,100104,100120,100136,100152,100168,100184,100200,100216,100232,100248,100264,100280,100296,100312,100328,100344,100360,100376,100392,100408,100424,100440,100456,100472,100488,100504,100520,100536,100552,100568,100584,100600,100616,100632,100648,100664,100680,100696,100712,100728,100744,100760,100776,100792,100808,100824,100840,100856,100872,100888,100904,100920,100936,100952,100968,100984,101000,101016]
index = 0
new_sim_time = 0
lenplist = len(plist)

# Init
rtc = RTC_DS3231.RTC(port=1, sda_pin=14, scl_pin=15)
xbee = uxbee.Uxbee(channel = 1, tx = 8, rx = 9, timeout = 250)
payload_xbee = uxbee.Uxbee(channel = 0, tx = 16, rx = 17, timeout = 250)
adc = ADC(0)
electro = em.EM()

## THREAD Stuff

enca = Pin(6, Pin.IN)

MAX_STEPS = 8
MAX_POWER = 2**16 - 2
STOP_STEPS = 55

step = 0
time_steps = 1e6
last_time = 0
last_value = enca.value()

speed_vec = [0]
speed_len = 1

def list_avg():
    return sum(speed_vec) / speed_len

pid = PID(3, 0.05, 0.0025, setpoint=0.5, scale='ms', output_limits=[-30, 30], sample_time=50)

power = 150
speed = 0

def second_thread():
    global tp_is_descending
    
    while step < STOP_STEPS:
    
        new_val = enca.value()
        
        if last_value == 0 and new_val == 1:
            aux_time = time.ticks_us()
            time_steps = aux_time - last_time
            last_time = aux_time
            step += 1

            speed = pi * 0.04 / (MAX_STEPS * time_steps * 1e-6)
            
            speed_vec.append(speed)
        
            if speed_len == 5:
                speed_vec.pop(0)
            else:
                speed_len += 1
                
        last_value = new_val
       
        speed_avg = list_avg()
        output = pid(speed_avg)
        
        power += output
        if power > 255:
            power = 255
        elif power < 0:
            power = 0
            
        total_power = power * MAX_POWER / 255
        
        electro.start_motor(int(total_power))

        time.sleep(0.01)
    electro.stop_motor()
    time.sleep(16)
    while step < STOP_STEPS:
    
        new_val = enca.value()
        
        if last_value == 0 and new_val == 1:
            aux_time = time.ticks_us()
            time_steps = aux_time - last_time
            last_time = aux_time
            step += 1
            
            speed = pi * 0.04 / (MAX_STEPS * time_steps * 1e-6)
            
            speed_vec.append(speed)
        
            if speed_len == 5:
                speed_vec.pop(0)
            else:
                speed_len += 1
                
        last_value = new_val
       
        speed_avg = list_avg()
        output = pid(speed_avg)
        
        power += output
        if power > 255:
            power = 255
        elif power < 0:
            power = 0
            
        total_power = power * MAX_POWER / 255
        
        electro.start_motor(int(total_power))
        
        time.sleep(0.01)
    electro.stop_motor()
    tp_is_descending = "False"
    eeprom.modify("tp_is_descending", "False")
    _thread.exit()

# Defines
PAYLOAD_DEPLOY_ALTITUDE = 300
#300
APOGEE_ALTITUDE = 650
#650
SECOND_PARACHUTE_ALTITUDE = 400
#400
DELTA_TIME_CONTAINER = 1000
DELTA_TIME_PAYLOAD = 250

# Timers for irq to send packets
tim_container = Timer()
tim_payload = Timer()

# Timers for oneshots
tim_parachute_nichrom = Timer()
tim_payload_nichrom = Timer()

# Timer for buzzer
tim_buzzer = Timer()

PAYLOAD_DESCEND_TIME = 5000
TEAM_ID = 1082
ALTITUDES_LIST_SIZE = 5
CONVERSION_FACTOR = 3.3 / 65535
NICROM_TIME_ON = 4000
BUZZER_TIME = 1000
ADD_LIST_TIME = 500

# Network Discovery
TIMEOUT = 250
COMMAND = 'MY'
DEFAULT_IP = ubinascii.unhexlify("FFFE")
actual_time = 0

GROUND_MAC = ubinascii.unhexlify("0013A20041BA29C8")
ground_ip = bytearray()
#ground_ip = 0000

PAYLOAD_MAC = ubinascii.unhexlify("0013A20041B11802")
payload_ip = bytearray()
#payload_ip = 

## Startup State - Retrieve all data from EEPROM
eeprom_variables = eeprom.get_all()
send_telemetry = eeprom_variables["send_telemetry"]
package_count = eeprom_variables["package_count"] 
simulation_mode = eeprom_variables["simulation_mode"]
sim_activated = eeprom_variables["sim_activated"]
current_state = eeprom_variables["current_state"]
hasReachApogee = eeprom_variables["hasReachApogee"]
isDescending = eeprom_variables["isDescending"]
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
add_list_time = 0
altitude = 0
nicrom_parachute = False
nicrom_payload = False
nicrom_time = 0
artificial_sealevel = 0
print_tick = 0
buzzer_time = 0
offset = 0
done = False

pin_led = Pin(25, Pin.OUT)
bool_led = False

## XBEE IP Discovery

def get_device_ip(DEVICE_MAC, device):
    device.send_remote_at_command(1, DEVICE_MAC, DEFAULT_IP, 0x02, COMMAND, '')
    actual_time = time.ticks_ms()
    packet = None
    while True:
        if device.read_command() != 0:
            packet = device.wait_for_frame()
            if packet is not None:
                if packet.get_frame_type() == 0x97:
                    if packet.response is not None:
                        return packet.response
        
        
        if time.ticks_ms() - actual_time > TIMEOUT:
            print("Discovery timeout: Retrying")
            packet = device.send_remote_at_command(1, DEVICE_MAC, DEFAULT_IP, 0x02, COMMAND, '')
            actual_time = time.ticks_ms()

def network_discovery():
    global ground_ip
    global payload_ip
    ground_ip = get_device_ip(GROUND_MAC, xbee)
    #print('GROUND IP: {}'.format(ground_ip))
    #payload_ip = get_device_ip(PAYLOAD_MAC, payload_xbee)
    #print('PAYLOAD IP: {}'.format(payload_ip))


## PACKAGES manager

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

def send_container_package(t):
    global altitude
    package = set_container_package(altitude)
    print("About to send --> {}".format(package))
    try:
        xbee.send_packet(0, GROUND_MAC, ground_ip, package)
    except:
        None

def send_payload_package(t):
    global tp_released
    global tp_is_descending
    global payload_ip
    package = set_payload_package(tp_released, tp_is_descending)
    try:
        payload_xbee.send_packet(0, PAYLOAD_MAC, payload_ip, package)
    except:
        None

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
                xbee.send_packet(0, GROUND_MAC, ground_ip, data)
                #print("Retransmited PAYLOAD to GROUND")

def init_container_timer():
    tim_container.init(period=DELTA_TIME_CONTAINER, callback=send_container_package, mode=Timer.PERIODIC)

def init_payload_timer():
    tim_payload.init(period=DELTA_TIME_PAYLOAD, callback=send_payload_package, mode=Timer.PERIODIC)
    


def setup():
    global sim_pressure
    global offset
    if simulation_mode == 'True' and sim_activated == 'True':
        sim_pressure = xbee.wait_for_simp()
        print("SIM PRESSURE: {}".format(sim_pressure))
        altitude = sensors.get_sim_altitude(sim_pressure)
        print("SIM ALTITUDE: {}".format(altitude))
    else: 
        artificial_sealevel = sensors.artificial_sea_level()
        altitude = sensors.get_altitude()
        if (altitude < 0):
            print("ALTITUDE: {}".format(altitude))
            offset = altitude * -1
            print("OFFSET: {}".format(offset))
            altitude += offset
            print("ALTITUDE + OFFSET: {}".format(altitude))
        time.sleep_ms(1500)
    altitude_list.append(altitude)
    if (send_telemetry == 'True'):
        init_container_timer()


## COMMAND manager

def recieve_command():
    global send_telemetry
    global simulation_mode
    global sim_pressure
    global send_payload_telemetry
    global sim_activated
    command = xbee.read_command()
    if command != 0:
        print("Recieved something!")
        packet = xbee.wait_for_frame()
        if packet != None:
            print("PACKET --> {}".format(packet.get_frame_data()))
            frame_type = packet.get_frame_type()
            if (frame_type == 0x90 or frame_type == 0x91):
                data = packet.get_frame_data().split(',')
                # Check if command / simp
                packet_type = data[0]
                if packet_type == 'CMD':
                    last_command = data[2]
                    print("RECIEVED " + str(last_command) + " from GROUND")

                    if last_command == 'CX':
                        if data[3] == 'OFF':
                            print("OFF command recieved.")
                            if send_telemetry == 'True':
                                print("Turning send telemetry off.")
                                send_telemetry = 'False'
                                tim_container.deinit()
                                eeprom.modify('send_telemetry', send_telemetry)
                        elif data[3] == 'ON':
                            print("ON command recieved.")
                            if send_telemetry == 'False':
                                print("Turning send telemetry off.")
                                send_telemetry = 'True'
                                init_container_timer()
                                eeprom.modify('send_telemetry', send_telemetry)
        # NowTime has to be in format like b'\x00\x23\x12\x28\x14\x07\x21'
        # It is encoded like this           sec min hour week day month year
                    elif last_command == 'ST':
                        time = data[3].split(':')
                        print(time)
                        format_time = "b'\\x" + str(time[2]) + "\\x" + str(time[1]) + "\\x" + str(time[0]) + "\\x23\\x12\\x06\\x22'"
                        print(format_time)
                        rtc.DS3231_SetTime(NowTime = format_time)
                
                    elif last_command == 'SIM':
                        sim_command = data[3]
                        if sim_command == "ENABLE":
                            print("Simulation mode enabled.")
                            simulation_mode = 'True'
                        elif sim_command == 'ACTIVATE':
                            if simulation_mode == 'True':
                                print("Simulation mode activated.")
                                sim_activated = 'True'
                        elif sim_command == 'DISABLE':
                            print("Simulation mode Disabled.")
                            simulation_mode = 'False'
                            sim_activated = 'False'
                        eeprom.modify('simulation_mode', simulation_mode)
                        eeprom.modify('sim_activated', sim_activated)

                    elif last_command == 'SIMP':
                        sim_pressure = data[3]
                        #print(data)
                        #print("Saving SIMP value: " + str(sim_pressure))
                
                    elif last_command == 'TPX':
                        if send_payload_telemetry == 'False':
                            send_payload_telemetry = 'True'
                        elif send_payload_telemetry == 'True':
                            send_payload_telemetry = 'False'
                        eeprom.modify('send_payload_telemetry', send_payload_telemetry)


## ELECTROMECHANICS

def stop_parachute_nichrom(t):
    global altitude
    electro.parachute_nicrom_off()
    print("PARACHUTE NICROM OFF AT: {}".format(altitude))
    
def stop_payload_nichrom(t):
    global entry
    global current_state
    global altitude
    electro.payload_nicrom_off()
    entry = True
    current_state = "DEPLOY"
    eeprom.modify("current_state", "DEPLOY")
    print("PAYLOAD NICROM OFF: {}".format(altitude))

def toggle_buzzer(t):
    electro.toggle_buzzer()

## GETTERS
    
def get_voltage():
    raw = adc.read_u16()
    volts = raw * CONVERSION_FACTOR
    return volts
        
            
network_discovery()
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
        if sim_pressure == None:
            altitude = last_altitude
        else:
            altitude = sensors.get_sim_altitude(sim_pressure)
        #print("Using SIMP altitude: " + str(altitude))
    else:
        altitude = sensors.get_altitude()
        #print("REAL ALTITUDE: {}".format(altitude))
        altitude += offset
        if (altitude < 0):
            altitude = 0
        
    if ((time.ticks_ms() - add_list_time) > ADD_LIST_TIME):
        altitude_list.append(altitude)
        add_list_time = time.ticks_ms()
        #print("Altitude List: {}".format(altitude_list))
        
    if len(altitude_list) > ALTITUDES_LIST_SIZE:
        altitude_list.pop(0)
        
    
    if altitude > APOGEE_ALTITUDE and hasReachApogee == "False":
        hasReachApogee = "True"
        eeprom.modify("hasReachApogee", "True")
        print("REACHED APOGEE AT: {}".format(altitude))

    #print(sensors.flight_state(altitude_list))
    
    if current_state == "PRE-DEPLOY":
        #print("PRE-DEPLOY state")
        if isDescending == "False":
            if hasReachApogee == "True":
                if sensors.flight_state(altitude_list) == "descending":
                    isDescending = "True"
                    print("IS DESCENDING")
        
        else:
            if parachute_deployed == "False" and altitude < SECOND_PARACHUTE_ALTITUDE:
                parachute_deployed = "True"
                eeprom.modify("parachute_deployed", "True")
                #electro.parachute_nicrom_on()
                #tim_parachute_nichrom.init(period=NICROM_TIME_ON, callback=stop_parachute_nichrom, mode=Timer.ONE_SHOT)
                print("PARACHUTE DEPLOYED AT: {}".format(altitude))
        
            if altitude < PAYLOAD_DEPLOY_ALTITUDE and nicrom_payload == False:
                #electro.payload_nicrom_on()
                nicrom_payload = True
                #tim_payload_nichrom.init(period=NICROM_TIME_ON, callback=stop_payload_nichrom, mode=Timer.ONE_SHOT)
                print("PAYLOAD NICROM ON: {}".format(altitude))

    elif current_state == "DEPLOY":
        if entry == True:
            #electro.start_motor()
            #_thread.start_new_thread(second_thread, ())
            entry = False
            tp_released = "True"
            tp_is_descending = "True"
            eeprom.modify("tp_released", "True")
            eeprom.modify("tp_deploy_time", str(time.ticks_ms()))
            eeprom.modify("tp_is_descending", "True")
            print("PAYLOAD DESCENDING: {}".format(altitude))
            
    # Check for LANDED state
        elif (tp_is_descending == "False"):
            landed = sensors.check_for_landed(altitude_list)
            if landed == True:
                current_state = "LANDED"
                eeprom.modify("current_state", "LANDED")
                print("LANDED AT: {}".format(altitude))
            
        
    elif current_state == "LANDED":
        if done == False:
            send_telemetry = "False"
            #tim_container.deinit()
            #tim_payload.deinit()
            eeprom.modify("send_telemetry", "False")
            done = True
        
            # power on audio beacon
            tim_buzzer.init(period=BUZZER_TIME, callback=toggle_buzzer, mode=Timer.PERIODIC)
