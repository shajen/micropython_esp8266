import animation_utils
import math
import uos
import esp

class FullSmoothTransitionAnimation():
    def __init__(self, pin, leds):
        self.pin = pin
        self.leds = leds
        self.currentH = 0
        self.nextH = 0

    def tick(self):
        if self.currentH == self.nextH:
            self.nextH = math.floor(uos.urandom(1)[0] / 256 * 360)
        if self.currentH < self.nextH:
            self.currentH += 1
        else:
            self.currentH -= 1

        self.setLeds()

    def setLeds(self):
        (r, g, b) = animation_utils.hsvToRgb((self.currentH, 1.0, 1.0))
        esp.neopixel_write(self.pin, bytearray([r, g, b] * self.leds), 1)
