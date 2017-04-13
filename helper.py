import utime
import ntptime
import machine

def printLog(label, message):
    year, month, day, _, hour, minute, second, ms = machine.RTC().datetime()
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    print("[%s%s%s][%s%d-%02d-%02d %02d:%02d:%02d:%03d%s] %s" % (GREEN, label, ENDC, YELLOW, year, month, day, hour, minute, second, ms, ENDC, message))

def syncDatetime():
    for i in range(1, 10):
        try:
            ntptime.settime()
            tm = utime.localtime(utime.time() + 2 * 60 * 60) # +2h
            tm = tm[0:3] + (0,) + tm[3:6] + (0,)
            machine.RTC().datetime(tm)
            break
        except:
            printLog('SYNC', 'ERROR')
