from time import ticks_ms
import lcd_i2c
import gc

DEFAULT_I2C_ADDR = 0x27

class Display():
    def __init__(self, i2c):
        self.lcd = lcd_i2c.LcdI2C(i2c, DEFAULT_I2C_ADDR)

    def update(self, timer):
        gc.collect()
        self.lcd.write('Uptime: %d s' % int(ticks_ms() / 1000), lcd_i2c.LCD_LINE_1)
        self.lcd.write('Free: %d' % gc.mem_free(), lcd_i2c.LCD_LINE_2)
