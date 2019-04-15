import utils
import lcd_i2c

_PHASE_REPEAT = 5

class SegmentalDisplay():
    def __init__(self, i2c, addresses, width, height):
        utils.printInfo('SEGMENTAL', 'init display on 0x%02X address' % addresses)
        utils.printInfo('SEGMENTAL', 'size %02dx%02d' %(width, height))
        self._width = width
        self._height = height
        self._lcd = lcd_i2c.LcdI2C(i2c, addresses)
        self._initialMessage = 'Hello World!'
        self._ip = '0.0.0.0'
        self._uptime = (0, 0, 0, 0)
        self._time = (0, 0, 0, 0, 0, 0)
        self._freeMemory = 0
        self._wifiIsConnected = False
        self._temperatures = []
        self._phase = 0
        self._lastLine = 0

    def setInitialMessage(self, initialMessage):
        self._initialMessage = initialMessage

    def setIp(self, ip):
        self._ip = ip

    def showInitialMessage(self):
        self._lcd.write(self._initialMessage, lcd_i2c.LCD_LINE_1)
        self._lcd.write(self._ip, lcd_i2c.LCD_LINE_2)

    def setBacklight(self, enable):
        self._lcd.setBacklight(enable)

    def setUptime(self, uptime):
        self._uptime = uptime

    def setTime(self, _time):
        self._time = _time

    def setFreeMemory(self, freeMemory):
        self._freeMemory = freeMemory

    def setWifiStatus(self, isConnected):
        self._wifiIsConnected = isConnected

    def setTemperatures(self, temperatures):
        self._temperatures = temperatures

    def update(self):
        (years, months, days, hours, minutes, seconds) = self._time
        lines = []
        lines.append(' '.join('%.1f' % t for t in self._temperatures))
        lines.append('free %d, WiFi %i' % (self._freeMemory, self._wifiIsConnected))
        lines.append('time %02d:%02d:%02d' % (hours, minutes, seconds))
        lines.append('up %02d:%02d:%02d:%02d' % self._uptime)

        self._phase = (self._phase + 1) % _PHASE_REPEAT
        if self._phase == 0:
            if len(lines) != self._height:
                self._lcd.clear()
            self._lastLine = (self._lastLine + self._height) % len(lines)

        for i in range(0, self._height):
            sourceLine = (self._lastLine + i) % len(lines)
            self._lcd.write(lines[sourceLine], lcd_i2c.LCD_LINES[i])
