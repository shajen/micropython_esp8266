from config import NETWORKS
from utils import printLog, printDebug, chipId
import esp
import gc
import machine
import network
import sys
import ubinascii
import ujson
import usocket
import utime

class StatusServerController():
    def __init__(self, controllers):
        self.wlan = network.WLAN()
        self.controllers = controllers

    def name(self):
        return 'status'

    def process(self, url, params):
        if url == '/':
            data = {}
            gc.collect()
            data['nodemcu'] = {}
            data['nodemcu']['mem_free'] = gc.mem_free()
            data['nodemcu']['flash_id'] = esp.flash_id()
            data['nodemcu']['chip_id'] = chipId()
            data['nodemcu']['bootreason'] = machine.reset_cause()
            data['python'] = {}
            data['python']['implementation'] = self.implementation()
            data['python']['version'] = sys.version
            data['datetime'] = {}
            data['datetime']['formatted'] = self.datetime()
            data['datetime']['seconds'] = utime.time()
            data['uptime'] = {}
            data['uptime']['formatted'] = self.uptime()
            data['uptime']['seconds'] = int(utime.ticks_ms() / 1000)
            data['network'] = {}
            data['network']['local'] = {}
            data['network']['local']['mac'] = ubinascii.hexlify(self.wlan.config('mac'),':').decode()
            data['network']['local']['ip'] = self.wlan.ifconfig()[0]
            (ssid, mac, rssi) = self.ssidAndRssi()
            data['network']['wifi'] = {}
            data['network']['wifi']['ssid'] = ssid
            data['network']['wifi']['mac'] = mac
            data['network']['wifi']['rssi'] = rssi
            data['controllers'] = [c.name() for c in self.controllers] + [self.name()]
            return ujson.dumps(data)
        elif url == '/REBOOT/':
            machine.reset()

    def ssidAndRssi(self):
        wlan = network.WLAN(network.STA_IF)
        return (wlan.config('essid'), wlan.config('dhcp_hostname'), wlan.status('rssi'))

    def datetime(self):
        year, month, day, _, hour, minute, second, ms = machine.RTC().datetime()
        return '%d-%02d-%02d %02d:%02d:%02d:%03d' % (year, month, day, hour, minute, second, ms)

    def uptime(self):
        s = utime.ticks_ms() / 1000
        seconds = s % 60
        s = s / 60
        minutes = s % 60
        s = s / 60
        hours = s % 24
        s = s / 24
        days = s
        return '%02d:%02d:%02d:%02d' % (days, hours, minutes, seconds)

    def implementation(self):
        v = sys.implementation
        return '%s %s.%s.%s' % (v[0], v[1][0], v[1][1], v[1][2])
