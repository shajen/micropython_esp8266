import config
import utime
import ntptime
import machine
import socket
import ujson

def printLog(label, message):
    year, month, day, _, hour, minute, second, ms = machine.RTC().datetime()
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    print("[%s%d-%02d-%02d %02d:%02d:%02d:%03d%s] [%s%14s%s] %s" % (YELLOW, year, month, day, hour, minute, second, ms, ENDC, GREEN, label, ENDC, message))

def printDebug(label, message):
    if config.DEBUG:
        printLog(label, message)

__TIMERS = []
def timer():
    global __TIMERS
    t = machine.Timer(len(__TIMERS))
    __TIMERS.append(t)
    printDebug('TIMER', 'create new (total: %d)' % len(__TIMERS))
    return t

def deleteTimers():
    global __TIMERS
    for t in __TIMERS:
        printDebug('TIMER', 'delete')
        t.deinit()

def getTimeZone():
    t = utime.time()
    if utime.mktime((2019, 3, 31, 2, 0, 0, 0, 0)) <= t and t <= utime.mktime((2019, 10, 27, 3, 0, 0, 0, 0)):
        return 2
    elif utime.mktime((2020, 3, 29, 2, 0, 0, 0, 0)) <= t and t <= utime.mktime((2020, 10, 25, 3, 0, 0, 0, 0)):
        return 2
    elif utime.mktime((2021, 3, 28, 2, 0, 0, 0, 0)) <= t and t <= utime.mktime((2021, 10, 31, 3, 0, 0, 0, 0)):
        return 2
    return 1

def syncDatetime():
    for i in range(1, 4):
        try:
            printLog('NTP', '%d try' % i)
            ntptime.settime()
            tm = utime.localtime(utime.time() + getTimeZone() * 60 * 60)
            tm = tm[0:3] + (0,) + tm[3:6] + (0,)
            machine.RTC().datetime(tm)
            printLog('NTP', 'success')
            return True
        except Exception as e:
            printLog('NTP', 'exception')
            printLog('NTP', e)
    return False

def createSyncDateTimeTimer(interval_ms = 60000, sync_on_start = True):
    t = timer()
    t.init(period=interval_ms, mode=machine.Timer.PERIODIC, callback=lambda t: syncDatetime())
    if sync_on_start:
        syncDatetime()
    return t

def httpGet(url):
    try:
        printDebug('HTTP', 'start GET %s' % url)
        _, _, host, path = url.split('/', 3)
        s = socket.socket()
        s.settimeout(3.0)
        s.connect(('91.185.185.211', 80))
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        s.close()
        printDebug("HTTP", "finish GET")
    except Exception as e:
        printDebug('HTTP', 'GET timeout %s' % url)
        printDebug('HTTP', 'GET exception: %s' % e)

def chipId():
    id = machine.unique_id()
    return '%02x%02x%02x' % (id[2], id[1], id[0])

def writeJson(file, json):
    f = open(file, "w")
    f.write(ujson.dumps(json))
    f.close()
    printDebug("JSON", "write json to {} success".format(file))

def readJson(file):
    try:
        f = open(file, "r")
        data = f.read()
        f.close()
        printDebug("JSON", "read json from {} success".format(file))
        return ujson.loads(data)
    except:
        printDebug("JSON", "read json from {} failed".format(file))
        return None

def jsonResponse(status, message):
    return ujson.dumps({"status": status, "message": message})

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def str2float(v):
    return float(v)
