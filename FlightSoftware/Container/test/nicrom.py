from electromechanical import em
import time

electro = em.EM()

electro.payload_nicrom_on()
time.sleep(5)
electro.payload_nicrom_off()