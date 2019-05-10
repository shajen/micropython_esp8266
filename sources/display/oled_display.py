import utils
import ssd1306

class OledDisplay():
    def __init__(self, i2c, address, width, height):
        utils.printInfo('OLED', 'init display on 0x%02X address' % address)
        utils.printInfo('OLED', 'size %dx%d' % (width, height))
        self._oled = ssd1306.SSD1306_I2C(width, height, i2c, address)
        self._initialMessage = 'Hello World!'
        self._ip = '0.0.0.0'
        self._uptime = (0, 0, 0, 0)
        self._time = (0, 0, 0, 0, 0, 0)
        self._freeMemory = 0
        self._wifiIsConnected = False
        self._temperatures = []

    def setInitialMessage(self, initialMessage):
        self._initialMessage = initialMessage

    def setIp(self, ip):
        self._ip = ip

    def showInitialMessage(self):
        self._oled.text(self._initialMessage, 0, 0)
        self._oled.text(self._ip, 0, 10)
        self._oled.show()
        
    def setBacklight(self, enable):
        if enable:
            self._oled.poweron()
        else:
            self._oled.poweroff()

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
        if len(self._temperatures) >= 4:
            lines.append(' '.join('%.0f' % t for t in self._temperatures))
        elif len(self._temperatures) >= 3:
            lines.append(' '.join('%.1f' % t for t in self._temperatures))
        else:
            lines.append(' '.join('%.2f' % t for t in self._temperatures))
        lines.append('time %02d:%02d:%02d' % (hours, minutes, seconds))
        lines.append('free %d, WiFi %i' % (self._freeMemory, self._wifiIsConnected))
        lines.append('up %02d:%02d:%02d:%02d' % self._uptime)

        self._oled.fill(0)
        for i in range(len(lines)):
            self._oled.text(lines[i], 0, i * 10)
        self._oled.show()
