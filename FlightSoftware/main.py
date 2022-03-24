import os

try:
    os.mkdir('data')
except OSError:
    pass 
file = open('eeprom.txt', 'a+')
for i in range(10):
    file.write("some data " + str(i))
print(file.readlines())
print(os.listdir())
file.close()
