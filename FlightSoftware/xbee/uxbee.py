from machine import UART, Pin
import ubinascii
import time
from common import *


class uxbee:
    def __init__(self, tx, rx, timeout): #8 9 2000 
        self.uart = UART(1, baudrate=9600, tx=Pin(tx), rx=Pin(rx), timeout=timeout)
        self.received = 0
        
    def read_next_byte(self):
        return self.uart.read(1)
        
    def wait_for_frame(self):
        xbee_packet = bytearray()
        byte = self.read_next_byte()
        
        # Add packet delimiter
        xbee_packet += byte
        if (xbee_packet[0] == 0x7E):
            return self.wait_for_packet_length(xbee_packet)
        else:
            return None
            
    def wait_for_packet_length(self, xbee_packet):
        length_packet = bytearray()
        for _ in range(2):
            length_packet += self.read_next_byte()
        xbee_packet += length_packet
        length = length_packet[0] << 8 | length_packet[1]
        return self.wait_for_data(xbee_packet, length)
        
    def wait_for_data(self, xbee_packet, length):
        # Add packet payload
        for _ in range(length): 
            xbee_packet += self.read_next_byte()
            
        # Add packet checksum
        xbee_packet += self.read_next_byte()
        
        # Return packet
        return self.get_packet(xbee_packet)
    
    def get_packet(self, packet_bytearray):
        frame_type = packet_bytearray[3]
        if (frame_type == 0x90):
            return ReceivePacket.create_packet(packet_bytearray)
        elif (frame_type == 0x8B):
            return TransmitStatusPacket.create_packet(packet_bytearray)
        elif (frame_type == 0x10):
            return TransmitPacket.create_packet(packet_bytearray)
        else:
            return None
        
    def send_packet(self, frame_id, x64bit_addr, x16bit_addr, data):
        data = data.encode()
        packet = TransmitPacket(frame_id, x64bit_addr, x16bit_addr, 0, 0, data)
        self.uart.write(packet.output())
        
    def get_received(self):
        return self.received
        
    def wait_for_read(self):
        current = self.uart.any()
        while (current == 0):
            current = self.uart.any()
            
        self.received += 1
        return self.wait_for_frame()

    def read_command(self):
        current = self.uart.any()
        return current

    def wait_for_simp(self):
        wait = True
        while wait:
            packet = self.wait_for_read()
            data = packet.get_frame_data().split(',')
            if data[2] == 'SIMP':
                wait = False
        return data[3]
        