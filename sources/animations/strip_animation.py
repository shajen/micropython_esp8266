import base_animation
import math
import uos

class StripAnimation():
    def __init__(self, np):
        self.np = np
        self.ledsCount = np.n
        self.lastLed = 1
        self.direction = 0
        self.ledsPerStep = 10
        self.currentH = 0
        self.nextH = 0

    def tick(self):
        if self.lastLed == (self.ledsCount - self.ledsPerStep) or self.lastLed == 0:
            self.direction = (self.direction + 1) % 2

        if self.currentH == self.nextH:
            self.nextH = math.floor(uos.urandom(1)[0] / 256 * 360)
        if self.currentH < self.nextH:
            self.currentH += 1
        else:
            self.currentH -= 1

        if self.direction == 0:
            self.lastLed = self.lastLed + 1
        else:
            self.lastLed = self.lastLed - 1

        self.setLeds(self.lastLed, self.lastLed + self.ledsPerStep)

    def setLeds(self, _from, _to):
        color = base_animation.hsvToRgb((self.currentH, 1.0, 1.0))
        for i in range(max(0, _from - 1), min(self.ledsCount, _to + 1)):
            if _from <= i and i < _to:
                self.np[i] = color
            else:
                self.np[i] = (0, 0, 0)
        self.np.write()
