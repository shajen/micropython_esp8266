from config import DEBUG
import utime
import ntptime
import machine

def printLog(label, message):
    year, month, day, _, hour, minute, second, ms = machine.RTC().datetime()
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    print("[%s%d-%02d-%02d %02d:%02d:%02d:%03d%s] [%s%7s%s] %s" % (YELLOW, year, month, day, hour, minute, second, ms, ENDC, GREEN, label, ENDC, message))

def printDebug(label, message):
    if DEBUG:
        printLog(label, message)

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

def httpGet(url):
    try:
        import socket
        printDebug('HTTP', 'start GET %s' % url)
        _, _, host, path = url.split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.settimeout(3.0)
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        s.close()
        printDebug("HTTP", "finish GET")
    except Exception as e:
        printLog('HTTP', 'GET timeout %s' % url)
        printLog('HTTP', 'GET exception: %s' % e)
