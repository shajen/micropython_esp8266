import machine
import utils

class PinServerController():
    def __init__(self, mqttClient, pins):
        utils.printInfo('PIN', 'init')
        self._mqttClient = mqttClient
        self.pins = []
        for p in pins:
            self.pins.append(machine.Pin(p, machine.Pin.OUT))

    def getState(self):
        data = {}
        for i in range(len(self.pins)):
            data[str(i)] = self.pins[i].value()
        return data

    def processPin(self, pin, mode):
        if mode == 'switch':
            pin.value((pin.value() + 1) % 2)
        else:
            pin.value(1 if mode == 'on' else 0)

    def process(self, command, data):
        if command == '/gpio/state/':
            self._mqttClient.publishStatus('gpio/state', self.getState())
        elif command == '/gpio/set/':
            try:
                if 'pin' in data:
                    self.processPin(self.pins[data['pin']], data['mode'])
                else:
                    for pin in self.pins:
                        self.processPin(pin, data['mode'])
                self._mqttClient.publishEvent('gpio/state', 'New state has been set.')
                self._mqttClient.publishStatus('gpio/state', self.getState())
            except Exception as e:
                utils.printWarn('PIN', 'exception during process')
                utils.printWarn('PIN', e)
