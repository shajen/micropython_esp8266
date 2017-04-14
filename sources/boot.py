import machine
import network
import utime
import webrepl

def detectSoftReboot():
    if utime.ticks_ms() >= 1000:
        machine.reset()

def doConnect():
    NETWORKS = {"SSID_1": "PASSWORD_1", "SSID_2": "PASSWORD_2"}
    network.WLAN(network.AP_IF).active(False)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while not wlan.isconnected():
        nets = wlan.scan()
        for net in nets:
            ssid = net[0].decode()
            if ssid in NETWORKS:
                print('Try to connect to %s' % ssid)
                wlan.connect(ssid, NETWORKS[ssid])
        while not wlan.isconnected():
            machine.idle()
    print('WLAN connection succeeded!')

detectSoftReboot()
print('Bolomajster - micropython')
print('Reset cause %d' % machine.reset_cause())
utime.sleep(3)
doConnect()
webrepl.start()
