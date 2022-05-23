from xbee import uxbee
from xbee.common import *
import ubinascii
import time

AMOUNT_OF_PACKETS = 100

xbee = uxbee.Uxbee(tx = 8, rx = 9, timeout = 2000)

# Transforms string into bytearray -> Better to do this,
# since addresses will always be the same, so this operation
# needs to be done only once
x64bit_addr = ubinascii.unhexlify("0013A20041BA29C8")
x16bit_addr = ubinascii.unhexlify("CC30")

# Data in string -> is encoded before every send
data = "[PACKET {}] {}"
message = "Hello XBee!"

print('GO')

for i in range(AMOUNT_OF_PACKETS):
    frame_id = i
    xbee.send_packet(frame_id, x64bit_addr, x16bit_addr, data.format(frame_id, message))
    time.sleep(0.25) # This is not mandatory (sleep in seconds)