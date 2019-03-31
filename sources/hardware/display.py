import time
import utils
import lcd_i2c
import gc
import network
import utime
import machine

_PHASES = 2
_PHASE_REPEAT = 5
_UPDATE_INTERVAL_MS = 1000
_BACKLIGHT_RANGE_HOUR = (7, 22)

class Display():
    def __init__(self, i2c, temperatureSensor):
        (ip, _, _, _) = network.WLAN(network.STA_IF).ifconfig()
        addresses = i2c.scan()
        if (len(addresses) == 1):
            utils.printDebug("DISPLAY", 'found on %s address' % addresses[0])
            self.lcd = lcd_i2c.LcdI2C(i2c, addresses[0])
            self.lcd.write('Bolomajster', lcd_i2c.LCD_LINE_1)
            self.lcd.write(ip, lcd_i2c.LCD_LINE_2)
            self.count = 0
            self.temperatureSensor = temperatureSensor
            self.wlan = network.WLAN(network.STA_IF)
        else:
            utils.printDebug("DISPLAY", 'not found')
            self.lcd = None
        self._updateTimer = machine.Timer(-1)
        self._updateTimer.init(period=_UPDATE_INTERVAL_MS, mode=machine.Timer.PERIODIC, callback=lambda t: self.update())

    def __del__(self):
        utils.printLog('DISPLAY', 'delete')
        self._updateTimer.deinit()

    def setBacklight(self, enable):
        if self.lcd:
            self.lcd.setBacklight(enable)

    def getBacklight(self):
        if self.lcd:
            return self.lcd.getBacklight()

    def uptime(self):
        s = int(time.ticks_ms() / 1000)
        seconds = s % 60
        s = s // 60
        minutes = s % 60
        s = s // 60
        hours = s % 24
        s = s // 24
        days = s
        if days > 0:
            return '%02d:%02d:%02d' % (days, hours, minutes)
        else:
            return '%02d:%02d:%02d' % (hours, minutes, seconds)

    def free(self):
        gc.collect()
        return '%dkB' % (gc.mem_free() / 1024)

    def status(self):
        if self.wlan.isconnected():
            return "+"
        else:
            return "-"

    def time(self):
        tm = utime.localtime(utime.time())
        return '%02d:%02d:%02d' % (tm[3], tm[4], tm[5])

    def temperatures(self):
        return " ".join('%.1f' % t for t in self.temperatureSensor.getExternalTemperatures())

    def update(self):
        if not self.lcd:
            return
        hour = utime.localtime(utime.time())[3]
        self.setBacklight(_BACKLIGHT_RANGE_HOUR[0] <= hour and hour <= _BACKLIGHT_RANGE_HOUR[1])
        if self.count % _PHASE_REPEAT == 0 and _PHASES > 1:
            self.lcd.clear()
        phase = int(self.count / _PHASE_REPEAT)
        if phase == 0:
            self.lcd.write('%s %s %s' % (self.time(), self.free(), self.status()), lcd_i2c.LCD_LINE_1)
            self.lcd.write(self.temperatures(), lcd_i2c.LCD_LINE_2)
        elif phase == 1:
            self.lcd.write('%s %s %s' % (self.uptime(), self.free(), self.status()), lcd_i2c.LCD_LINE_1)
            self.lcd.write(self.temperatures(), lcd_i2c.LCD_LINE_2)
        self.count = (self.count + 1) % (_PHASE_REPEAT * _PHASES)
