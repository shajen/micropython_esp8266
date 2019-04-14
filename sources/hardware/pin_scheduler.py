import machine
import utils
import utime

SECONDS_IN_DAY = 24 * 60 * 60
SCHEDULER_MARGIN = 30 * 60

class PinScheduler():
    def __init__(self, pin, periods):
        self.pin = pin
        self.pin.value(True)
        self.periods = periods
        self.updateTimer = utils.timer()
        self.syncTimer = utils.timer()
        self.updateTimer.init(period=1000, mode=machine.Timer.PERIODIC, callback=lambda t: self.update())
        self.syncTimer.init(period=3600000, mode=machine.Timer.PERIODIC, callback=lambda t: self.sync())
        self.sync()

    def sync(self):
        if not self.isTimeNearScheduler():
            utils.syncDatetime()

    def update(self):
        secondsFromMidnight = utime.time() % SECONDS_IN_DAY
        state = False
        for (startTime, spentTime) in self.periods:
            startTime = self.timeToSecondsFromMidnight(startTime)
            if startTime <= secondsFromMidnight and secondsFromMidnight <= startTime + spentTime:
                state = True
        self.pin.value(not state)
        utils.printDebug("PIN_SCHEDULER", "set state %d" % state)

    def isTimeNearScheduler(self):
        secondsFromMidnight = utime.time() % SECONDS_IN_DAY
        for (startTime, spentTime) in self.periods:
            startTime = self.timeToSecondsFromMidnight(startTime)
            if startTime - SCHEDULER_MARGIN <= secondsFromMidnight and secondsFromMidnight <= startTime + SCHEDULER_MARGIN:
                return True
        return False

    def timeToSecondsFromMidnight(self, date):
        (hours, minutes, seconds) = date
        return (hours * 60 + minutes) * 60 + seconds
