
class Brew:
    def __init__(self, devices):
        self.devices = devices
        self.activeMode = 'CLOSE'
        self.temperature = 0.0
        self.started = False
        self.breaks = []

    def setMode(self, mode):
        self.activeMode = mode
        return True

    def getMode(self):
        return self.activeMode

    def setTemperature(self, temperature):
        if not self.started:
            self.temperature = temperature

    def getTemperature(self):
        return self.temperature

    def setBreaks(self, breaks):
        if not self.started:
            self.breaks = []
            print(breaks)
            print(len(breaks))
            for v in breaks:
                b = {}
                b['STATE'] = 'STOP'
                b['TIME'] = v['TIME']
                b['TEMP'] = v['TEMP']
                print(b)
                self.breaks.append(b)

    def getBreaks(self):
        return self.breaks

    def start(self):
        self.started = True

    def stop(self):
        self.started = False

    def isStarted(self):
        return self.started
