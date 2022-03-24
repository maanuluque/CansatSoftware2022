import machine

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
#mpu = MPU9250(i2c)
print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))