class TpSensorModule:
    def __init__(self):
        i2c_bme = machine.I2C(1, scl=machine.Pin(11), sda=machine.Pin(10))
        self.bme = bme280.BME280(i2c=i2c)
        i2c_mpu = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
        self.mpu = MPU9250(i2c)
        
    def get_altitude(self):
        return self.bme.altitude

    def get_gyro(self):
        return self.mpu.gyro
    
    def get_acceleration(self):
        return self.mpu.acceleration