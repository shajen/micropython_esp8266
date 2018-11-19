import base_animation
import math
import uos

class FullSmoothTransitionAnimation():
    def __init__(self, np):
        self.np = np
        self.ledsCount = np.n
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
        color = base_animation.hsvToRgb((self.currentH, 1.0, 1.0))
        for i in range(0, self.ledsCount):
            self.np[i] = color
        self.np.write()
