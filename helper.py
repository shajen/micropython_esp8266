import utime

def printLog(label, message):
    year, month, day, hour, minute, second, _, _ = utime.localtime()
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    print("[%s%s%s][%s%d-%02d-%02d %02d:%02d:%02d%s] %s" % (GREEN, label, ENDC, YELLOW, year, month, day, hour, minute, second, ENDC, message))
