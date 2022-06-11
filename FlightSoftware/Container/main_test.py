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
#plist = [101000,101000,101000,100936,100872,100744,100680,100552,100488,100360,100296,100232,100168,100104,100040,99976,99912,99848,99784,99720,99656,99592,99528,99464,99400,99336,99272,99208,99144,99080,99016,98952,98888,98824,98760,98696,98632,98568,98504,98440,98376,98312,98248,98184,98120,98056,97992,97928,97864,97800,97736,97672,97608,97544,97480,97416,97352,97288,97224,97160,97096,97032,96968,96904,96840,96776,96712,96648,96584,96520,96456,96392,96328,96264,96200,96136,96072,96008,95944,95880,95816,95752,95688,95624,95560,95496,95432,95368,95304,95240,95176,95112,95048,94984,94920,94856,94792,94728,94664,94600,94536,94472,94408,94344,94280,94216,94152,94088,94024,93960,93896,93832,93768,93704,93640,93576,93512,93448,93384,93320,93256,93192,93128,93064,93000,92936,92872,92808,92744,92760,92776,92792,92808,92824,92840,92856,92872,92888,92904,92920,92936,92952,92968,92984,93000,93016,93032,93048,93064,93080,93096,93112,93128,93144,93160,93176,93192,93208,93224,93240,93256,93272,93288,93304,93320,93336,93352,93368,93384,93400,93416,93432,93448,93464,93480,93496,93512,93528,93544,93560,93576,93592,93608,93624,93640,93656,93672,93688,93704,93720,93736,93752,93768,93784,93800,93816,93832,93848,93864,93880,93896,93912,93928,93944,93960,93976,93992,94008,94024,94040,94056,94072,94088,94104,94120,94136,94152,94168,94184,94200,94216,94232,94248,94264,94280,94296,94312,94328,94344,94360,94376,94392,94408,94424,94440,94456,94472,94488,94504,94520,94536,94552,94568,94584,94600,94616,94632,94648,94664,94680,94696,94712,94728,94744,94760,94776,94792,94808,94824,94840,94856,94872,94888,94904,94920,94936,94952,94968,94984,95000,95016,95032,95048,95064,95080,95096,95112,95128,95144,95160,95176,95192,95208,95224,95240,95256,95272,95288,95304,95320,95336,95352,95368,95384,95400,95416,95432,95448,95464,95480,95496,95512,95528,95544,95560,95576,95592,95608,95624,95640,95656,95672,95688,95704,95720,95736,95752,95768,95784,95800,95816,95832,95848,95864,95880,95896,95912,95928,95944,95960,95976,95992,96008,96024,96040,96056,96072,96088,96104,96120,96136,96152,96168,96184,96200,96216,96232,96248,96264,96280,96296,96312,96328,96344,96360,96376,96392,96408,96424,96440,96456,96472,96488,96504,96520,96536,96552,96568,96584,96600,96616,96632,96648,96664,96680,96696,96712,96728,96744,96760,96776,96792,96808,96824,96840,96856,96872,96888,96904,96920,96936,96952,96968,96984,97000,97016,97032,97048,97064,97080,97096,97112,97128,97144,97160,97176,97192,97208,97224,97240,97256,97272,97288,97304,97320,97336,97352,97368,97384,97400,97416,97432,97448,97464,97480,97496,97512,97528,97544,97560,97576,97592,97608,97624,97640,97656,97672,97688,97704,97720,97736,97752,97768,97784,97800,97816,97832,97848,97864,97880,97896,97912,97928,97944,97960,97976,97992,98008,98024,98040,98056,98072,98088,98104,98120,98136,98152,98168,98184,98200,98216,98232,98248,98264,98280,98296,98312,98328,98344,98360,98376,98392,98408,98424,98440,98456,98472,98488,98504,98520,98536,98552,98568,98584,98600,98616,98632,98648,98664,98680,98696,98712,98728,98744,98760,98776,98792,98808,98824,98840,98856,98872,98888,98904,98920,98936,98952,98968,98984,99000,99016,99032,99048,99064,99080,99096,99112,99128,99144,99160,99176,99192,99208,99224,99240,99256,99272,99288,99304,99320,99336,99352,99368,99384,99400,99416,99432,99448,99464,99480,99496,99512,99528,99544,99560,99576,99592,99608,99624,99640,99656,99672,99688,99704,99720,99736,99752,99768,99784,99800,99816,99832,99848,99864,99880,99896,99912,99928,99944,99960,99976,99992,100008,100024,100040,100056,100072,100088,100104,100120,100136,100152,100168,100184,100200,100216,100232,100248,100264,100280,100296,100312,100328,100344,100360,100376,100392,100408,100424,100440,100456,100472,100488,100504,100520,100536,100552,100568,100584,100600,100616,100632,100648,100664,100680,100696,100712,100728,100744,100760,100776,100792,100808,100824,100840,100856,100872,100888,100904,100920,100936,100952,100968,100984,101000,101016]
plist = [101000,101000,101000,101000.00,100862.40,100724.80,100587.20,100449.60,100312.00,100174.40,100036.80,99899.20,99761.60,99624.00,99486.40,99348.80,99211.20,99073.60,98936.00,98798.40,98660.80,98523.20,98385.60,98248.00,98110.40,97972.80,97835.20,97697.60,97560.00,97422.40,97284.80,97147.20,97009.60,96872.00,96734.40,96596.80,96459.20,96321.60,96184.00,96046.40,95908.80,95771.20,95633.60,95496.00,95358.40,95220.80,95083.20,94945.60,94808.00,94670.40,94532.80,94395.20,94257.60,94120.00,93982.40,93844.80,93707.20,93569.60,93432.00,93294.40,93156.80,93019.20,92881.60,92812.80,92825.59,92838.38,92851.18,92863.97,92876.76,92889.55,92902.35,92915.14,92927.93,92940.72,92953.52,92966.31,92979.10,92991.89,93004.69,93017.48,93030.27,93043.06,93055.86,93068.65,93081.44,93094.23,93107.03,93119.82,93132.61,93145.40,93158.20,93170.99,93183.78,93196.57,93209.37,93222.16,93234.95,93247.74,93260.54,93273.33,93286.12,93298.91,93311.71,93324.50,93337.29,93350.08,93362.88,93375.67,93388.46,93401.25,93414.05,93426.84,93439.63,93452.42,93465.22,93478.01,93490.80,93503.59,93516.39,93529.18,93541.97,93554.76,93567.56,93580.35,93593.14,93605.93,93618.73,93631.52,93644.31,93657.10,93669.90,93682.69,93695.48,93708.27,93721.07,93733.86,93746.65,93759.44,93772.24,93785.03,93797.82,93810.61,93823.41,93836.20,93848.99,93861.78,93874.58,93887.37,93900.16,93912.95,93925.75,93938.54,93951.33,93964.12,93976.92,93989.71,94002.50,94015.29,94028.09,94040.88,94053.67,94066.46,94079.26,94092.05,94104.84,94117.63,94130.43,94143.22,94156.01,94168.80,94181.60,94194.39,94207.18,94219.97,94232.77,94245.56,94258.35,94271.14,94283.94,94296.73,94309.52,94322.31,94335.11,94347.90,94360.69,94373.48,94386.28,94399.07,94411.86,94424.65,94437.45,94450.24,94463.03,94475.82,94488.62,94501.41,94514.20,94526.99,94539.79,94552.58,94565.37,94578.16,94590.96,94603.75,94616.54,94629.33,94642.13,94654.92,94667.71,94680.50,94693.30,94706.09,94718.88,94731.67,94744.47,94757.26,94770.05,94782.84,94795.64,94808.43,94821.22,94834.01,94846.81,94859.60,94872.39,94885.18,94897.98,94910.77,94923.56,94936.35,94949.15,94961.94,94974.73,94987.52,95000.32,95013.11,95025.90,95038.69,95051.49,95064.28,95077.07,95089.86,95102.66,95115.45,95128.24,95141.03,95153.83,95166.62,95179.41,95192.20,95205.00,95217.79,95230.58,95243.37,95256.17,95268.96,95281.75,95294.54,95307.34,95320.13,95332.92,95345.71,95358.51,95371.30,95384.09,95396.88,95409.68,95422.47,95435.26,95448.05,95460.85,95473.64,95486.43,95499.22,95512.02,95524.81,95537.60,95550.39,95563.19,95575.98,95588.77,95601.56,95614.36,95627.15,95639.94,95652.73,95665.53,95678.32,95691.11,95703.90,95716.70,95729.49,95742.28,95755.07,95767.87,95780.66,95793.45,95806.24,95819.04,95831.83,95844.62,95857.41,95870.21,95883.00,95895.79,95908.58,95921.38,95934.17,95946.96,95959.75,95972.55,95985.34,95998.13,96010.92,96023.72,96036.51,96049.30,96062.09,96074.89,96087.68,96100.47,96113.26,96126.06,96138.85,96151.64,96164.43,96177.23,96190.02,96202.81,96215.60,96228.40,96241.19,96253.98,96266.77,96279.57,96292.36,96305.15,96317.94,96330.74,96343.53,96356.32,96369.11,96381.91,96394.70,96407.49,96420.28,96433.08,96445.87,96458.66,96471.45,96484.25,96497.04,96509.83,96522.62,96535.42,96548.21,96561.00,96573.79,96586.59,96599.38,96612.17,96624.96,96637.76,96650.55,96663.34,96676.13,96688.93,96701.72,96714.51,96727.30,96740.10,96752.89,96765.68,96778.47,96791.27,96804.06,96816.85,96829.64,96842.44,96855.23,96868.02,96880.81,96893.61,96906.40,96919.19,96931.98,96944.78,96957.57,96970.36,96983.15,96995.95,97008.74,97021.53,97034.32,97047.12,97059.91,97072.70,97085.49,97098.29,97111.08,97123.87,97136.66,97149.46,97162.25,97175.04,97187.83,97200.63,97213.42,97226.21,97239.00,97251.80,97264.59,97277.38,97290.17,97302.97,97315.76,97328.55,97341.34,97354.14,97366.93,97379.72,97392.51,97405.31,97418.10,97430.89,97443.68,97456.48,97469.27,97482.06,97494.85,97507.65,97520.44,97533.23,97546.02,97558.82,97571.61,97584.40,97597.19,97609.99,97622.78,97635.57,97648.36,97661.16,97673.95,97686.74,97699.53,97712.33,97725.12,97737.91,97750.70,97763.50,97776.29,97789.08,97801.87,97814.67,97827.46,97840.25,97853.04,97865.84,97878.63,97891.42,97904.21,97917.01,97929.80,97942.59,97955.38,97968.18,97980.97,97993.76,98006.55,98019.35,98032.14,98044.93,98057.72,98070.52,98083.31,98096.10,98108.89,98121.69,98134.48,98147.27,98160.06,98172.86,98185.65,98198.44,98211.23,98224.03,98236.82,98249.61,98262.40,98275.20,98287.99,98300.78,98313.57,98326.37,98339.16,98351.95,98364.74,98377.54,98390.33,98403.12,98415.91,98428.71,98441.50,98454.29,98467.08,98479.88,98492.67,98505.46,98518.25,98531.05,98543.84,98556.63,98569.42,98582.22,98595.01,98607.80,98620.59,98633.39,98646.18,98658.97,98671.76,98684.56,98697.35,98710.14,98722.93,98735.73,98748.52,98761.31,98774.10,98786.90,98799.69,98812.48,98825.27,98838.07,98850.86,98863.65,98876.44,98889.24,98902.03,98914.82,98927.61,98940.41,98953.20,98965.99,98978.78,98991.58,99004.37,99017.16,99029.95,99042.75,99055.54,99068.33,99081.12,99093.92,99106.71,99119.50,99132.29,99145.09,99157.88,99170.67,99183.46,99196.26,99209.05,99221.84,99234.63,99247.43,99260.22,99273.01,99285.80,99298.60,99311.39,99324.18,99336.97,99349.77,99362.56,99375.35,99388.14,99400.94,99413.73,99426.52,99439.31,99452.11,99464.90,99477.69,99490.48,99503.28,99516.07,99528.86,99541.65,99554.45,99567.24,99580.03,99592.82,99605.62,99618.41,99631.20,99643.99,99656.79,99669.58,99682.37,99695.16,99707.96,99720.75,99733.54,99746.33,99759.13,99771.92,99784.71,99797.50,99810.30,99823.09,99835.88,99848.67,99861.47,99874.26,99887.05,99899.84,99912.64,99925.43,99938.22,99951.01,99963.81,99976.60,99989.39,100002.18,100014.98,100027.77,100040.56,100053.35,100066.15,100078.94,100091.73,100104.52,100117.32,100130.11,100142.90,100155.69,100168.49,100181.28,100194.07,100206.86,100219.66,100232.45,100245.24,100258.03,100270.83,100283.62,100296.41,100309.20,100322.00,100334.79,100347.58,100360.37,100373.17,100385.96,100398.75,100411.54,100424.34,100437.13,100449.92,100462.71,100475.51,100488.30,100501.09,100513.88,100526.68,100539.47,100552.26,100565.05,100577.85,100590.64,100603.43,100616.22,100629.02,100641.81,100654.60,100667.39,100680.19,100692.98,100705.77,100718.56,100731.36,100744.15,100756.94,100769.73,100782.53,100795.32,100808.11,100820.90,100833.70,100846.49,100859.28,100872.07,100884.87,100897.66,100910.45,100923.24,100936.04,100948.83,100961.62,100974.41,100987.21,101000.00]
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
    a = 0
    while a < 10:
        a += 1
        print("Douuu: {}".format(a))
        time.sleep(1)
        
    tp_is_descending = "False"
    #eeprom.modify("tp_is_descending", "False")
    print("Payload Descended!")
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
CONVERSION_FACTOR = 3.3 * 1.454545454545454545
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
    voltage = get_voltage()
    package.append(str(voltage))
    
    #gps_values = gps_spio.get_nmea()
    gps_values = None
    if gps_values is None:
        for _ in range(5):
            package.append("None")
    else:
        package.append(gps_values[0])
        package.append(gps_values[1])
        package.append(gps_values[2])
        package.append(gps_values[3])
        package.append(gps_values[4])
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
    global index
    global new_sim_time
    if simulation_mode == 'True' and sim_activated == 'True':
        #sim_pressure = xbee.wait_for_simp()
        sensors.set_sea_level(plist[index])
        sim_pressure = plist[index]
        index += 1
        print("SIM PRESSURE: {}".format(sim_pressure))
        altitude = sensors.get_sim_altitude(sim_pressure)
        print("SIM ALTITUDE: {}".format(altitude))
        new_sim_time = time.ticks_ms()
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
    raw *= CONVERSION_FACTOR
    raw /= 2**12
    return raw
        
            
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

    #if send_payload_telemetry == "True":
    #    receive_payload_package()

    last_altitude = altitude
    
    if simulation_mode == 'True' and sim_activated == 'True':
        if sim_pressure is None:
            altitude = sensors.get_sim_altitude(101325)
        else:
            if time.ticks_ms() - new_sim_time > 125:
                #altitude = sensors.get_sim_altitude(sim_pressure)
                altitude = sensors.get_sim_altitude(plist[index])
                if (index < lenplist - 1):
                    index += 1
                new_sim_time = time.ticks_ms()
    else:
        altitude = sensors.get_altitude()
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
                tim_parachute_nichrom.init(period=NICROM_TIME_ON, callback=stop_parachute_nichrom, mode=Timer.ONE_SHOT)
                print("PARACHUTE DEPLOYED AT: {}".format(altitude))
        
            if altitude < PAYLOAD_DEPLOY_ALTITUDE and nicrom_payload == False:
                #electro.payload_nicrom_on()
                nicrom_payload = True
                tim_payload_nichrom.init(period=NICROM_TIME_ON, callback=stop_payload_nichrom, mode=Timer.ONE_SHOT)
                print("PAYLOAD NICROM ON: {}".format(altitude))

    elif current_state == "DEPLOY":
        if entry == True:
            #electro.start_motor()
            _thread.start_new_thread(second_thread, ())
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




