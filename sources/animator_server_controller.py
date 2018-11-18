import neopixel
import machine
import config
import utils
import uos

class AnimatorServerController():
    def __init__(self):
        self.ledsCount = 60
        self.np = neopixel.NeoPixel(machine.Pin(config.WS2811_PIN), self.ledsCount)
        self.lastLed = 1
        self.direction = 0
        self.colour = (0, 0, 0)
        self.ledsPerStep = 10
        self.rMapTable = self.getColorsMapTable()
        self.gMapTable = self.getColorsMapTable()
        self.bMapTable = self.getColorsMapTable()

    def name(self):
        return 'animator'

    def tick(self):
        if self.lastLed == (self.ledsCount - self.ledsPerStep) or self.lastLed == 0:
            self.direction = (self.direction + 1) % 2
            self.refreshColor()

        if self.direction == 0:
            self.lastLed = self.lastLed + 1
        else:
            self.lastLed = self.lastLed - 1

        self.setLeds(self.lastLed, self.lastLed + self.ledsPerStep)

    def getColorsMapTable(self):
        utils.printDebug("LED", "start generating colors map table")
        tmp = list(range(0, 256))
        result = []
        for i in range(0, 256):
            index = uos.urandom(1)[0] % len(tmp)
            result.append(tmp[index])
            tmp.pop(index)
        utils.printDebug("LED", "finish generating colors map table")
        return result

    def refreshColor(self):
        self.colour = (self.rMapTable[uos.urandom(1)[0]], self.gMapTable[uos.urandom(1)[0]], self.bMapTable[uos.urandom(1)[0]])

    def setLeds(self, _from, _to):
        for i in range(0, self.ledsCount):
            if _from <= i and i < _to:
                self.np[i] = self.colour
            else:
                self.np[i] = (0, 0,0 )
        self.np.write()

    def process(self, url, params):
        return None
