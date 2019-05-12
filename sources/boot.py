import machine
import network
import utime
import webrepl
import os

def printInfo(message):
    ms = utime.ticks_ms()
    seconds = ms / 1000
    ms = ms % 1000
    print("[% 5d.%03d] [%13s] %s" % (seconds, ms, 'BOOT', message))

def detectSoftReboot():
    if utime.ticks_ms() >= 1000:
        machine.reset()

def detectReset():
    printInfo('reset cause %d' % machine.reset_cause())
    rtc = machine.RTC()
    printInfo('RTC memory: %s' % rtc.memory().decode('utf-8'))
    if machine.reset_cause() == 6:
        try:
            resets_count = int(rtc.memory().decode('utf-8'))
        except:
            resets_count = 0
        resets_count = resets_count + 1
        rtc.memory(str(resets_count))
    else:
        rtc.memory(str(0))

def preBoot():
    try:
        import pre_boot
    except Exception as e:
        printInfo('exception in pre_boot')
        printInfo(e)

def tryConnect(timeoutMs):
    printInfo('start tryConnect')
    startTimeMs = utime.ticks_ms()
    connected = False
    while (startTimeMs + timeoutMs >= utime.ticks_ms() and not connected):
        try:
            try:
                from config import NETWORKS
            except:
                printInfo('exception during import NETWORKS')
                NETWORKS = {}
            network.WLAN(network.AP_IF).active(False)
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            nets = wlan.scan()
            for net in nets:
                ssid = net[0].decode()
                if ssid in NETWORKS:
                    printInfo('Try to connect to %s' % ssid)
                    wlan.connect(ssid, NETWORKS[ssid])
                    connected = True
        except Exception as e:
            printInfo('exception during connecting')
            printInfo(e)
            machine.reset()
    printInfo('finish tryConnect')

def waitForConnection(timeoutMs):
    printInfo('start waitForConnection')
    startTimeMs = utime.ticks_ms()
    wlan = network.WLAN(network.STA_IF)
    while (startTimeMs + timeoutMs >= utime.ticks_ms() and not wlan.isconnected()):
        utime.sleep_ms(100)
    if wlan.isconnected():
        printInfo('wlan connection succeeded')
    printInfo('finish waitForConnection')

def isConnected():
    return network.WLAN(network.STA_IF).isconnected()

print()
printInfo('shajen development - micropython')
detectSoftReboot()
detectReset()
preBoot()
waitForConnection(10000)
if not isConnected():
    tryConnect(10000)
    waitForConnection(10000)
webrepl.start()
