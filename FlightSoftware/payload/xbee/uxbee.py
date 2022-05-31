from machine import UART, Pin
import ubinascii
import time
from xbee.common import *


class Uxbee:
    def __init__(self, channel, tx, rx, timeout): #8 9 2000 
        self.uart = UART(channel, baudrate=9600, tx=Pin(tx), rx=Pin(rx), timeout=timeout)
        self.received = 0
        self.lost = 0
        
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
            next_byte = self.read_next_byte()
            if (next_byte == None):
                return None
            
            if (next_byte != b'~'):
                length_packet += next_byte
            else:
                self.lost += 1
                print("Lost: {}".format(self.get_lost()))
                new_packet = bytearray()
                new_packet += next_byte
                try:
                    ans = self.wait_for_packet_length(new_packet)
                    return ans
                except:
                    return None
            
        xbee_packet += length_packet
        length = length_packet[0] << 8 | length_packet[1]
        return self.wait_for_data(xbee_packet, length)
        
    def wait_for_data(self, xbee_packet, length):
        # Add packet payload
        for _ in range(length):
            next_byte = self.read_next_byte()
            if (next_byte == None):
                return None
            
            if (next_byte != b'~'):
                xbee_packet += next_byte
            else:
                self.lost += 1
                print("Lost: {}".format(self.get_lost()))
                new_packet = bytearray()
                new_packet += next_byte
                try:
                    ans = self.wait_for_packet_length(new_packet)
                    return ans
                except:
                    return None
            
        # Add packet checksum
        checksum = self.read_next_byte()
        if (checksum == None):
            return None
        
        if (checksum != b'~'):
            xbee_packet += checksum
        else:
            self.lost += 1
            print("Lost: {}".format(self.get_lost()))
            new_packet = bytearray()
            new_packet += checksum
            try:
                ans = self.wait_for_packet_length(new_packet)
                return ans
            except:
                return None
        
        # Return packet
        return self.get_packet(xbee_packet, checksum)
    
    def get_packet(self, packet_bytearray, checksum):
        checksum = 0xFF - (sum(packet_bytearray[3:-1]) & 0xFF)
        if (checksum != packet_bytearray[-1]):
            self.lost += 1
            print("Lost: {}".format(self.get_lost()))
            return None
        frame_type = packet_bytearray[3]
        #print("RAW PACKET READ: {}".format(packet_bytearray))
        #print("FRAME TYPE --> {}".format(frame_type))
        if (frame_type == 0x90):
            return ReceivePacket.create_packet(packet_bytearray)
        elif (frame_type == 0x91):
            return ExplicitRXIndicatorPacket.create_packet(packet_bytearray)
        elif (frame_type == 0x8B):
            return TransmitStatusPacket.create_packet(packet_bytearray)
        elif (frame_type == 0x10):
            return TransmitPacket.create_packet(packet_bytearray)
        elif (frame_type == 0x97):
            return RemoteATCommandResponsePacket.create_packet(packet_bytearray)
        else:
            return None
        
    def send_packet(self, frame_id, x64bit_addr, x16bit_addr, data):
        #print("XBEE: Data --> " + data)
        data = data.encode("utf-8")
        #print("XBEE: Encoded Data --> {}".format(data))
        packet = TransmitPacket(frame_id, x64bit_addr, x16bit_addr, 0, 0, data)
        #print("SENDING RAW: {}".format(packet.output()))
        #print("XBEE: Packet --> {}".format(packet.output()))
        self.uart.write(packet.output())
        
    def send_remote_at_command(self, frame_id, x64bit_addr, x16bit_addr, options, command, parameter):
        packet = RemoteATCommandPacket(frame_id, x64bit_addr, x16bit_addr, options, command, parameter)
        print("About to send {}".format(packet.output()))
        self.uart.write(packet.output())
        
    def get_received(self):
        return self.received
    
    def get_lost(self):
        return self.lost
        
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
        print("Waiting for simp")
        wait = True
        while wait:
            packet = self.wait_for_read()
            if packet != None:
                data = packet.get_frame_data().split(',')
                print("PACKET DATA: {}".format(data))
                if data[2] == 'SIMP':
                    wait = False
        print("Returning: {}".format(data[3]))
        return data[3]
        




