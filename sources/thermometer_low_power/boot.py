import machine
import network
import utime
import webrepl
import os
import utime

def detectSoftReboot():
    if utime.ticks_ms() >= 1000:
        machine.reset()

def doConnect(seconds=10):
    try:
        print('Scanning networks...')
        NETWORKS = {"SSID_1": "PASSWORD_1", "SSID_2": "PASSWORD_2"}
        network.WLAN(network.AP_IF).active(False)
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        startTime = utime.ticks_ms()
        while utime.ticks_ms() < startTime + seconds * 1000:
            nets = wlan.scan()
            for net in nets:
                ssid = net[0].decode()
                if ssid in NETWORKS:
                    print('Try to connect to %s' % ssid)
                    wlan.connect(ssid, NETWORKS[ssid])
                    return
            utime.sleep_ms(10)
    except:
        print('Exception during scan!')
        machine.reset()
    print('Can not find any suitable network')

def waitForConnection(seconds=20):
    print('Waiting for connes
    ction...')
    wlan = network.WLAN(network.STA_IF)
    startTime = utime.ticks_ms()
    while utime.ticks_ms() < startTime + seconds * 1000 and not wlan.isconnected():
        utime.sleep_ms(10)
    if wlan.isconnected():
        print('WLAN connection succeeded!')
    else:
        print('WLAN connection error!')

def setWebreplPassword():
    if "webrepl_cfg.py" not in os.listdir():
        print('webrepl set password')
        f = open("webrepl_cfg.py", 'w')
        f.write("PASS = 'PASSWORD'\n")
        f.close()

detectSoftReboot()
print('Shajen development - micropython')
print('Reset cause %d' % machine.reset_cause())
doConnect()
waitForConnection()
setWebreplPassword()
webrepl.start()
