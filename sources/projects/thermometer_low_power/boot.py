import machine
import network
import utime
import webrepl
import os
import utime

def printLog(message):
    ms = utime.ticks_ms()
    seconds = ms / 1000
    ms = ms % 1000
    printLog("[% 3d.%03d] %s" % (seconds, ms, message))

def detectSoftReboot():
    if utime.ticks_ms() >= 1000:
        machine.reset()

def doConnect(seconds=10):
    try:
        try:
            from config import NETWORKS
        except:
            printLog('exception during import NETWORKS')
            NETWORKS = {}
        printLog('Scanning networks...')
        network.WLAN(network.AP_IF).active(False)
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        startTime = utime.ticks_ms()
        while utime.ticks_ms() < startTime + seconds * 1000:
            nets = wlan.scan()
            for net in nets:
                ssid = net[0].decode()
                if ssid in NETWORKS:
                    printLog('Try to connect to %s' % ssid)
                    wlan.connect(ssid, NETWORKS[ssid])
                    return
            utime.sleep_ms(10)
    except:
        printLog('exception during connecting')
        printLog(e)
        machine.reset()
    printLog('Can not find any suitable network')

def waitForConnection(seconds=20):
    printLog('Waiting for connes
    ction...')
    wlan = network.WLAN(network.STA_IF)
    startTime = utime.ticks_ms()
    while utime.ticks_ms() < startTime + seconds * 1000 and not wlan.isconnected():
        utime.sleep_ms(100)
    if wlan.isconnected():
        printLog('WLAN connection succeeded!')
    else:
        printLog('WLAN connection error!')

def setWebreplPassword():
    if "webrepl_cfg.py" not in os.listdir():
        printLog('webrepl set password')
        f = open("webrepl_cfg.py", 'w')
        f.write("PASS = 'PASSWORD'\n")
        f.close()

detectSoftReboot()
printLog('Shajen development - micropython')
printLog('Reset cause %d' % machine.reset_cause())
doConnect()
waitForConnection()
setWebreplPassword()
webrepl.start()
