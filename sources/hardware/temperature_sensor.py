import config
import ds18x20
import machine
import onewire
import utils

_UPDATE_INTERVAL_MS = 1000
_UPLOAD_INTERVAL_MS = 60000

class TemperatureSensor:
    def __init__(self, pin):
        utils.printInfo('TEMPERATURE', 'init')
        self.dallas = ds18x20.DS18X20(onewire.OneWire(pin))
        self.externalTemperatures = {}
        self._updateTimer = utils.timer()
        self._uploadTimer = utils.timer()
        self.update()
        self._updateTimer.init(period=_UPDATE_INTERVAL_MS, mode=machine.Timer.PERIODIC, callback=lambda t: self.update())
        self._uploadTimer.init(period=_UPLOAD_INTERVAL_MS, mode=machine.Timer.PERIODIC, callback=lambda t: self.upload())

    def getExternalTemperatures(self):
        return list(self.externalTemperatures.values())

    def getExternalTemperaturesWithId(self):
        return list(self.externalTemperatures.items())

    def getAverageExternalTemperature(self):
        if not self.externalTemperatures:
            raise Exception('temperature sensors not found')
        return sum(self.externalTemperatures.values())/len(self.externalTemperatures)

    def update(self):
        self.externalTemperatures = {}
        roms = self.dallas.scan()
        try:
            utils.printDebug("TEMPERATURE", "read %d dallas sensors success" % len(roms))
            if roms:
                self.dallas.convert_temp()
        except Exception as e:
            utils.printWarn("TEMPERATURE", "dallas exception %s" % e)
        for rom in roms:
            id = "".join("{:02x}".format(c) for c in rom)
            temperature = self.dallas.read_temp(rom)
            utils.printDebug("TEMPERATURE", "%s = %.2f" % (id, temperature))
            if temperature != 85.0:
                self.externalTemperatures[id] = temperature

    def upload(self):
        utils.printDebug("TEMPERATURE", "start upload")
        for (serial, temperature) in self.externalTemperatures.items():
            self.uploadTemperature(serial, temperature)
        utils.printDebug("TEMPERATURE", "finish upload")

    def uploadTemperature(self, serial, temperature):
        if temperature != 0.0:
            url = "http://monitor.shajen.pl/api/temp/add?serial=%s&temperature=%.2f&key=%s" % (serial, temperature, config.UPLOADER_KEY)
            utils.httpGet(url)
