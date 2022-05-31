from xbee import utils

class XBeePacket():
    def __init__(self, api_frame_type):
        self.frame_type = api_frame_type
        self.frame_id = 0
        self.data = None
        
    def output(self):
        packet_raw = bytearray()
        packet_raw.append(0x7E)
        frame_spec_data = self.get_frame_spec_data()
        packet_raw += utils.int_to_length(len(frame_spec_data)) + frame_spec_data
        packet_raw.append(self.get_checksum())
        return packet_raw
        
    def get_checksum(self):
        return 0xFF - (sum(self.get_frame_spec_data()) & 0xFF)
    
    def get_frame_data(self):
        return self.data.decode()
    
    def get_frame_spec_data(self):
        return None
    
    def get_frame_type(self):
        return self.frame_type
    
    def get_frame_id(self):
        return self.frame_id
    
class ReceivePacket(XBeePacket):
    def __init__(self, x64bit_addr, x16bit_addr, rx_options, rf_data = None):
        super().__init__(0x90)
        self.x64bit_addr = x64bit_addr
        self.x16bit_addr = x16bit_addr
        self.rx_options = rx_options
        self.data = rf_data
    
    def create_packet(raw):
        return ReceivePacket(raw[4:12], raw[12:14], raw[14], raw[15:-1])
    
    def get_frame_spec_data(self):
        data = bytearray()
        data.append(self.frame_type)
        data += self.x64bit_addr
        data += self.x16bit_addr
        data.append(self.rx_options)
        data += self.get_frame_data()
        return data
        
class TransmitPacket(XBeePacket):
    def __init__(self, frame_id, x64bit_addr, x16bit_addr, broadcast_radius, tx_options, rf_data = None):
        if frame_id > 255 or frame_id < 0:
            frame_id = 0
        
        super().__init__(0x10)
        self.frame_id = frame_id
        self.x64bit_addr = x64bit_addr
        self.x16bit_addr = x16bit_addr
        self.broadcast_radius = broadcast_radius
        self.tx_options = tx_options
        self.data = rf_data
        
    def create_packet(raw):
        return TransmitPacket(raw[4], raw[5:13], raw[13:15], raw[15], raw[16], raw[17:-1])
    
    def get_frame_spec_data(self):
        data = bytearray()
        data.append(self.frame_type)
        data.append(self.frame_id)
        data += self.x64bit_addr
        data += self.x16bit_addr
        data.append(self.broadcast_radius)
        data.append(self.tx_options)
        data += self.get_frame_data()
        return data
    
class ExplicitRXIndicatorPacket(XBeePacket):
    def __init__(self, x64bit_addr, x16bit_addr, src_endpoint, dest_endpoint,
                 cluster_id, profile_id, rx_options, rf_data=None):
        super().__init__(0x91)
        self.x64bit_addr = x64bit_addr
        self.x16bit_addr = x16bit_addr
        self.src_endpoint = src_endpoint
        self.dest_endpoint = dest_endpoint
        self.cluster_id = cluster_id
        self.profile_id = profile_id
        self.rx_options = rx_options
        self.data = rf_data
        
    def create_packet(raw):
        return ExplicitRXIndicatorPacket(raw[4:12], raw[12:14], raw[14], raw[15], raw[16:18], raw[18:20], raw[20], raw[21:-1])
    
    def get_frame_spec_data(self):
        data = bytearray()
        data.append(self.frame_type)
        data += self.x64bit_addr
        data += self.x16bit_addr
        data.append(self.src_endpoint)
        data.append(self.dest_endpoint)
        data += self.cluster_id
        data += self.profile_id
        data.append(self.rx_options)
        data += self.get_frame_data()
        return data
    
class TransmitStatusPacket(XBeePacket):
    def __init__(self, frame_id, x16bit_addr, tx_retry_count, delivery_status = 0, discovery_status = 0):
        if frame_id > 255 or frame_id < 0:
            frame_id = 0
        
        super().__init__(0x8B)
        self.frame_id = frame_id
        self.x16bit_addr = x16bit_addr
        self.tx_retry_count = tx_retry_count
        self.delivery_status = delivery_status
        self.discovery_status = discovery_status
        
    def create_packet(raw):
        return TransmitStatusPacket(raw[4], raw[5:7], raw[7], raw[8], raw[9])
    
    def get_frame_spec_data(self):
        data = bytearray()
        data.append(self.frame_type)
        data.append(self.frame_id)
        data += self.x16bit_addr
        data.append(tx_retry_count)
        data.append(delivery_status)
        data.append(discovery_status)
        return data
    

class RemoteATCommandPacket(XBeePacket):
    def __init__(self, frame_id, x64bit_addr, x16bit_addr, tx_options,
                 command, parameter=None):
        if frame_id > 255 or frame_id < 0:
            frame_id = 0
        super().__init__(0x17)
        self._frame_id = frame_id
        self.x64bit_addr = x64bit_addr
        self.x16bit_addr = x16bit_addr
        self.tx_options = tx_options
        cmd = command.encode(encoding='utf8')
        while len(cmd) != 2:
            cmd += b'?'
        self.cmd = cmd
        self.param = parameter
    
    def create_packet(raw):
        return RemoteATCommandPacket(raw[4], raw[5:13], raw[13:15], raw[15], raw[16:18], raw[18:-1])
    
    def get_frame_spec_data(self):
        data = bytearray()
        data.append(self.frame_type)
        data.append(self.frame_id)
        data += self.x64bit_addr
        data += self.x16bit_addr
        data.append(self.tx_options)
        data += self.cmd
        data += self.param
        return data
        
class RemoteATCommandResponsePacket(XBeePacket):
    def __init__(self, frame_id, x64bit_addr, x16bit_addr, command,
                 status, response=None):
        if frame_id > 255 or frame_id < 0:
            frame_id = 0
        super().__init__(0x97)
        self.frame_id = frame_id
        self.x64bit_addr = x64bit_addr
        self.x16bit_addr = x16bit_addr
        self.cmd = command
        self.status = status
        self.response = response
    
    def create_packet(raw):
        return RemoteATCommandResponsePacket(raw[4], raw[5:13], raw[13:15], raw[15:17], raw[17], raw[18:-1])
    
    def get_frame_spec_data(self):
        data = bytearray()
        data.append(self.frame_type)
        data.append(self.frame_id)
        data += self.x64bit_addr
        data += self.x16bit_addr
        data += self.cmd
        data += self.status
        data += self.response
        return data