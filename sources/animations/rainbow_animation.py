import base_animation
import math
import uos

class RainbowAnimation():
    def __init__(self, np):
        self.np = np
        self.ledsCount = np.n
        self.colors = []
        for i in range(0, self.ledsCount):
            h = i * (360 / self.ledsCount)
            color = base_animation.hsvToRgb((h, 1.0, 1.0))
            self.colors.append(color)

    def tick(self):
        tmp = self.colors.pop()
        self.colors.insert(0, tmp)
        self.setLeds()

    def setLeds(self):
        tmp = []
        for i in range(0, self.ledsCount):
            #self.np[i] = self.colors[i]
            tmp.append(self.colors[i][0])
            tmp.append(self.colors[i][1])
            tmp.append(self.colors[i][2])
        self.np.buf = bytearray(tmp)
        self.np.write()
