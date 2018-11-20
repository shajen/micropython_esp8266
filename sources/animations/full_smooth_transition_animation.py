import base_animation
import math
import uos

class FullSmoothTransitionAnimation():
    def __init__(self, np):
        self.np = np
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
        (r, g, b) = base_animation.hsvToRgb((self.currentH, 1.0, 1.0))
        self.np.buf = bytearray([r, g, b] * self.np.n)
        self.np.write()
