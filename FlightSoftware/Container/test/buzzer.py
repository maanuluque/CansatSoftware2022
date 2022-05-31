from electromechanical import em
import time

electro = em.EM()
while True:
    electro.toggle_buzzer()
    time.sleep(0.5)
