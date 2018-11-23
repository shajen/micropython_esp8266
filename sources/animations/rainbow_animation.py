import animation_utils

class RainbowAnimation():
    def __init__(self, np):
        self.np = np
        self.colors = []
        for i in range(0, self.np.n):
            h = i * (360 / self.np.n)
            color = animation_utils.hsvToRgb((h, 1.0, 1.0))
            self.colors.append(color[1])
            self.colors.append(color[0])
            self.colors.append(color[2])

    def tick(self):
        self.colors.append(self.colors.pop(0))
        self.colors.append(self.colors.pop(0))
        self.colors.append(self.colors.pop(0))
        self.setLeds()

    def setLeds(self):
        self.np.buf = bytearray(self.colors)
        self.np.write()
