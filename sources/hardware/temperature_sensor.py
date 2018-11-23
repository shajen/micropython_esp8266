import config
import ds18x20
import machine
import onewire
import utils

class TemperatureSensor:
    def __init__(self, pin):
        self.dallas = ds18x20.DS18X20(onewire.OneWire(pin))
        self.externalTemperatures = {}

    def getExternalTemperatures(self):
        return list(self.externalTemperatures.values())

    def getAverageExternalTemperature(self):
        if not self.externalTemperatures:
            return 0.0
        return sum(self.externalTemperatures.values())/len(self.externalTemperatures)

    def update(self):
        self.externalTemperatures = {}
        roms = self.dallas.scan()
        try:
            utils.printDebug("TEMP", "read %d dallas sensors success" % len(roms))
            if roms:
                self.dallas.convert_temp()
        except Exception as e:
            utils.printDebug("TEMP", "dallas exception %s" % e)
        for rom in roms:
            id = "".join("{:02x}".format(c) for c in rom)
            temperature = self.dallas.read_temp(rom)
            if temperature != 85.0:
                self.externalTemperatures[id] = temperature

    def upload(self):
        utils.printDebug("TEMP", "start upload")
        for (serial, temperature) in self.externalTemperatures.items():
            self.uploadTemperature(serial, temperature)
        utils.printDebug("TEMP", "finish upload")

    def uploadTemperature(self, serial, temperature):
        if temperature != 0.0:
            url = "http://monitor.shajen.pl/api/temp/add?serial=%s&temperature=%.2f&key=%s" % (serial, temperature, config.UPLOADER_KEY)
            utils.httpGet(url)
