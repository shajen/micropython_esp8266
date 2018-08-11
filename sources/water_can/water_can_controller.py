from config import PUMP_PIN, PUMP_START, PUMP_TIME
from utils import printDebug
import machine
import utime

class WaterCanController():
    def __init__(self):
        self.pin = machine.Pin(PUMP_PIN, machine.Pin.OUT)
        self.pin.value(True)

    def update(self):
        secondsFromMidnight = utime.time() % 86400
        state = False
        for startTime in PUMP_START:
            if startTime <= secondsFromMidnight and secondsFromMidnight <= startTime + PUMP_TIME:
                state = True
        self.pin.value(not state)
        printDebug("WATER", "set state %d" % state)
