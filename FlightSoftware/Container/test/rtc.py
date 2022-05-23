##########################################
### This Code is for Raspberry Pi Pico ###
###      copyright 2021 balance19      ###
##########################################

from rtc import RTC_DS3231
import time

#initialisation of RTC object. Several settings are possible but everything is optional. If you meet the standards (see /my_lib/RTC_DS3231.py) no parameter's needed.
rtc = RTC_DS3231.RTC(port=1, sda_pin=14, scl_pin=15)

# It is encoded like this sec min hour week day month year
#rtc.DS3231_SetTime(NowTime = b'\x00\x25\x14\x18\x08\x05\x22')    #remove comment to set time. Do this only once otherwise time will be set everytime the code is executed.

while True:
    t = rtc.DS3231_ReadTime(3)  #read RTC and receive data in Mode 1 (see /my_lib/RTC_DS3231.py)
    print(t)
    time.sleep(1)