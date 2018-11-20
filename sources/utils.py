import config
import utime
import ntptime
import machine
import socket

def printLog(label, message):
    year, month, day, _, hour, minute, second, ms = machine.RTC().datetime()
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    print("[%s%d-%02d-%02d %02d:%02d:%02d:%03d%s] [%s%14s%s] %s" % (YELLOW, year, month, day, hour, minute, second, ms, ENDC, GREEN, label, ENDC, message))

def printDebug(label, message):
    if config.DEBUG:
        printLog(label, message)

def syncDatetime():
    for i in range(1, 4):
        try:
            printLog('NTP', '%d try' % i)
            ntptime.settime()
            tm = utime.localtime(utime.time() + 1 * 60 * 60) # +2h
            tm = tm[0:3] + (0,) + tm[3:6] + (0,)
            machine.RTC().datetime(tm)
            printLog('NTP', 'success')
            return
        except:
            printLog('NTP', 'ERROR')
    machine.reset()

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

