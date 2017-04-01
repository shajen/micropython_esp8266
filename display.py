from time import ticks_ms
import lcd_i2c
import gc

DEFAULT_I2C_ADDR = 0x3f

class Display():
    def __init__(self, i2c):
        self.lcd = lcd_i2c.LcdI2C(i2c, DEFAULT_I2C_ADDR)

    def update(self, timer):
        uptime = int(ticks_ms() / 1000)
        gc.collect()
        free = gc.mem_free()
        self.lcd.write('Uptime: %d s' % uptime, lcd_i2c.LCD_LINE_1)
        self.lcd.write('Free: %d' % free, lcd_i2c.LCD_LINE_2)
