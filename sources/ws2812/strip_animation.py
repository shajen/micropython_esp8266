import animation_utils
import esp
import math
import uos

class StripAnimation():
    def __init__(self, pin, leds):
        self.pin = pin
        self.setup(leds)

    def setup(self, leds):
        self.ledsPerStep = 10
        self.leds = max(leds, self.ledsPerStep + 1)
        self.lastLed = 1
        self.direction = 0
        self.currentH = 0
        self.nextH = 0

    def tick(self):
        if self.lastLed == (self.leds - self.ledsPerStep) or self.lastLed == 0:
            self.direction = (self.direction + 1) % 2

        if self.currentH == self.nextH:
            self.nextH = math.floor(uos.urandom(1)[0] / 256 * 360)
        if self.currentH < self.nextH:
            self.currentH += 1
        else:
            self.currentH -= 1

        if self.direction == 0:
            self.lastLed += 1
        else:
            self.lastLed -= 1

        self.setLeds(self.lastLed, self.lastLed + self.ledsPerStep)

    def setLeds(self, _from, _to):
        (r, g, b) = animation_utils.hsvToRgb((self.currentH, 1.0, 1.0))
        tmp = [0, 0, 0] * _from + [r, g , b] * (_to - _from + 1) + [0, 0, 0] * (self.leds - _to)
        esp.neopixel_write(self.pin, bytearray(tmp), 1)
