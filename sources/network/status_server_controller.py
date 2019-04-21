import esp
import gc
import machine
import network
import sys
import ubinascii
import usocket
import utils
import utime

class StatusServerController():
    def __init__(self, mqttClient, deviceType):
        utils.printInfo('STATUS', 'init')
        self._mqttClient = mqttClient
        self.wlan = network.WLAN()
        self.adc = machine.ADC(1)
        self.deviceType = deviceType

    def process(self, command, data):
        if command == '/status/':
            data = {}
            gc.collect()
            data['nodemcu'] = {}
            data['nodemcu']['mem_free'] = gc.mem_free()
            data['nodemcu']['flash_id'] = esp.flash_id()
            data['nodemcu']['chip_id'] = utils.chipId()
            data['nodemcu']['bootreason'] = machine.reset_cause()
            data['nodemcu']['voltage'] = self.adc.read() / 1000.0
            data['python'] = {}
            data['python']['implementation'] = self.implementation()
            data['python']['version'] = sys.version
            data['datetime'] = {}
            data['datetime']['formatted'] = self.datetime()
            data['datetime']['seconds'] = utime.time()
            data['uptime'] = {}
            data['uptime']['formatted'] = self.uptime()
            data['uptime']['seconds'] = int(utime.ticks_ms() / 1000)
            (ssid, hostname, rssi) = self.ssidAndRssi()
            data['network'] = {}
            data['network']['local'] = {}
            data['network']['local']['mac'] = ubinascii.hexlify(self.wlan.config('mac'),':').decode()
            data['network']['local']['ip'] = self.wlan.ifconfig()[0]
            data['network']['local']['hostname'] = hostname
            data['network']['wifi'] = {}
            data['network']['wifi']['ssid'] = ssid
            data['network']['wifi']['rssi'] = rssi
            data['device_type'] = self.deviceType
            self._mqttClient.publishDevice('status', data)
        elif command == '/reset/':
            utils.timer().init(period=3000, mode=machine.Timer.PERIODIC, callback=lambda t: machine.reset())
            self._mqttClient.publishEvent('reset', 'Board will be restarted in a 3 seconds.')

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
