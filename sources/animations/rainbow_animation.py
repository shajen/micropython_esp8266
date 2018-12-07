import animation_utils
import esp

class RainbowAnimation():
    def __init__(self, pin, leds):
        self.pin = pin
        self.leds = leds
        self.colors = []
        for i in range(0, leds):
            h = i * (360 / leds)
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
        esp.neopixel_write(self.pin, bytearray(self.colors), 1)
