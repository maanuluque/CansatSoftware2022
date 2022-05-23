from uxbee import uxbee
from common import *
import ubinascii

xbee = uxbee(tx = 8, rx = 9, timeout = 2000)

# Transforms string into bytearray -> Better to do this,
# since addresses will always be the same, so this operation
# needs to be done only once
x64bit_addr = ubinascii.unhexlify("0013A20041B11939")
x16bit_addr = ubinascii.unhexlify("7906")

print('GO')

while (True): # Wait for any packet to be received
    packet = xbee.wait_for_read() # Waits for any received byte -> Starts building packet
    print("[PACKET {}] {}".format(xbee.get_received(), packet.output()))