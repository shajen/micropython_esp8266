import utime as time

LCD_WIDTH = 16   # Maximum characters per line

LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

class LcdI2C():
    def __init__(self, i2c, address):
        self.i2c = i2c
        self.address = address
        self.backlight  = 0x08
        self.lcd_byte(0x33,LCD_CMD) # 110011 Initialise
        self.lcd_byte(0x32,LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01,LCD_CMD) # 000001 Clear display
        time.sleep(E_DELAY)

    def lcd_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | self.backlight
        bits_low = mode | ((bits<<4) & 0xF0) | self.backlight

        self.i2c.writeto(self.address, bytearray([bits_high]))
        self.lcd_toggle_enable(bits_high)

        self.i2c.writeto(self.address, bytearray([bits_low]))
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        time.sleep(E_DELAY)
        self.i2c.writeto(self.address, bytearray([(bits | ENABLE)]))
        time.sleep(E_PULSE)
        self.i2c.writeto(self.address, bytearray([(bits & ~ENABLE)]))
        time.sleep(E_DELAY)

    def setBacklight(self, enable):
        if enable:
            self.backlight  = 0x08
        else:
            self.backlight = 0x00
        self.lcd_byte(0x0C,LCD_CMD)

    def getBacklight(self):
        return self.backlight == 0x08

    def clear(self):
        self.lcd_byte(0x01,LCD_CMD)

    def write(self, message, line):
        self.lcd_byte(line, LCD_CMD)
        for c in message:
            self.lcd_byte(ord(c),LCD_CHR)
        for i in range(len(message), LCD_WIDTH):
            self.lcd_byte(ord(' '),LCD_CHR)
