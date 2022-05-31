from xbee import uxbee
import ubinascii
import time

xbee = uxbee.Uxbee(channel = 1, tx = 8, rx = 9, timeout = 250)
payload_xbee = uxbee.Uxbee(channel = 0, tx = 16, rx = 17, timeout = 250)

GROUND_MAC = ubinascii.unhexlify("0013A20041BA29C8")
GROUND_IP = ubinascii.unhexlify("607A")

PAYLOAD_MAC = ubinascii.unhexlify("0013A20041B11802")
PAYLOAD_IP = ubinascii.unhexlify("E6D5")

counter = 0

def receive_payload_package():
    global counter
    command = payload_xbee.read_command()
    if command != 0:
        print('Received from Payload!')
        packet = payload_xbee.wait_for_frame()
        if packet != None:
            frame_type = packet.get_frame_type()
            if (frame_type == 0x90 or frame_type == 0x91):
                data = packet.get_frame_data()
                print("Data: {}".format(data))
                counter += 1
                xbee.send_packet(0, GROUND_MAC, GROUND_IP, data)
    else:
        print('COUNTER: {}'.format(counter))
                
while True:
    receive_payload_package()
    time.sleep(0.5)