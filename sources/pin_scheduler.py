from config import SCHEDULER_PIN1, SCHEDULER_PIN1_PERIODS
from utils import printDebug
import machine
import utime

SECONDS_IN_DAY = 24 * 60 * 60
SCHEDULER_MARGIN = 30 * 60

class PinScheduler():
    def __init__(self):
        self.pin = machine.Pin(SCHEDULER_PIN1, machine.Pin.OUT)
        self.pin.value(True)

    def update(self):
        secondsFromMidnight = utime.time() % SECONDS_IN_DAY
        state = False
        for (startTime, spentTime)  in SCHEDULER_PIN1_PERIODS:
            startTime = self.timeToSecondsFromMidnight(startTime)
            if startTime <= secondsFromMidnight and secondsFromMidnight <= startTime + spentTime:
                state = True
        self.pin.value(not state)
        printDebug("PIN_SCHEDULER", "set state %d" % state)

    def isTimeNearScheduler(self):
        secondsFromMidnight = utime.time() % SECONDS_IN_DAY
        for (startTime, spentTime)  in SCHEDULER_PIN1_PERIODS:
            startTime = self.timeToSecondsFromMidnight(startTime)
            if startTime - SCHEDULER_MARGIN <= secondsFromMidnight and secondsFromMidnight <= startTime + SCHEDULER_MARGIN:
                return True
        return False

    def timeToSecondsFromMidnight(self, date):
        (hours, minutes, seconds) = date
        return (hours * 60 + minutes) * 60 + seconds
