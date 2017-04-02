from time import ticks_ms
import lcd_i2c
import gc
import network

DEFAULT_I2C_ADDR = 0x3f
PHASES = 2
PHASE_REPEAT = 10

class Display():
    def __init__(self, i2c, devices):
        (ip, _, _, _) = network.WLAN(network.STA_IF).ifconfig()
        self.lcd = lcd_i2c.LcdI2C(i2c, DEFAULT_I2C_ADDR)
        self.lcd.write('Bolomajster', lcd_i2c.LCD_LINE_1)
        self.lcd.write(ip, lcd_i2c.LCD_LINE_2)
        self.count = 0
        self.devices = devices

    def update(self):
        if self.count % PHASE_REPEAT == 0:
            self.lcd.clear()
        phase = int(self.count / PHASE_REPEAT)
        if phase == 0:
            uptime = int(ticks_ms() / 1000)
            gc.collect()
            free = gc.mem_free()
            self.lcd.write('Uptime: %d s' % uptime, lcd_i2c.LCD_LINE_1)
            self.lcd.write('Free: %d kB' % free, lcd_i2c.LCD_LINE_2)
        elif phase == 1:
            externalTemperature = " ".join('%.2f' % t for t in self.devices.getExternalTemperatures())
            self.lcd.write('I:%.2f A:%.2f ' % (self.devices.getInternalTemperature(), self.devices.getAverageExternalTemperature()), lcd_i2c.LCD_LINE_1)
            self.lcd.write(externalTemperature, lcd_i2c.LCD_LINE_2)
        self.count = (self.count + 1) % (PHASE_REPEAT * PHASES)
