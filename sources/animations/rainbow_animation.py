import array
import base_animation

class RainbowAnimation():
    def __init__(self, np):
        self.np = np
        self.ledsCount = np.n
        self.colors = []
        for i in range(0, self.ledsCount):
            h = i * (360 / self.ledsCount)
            color = base_animation.hsvToRgb((h, 1.0, 1.0))
            self.colors.append(color[1])
            self.colors.append(color[0])
            self.colors.append(color[2])

    def tick(self):
        self.colors.append(self.colors.pop(0))
        self.colors.append(self.colors.pop(0))
        self.colors.append(self.colors.pop(0))
        self.setLeds()

    def setLeds(self):
        tmp = array.array('B', self.colors)
        self.np.buf = bytearray(tmp)
        self.np.write()
