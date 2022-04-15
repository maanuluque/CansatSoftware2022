from machine import UART, Pin
import ubinascii

class uxbee:
    
    
    def __init__(self, tx, rx, timeout): #tx 8, rx 9
        self.uart = UART(1, baudrate=9600, tx=Pin(tx), rx=Pin(rx), timeout=timeout)
    
    def send_packet(self, frame_id, dest_addr_64, dest_addr_16, data):
        start_delimiter = "7E"
        frame_type = "10"
        
        frame_hex = hex(frame_id).split('x')[-1]
        if len(frame_hex) < 2:
            frame_hex = '0' + frame_hex
        
        data_hex = ubinascii.hexlify(data).decode('utf8')
        frame_data = frame_type + frame_hex + dest_addr_64 + dest_addr_16 + "0000" + data_hex
        
        byte_data_len = int(len(frame_data) / 2)
        hex_data_len = hex(byte_data_len).split('x')[-1]
        
        for i in range(len(hex_data_len), 4):
            hex_data_len = "0" + hex_data_len
        
        frame_data = frame_data.encode()
        n = 2
        arr = [frame_data[i:i+n] for i in range(0, len(frame_data), n)]
        hex_arr = [int(i, 16) for i in arr]
        checksum_data_sum = hex(sum(hex_arr))
        hex_sum = int("0x" + checksum_data_sum[-2:])
        checksum = hex(0xFF - hex_sum).split('x')[-1]
                
        packet = start_delimiter + hex_data_len + frame_data.decode() + checksum
        
        packet_bin = ubinascii.unhexlify(packet)
        
        self.uart.write(packet_bin)
        
        
        
        
        