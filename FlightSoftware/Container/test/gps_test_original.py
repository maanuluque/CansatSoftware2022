import time
import os
from gps import pgps

while True:
    data = pgps.get_data()
    