import machine
import network
import utime
import webrepl
import os

def printLog(message):
    ms = utime.ticks_ms()
    seconds = ms / 1000
    ms = ms % 1000
    print("[% 3d.%03d] %s" % (seconds, ms, message))

def detectSoftReboot():
    if utime.ticks_ms() >= 1000:
        machine.reset()

def preBoot():
    try:
        import pre_boot
    except Exception as e:
        printLog('exception in pre_boot')
        printLog(e)

def tryConnect(timeoutMs):
    printLog('start tryConnect')
    startTimeMs = utime.ticks_ms()
    connected = False
    while (startTimeMs + timeoutMs >= utime.ticks_ms() and not connected):
        try:
            try:
                from config import NETWORKS
            except:
                printLog('exception during import NETWORKS')
                NETWORKS = {}
            network.WLAN(network.AP_IF).active(False)
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            nets = wlan.scan()
            for net in nets:
                ssid = net[0].decode()
                if ssid in NETWORKS:
                    printLog('Try to connect to %s' % ssid)
                    wlan.connect(ssid, NETWORKS[ssid])
                    connected = True
        except Exception as e:
            printLog('exception during connecting')
            printLog(e)
            machine.reset()
    printLog('finish tryConnect')

def waitForConnection(timeoutMs):
    printLog('start waitForConnection')
    startTimeMs = utime.ticks_ms()
    wlan = network.WLAN(network.STA_IF)
    while (startTimeMs + timeoutMs >= utime.ticks_ms() and not wlan.isconnected()):
        utime.sleep_ms(100)
    if wlan.isconnected():
        printLog('wlan connection succeeded')
    printLog('finish waitForConnection')

printLog('shajen development - micropython')
printLog('reset cause %d' % machine.reset_cause())
detectSoftReboot()
preBoot()
tryConnect(10000)
waitForConnection(10000)
webrepl.start()
