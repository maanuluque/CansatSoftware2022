from xbee import uxbee
import ubinascii
import time

GROUND_MAC = ubinascii.unhexlify("0013A20041BA29C8")
PAYLOAD_MAC = ubinascii.unhexlify("0013A20041B11802")
DEFAULT_IP = ubinascii.unhexlify("FFFE")

payload_ip = bytearray()
ground_ip = bytearray()

TIMEOUT = 250
actual_time = 0

command = 'MY'

xbee = uxbee.Uxbee(channel = 1, tx = 8, rx = 9, timeout = 250)

def get_device_ip(DEVICE_MAC):
    packet = xbee.send_remote_at_command(1, DEVICE_MAC, DEFAULT_IP, 0x02, command, '')
    actual_time = time.ticks_ms()
    packet = None
    while True:
        if xbee.read_command() != 0:
            packet = xbee.wait_for_frame()
            if packet is not None:
                if packet.get_frame_type() == 0x97:
                    if packet.response is not None:
                        return packet.response
        
        
        if time.ticks_ms() - actual_time > TIMEOUT:
            print("Timeout: Retrying")
            packet = xbee.send_remote_at_command(1, DEVICE_MAC, DEFAULT_IP, 0x02, command, '')
            actual_time = time.ticks_ms()

def network_discovery():
    global ground_ip
    global payload_ip
    ground_ip = get_device_ip(GROUND_MAC)
    print('GROUND IP: {}'.format(ground_ip))
    payload_ip = get_device_ip(PAYLOAD_MAC)
    print('PAYLOAD IP: {}'.format(payload_ip))
    
    
print('Starting...')
network_discovery()

xbee.send_packet(0, GROUND_MAC, ground_ip, "I DISCOVERED YOU, GROUND!")
xbee.send_packet(0, PAYLOAD_MAC, payload_ip, "I DISCOVERED YOU, PAYLOAD!")
print('Done!')