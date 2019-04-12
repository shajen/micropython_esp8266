import gc
import machine
import network
import segmental_display
import time
import utils
import utime

_UPDATE_INTERVAL_MS = 1000

class Display():
    def __init__(self, i2c, temperatureSensor, initialMessage):
        utils.printLog('DISPLAY', 'init')
        self._displays = []
        self._wlan = network.WLAN(network.STA_IF)
        self._temperatureSensor = temperatureSensor

        for address in i2c.scan():
            self._displays.append(segmental_display.SegmentalDisplay(i2c, address, 20, 4))

        (ip, _, _, _) = network.WLAN(network.STA_IF).ifconfig()
        for display in self._displays:
            display.setInitialMessage(initialMessage)
            display.setIp(ip)
            display.showInitialMessage()

        self._updateTimer = machine.Timer(-1)
        self._updateTimer.init(period=_UPDATE_INTERVAL_MS, mode=machine.Timer.PERIODIC, callback=lambda t: self.update())

    def __del__(self):
        utils.printLog('DISPLAY', 'delete')
        self._updateTimer.deinit()
        for display in self._displays:
            display.__del__()

    def _uptime(self):
        s = int(time.ticks_ms() / 1000)
        seconds = s % 60
        s = s // 60
        minutes = s % 60
        s = s // 60
        hours = s % 24
        s = s // 24
        days = s
        return (days, hours, minutes, seconds)

    def _time(self):
        tm = utime.localtime(utime.time())
        return (tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])

    def update(self):
        uptime = self._uptime()
        datetime = self._time()
        gc.collect()
        freeMemory = gc.mem_free()
        wifiIsConnected = self._wlan.isconnected()
        temperatures = self._temperatureSensor.getExternalTemperatures()

        for display in self._displays:
            display.setUptime(uptime)
            display.setTime(datetime)
            display.setFreeMemory(freeMemory)
            display.setWifiStatus(wifiIsConnected)
            display.setTemperatures(temperatures)
            display.update()
