import machine
import time

enca = machine.Pin(9, machine.Pin.IN)
encb = machine.Pin(8, machine.Pin.IN)

pos = 0

###
#     *********     *********     *********     *********     *********     *********
#   ..*...... *   ..*...... *   ..*...... *   ..*...... *   ..*...... *   ..*...... *
#   . *     . *   . *     . *   . *     . *   . *     . *   . *     . *   . *     . *
#   . *     . *   . *     . *   . *     . *   . *     . *   . *     . *   . *     . *
# ...**     ..*....**     ..*....**     ..*....**     ..*....**     ..*....**     ..*...
#
# .A *B
###

def read_encoder(pin):
    #timer = time.ticks_us()
    global pos
    
    b = encb.value()
    a = enca.value()
    if b > 0:
        if a > 0:
            pos -= 1
        else:
            pos += 1
    else:
        if a > 0:
            pos += 1
        else:
            pos -= 1
    if pos > 419:
        pos -= 420
    elif pos < 0:
        pos += 420
    #end = time.ticks_us() - timer
    #print("TIME ELAPSED: {}".format(end))
        
enca.irq(handler=read_encoder, hard=True)

#debouncing = time.ticks_us()
while True:
    #motor_pos = pos * 360 / 210
    #print("Pos: {}".format(motor_pos))
    print("Steps: {}".format(pos))
    time.sleep(0.5)
    
        
