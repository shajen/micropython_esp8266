from time import ticks_ms
from utils import printDebug
import lcd_i2c
import gc
import network
import utime

PHASES = 2
PHASE_REPEAT = 5

class Display():
    def __init__(self, i2c, devices):
        (ip, _, _, _) = network.WLAN(network.STA_IF).ifconfig()
        addresses = i2c.scan()
        if (len(addresses) == 1):
            printDebug("DISPLAY", 'found on %s address' % addresses[0])
            self.lcd = lcd_i2c.LcdI2C(i2c, addresses[0])
            self.lcd.write('Bolomajster', lcd_i2c.LCD_LINE_1)
            self.lcd.write(ip, lcd_i2c.LCD_LINE_2)
            self.count = 0
            self.devices = devices
            self.wlan = network.WLAN(network.STA_IF)
        else:
            printDebug("DISPLAY", 'not found')
            self.lcd = None

    def setBacklight(self, enable):
        if self.lcd:
            self.lcd.setBacklight(enable)

    def getBacklight(self):
        if self.lcd:
            return self.lcd.getBacklight()

    def uptime(self):
        s = int(ticks_ms() / 1000)
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
        return " ".join('%.1f' % t for t in self.devices.getExternalTemperatures())

    def update(self):
        if not self.lcd:
            return
        if self.count % PHASE_REPEAT == 0 and PHASES > 1:
            self.lcd.clear()
        phase = int(self.count / PHASE_REPEAT)
        if phase == 0:
            self.lcd.write('%s %s %s' % (self.time(), self.free(), self.status()), lcd_i2c.LCD_LINE_1)
            self.lcd.write(self.temperatures(), lcd_i2c.LCD_LINE_2)
        elif phase == 1:
            self.lcd.write('%s %s %s' % (self.uptime(), self.free(), self.status()), lcd_i2c.LCD_LINE_1)
            self.lcd.write(self.temperatures(), lcd_i2c.LCD_LINE_2)
        self.count = (self.count + 1) % (PHASE_REPEAT * PHASES)
