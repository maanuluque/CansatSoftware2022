import os

try:
    os.mkdir('data')
except OSError:
    pass
#os.remove('data/eeprom.txt')
file = open('data/eeprom.txt', 'a+')
for i in range(10):
    file.write("some data " + str(i))
    file.write('\n')
file.close()
print(os.listdir())