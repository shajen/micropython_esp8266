import machine
import network
import utils

class SonoffServerController():
    def __init__(self, mqttClient, switches, statusPin):
        utils.printInfo('SONOFF', 'init')
        self._mqttClient = mqttClient
        self.switches = switches
        self.statusPin = statusPin

        for switch in self.switches:
            (r, l, s) = switch
            r.value(0)
            if l:
                l.value(1)
            s.irq(trigger=machine.Pin.IRQ_FALLING, handler=lambda p, switch=switch:self.switchClicked(switch))

        self.timer = utils.timer()
        self.timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=lambda t: self.update())

    def update(self):
        isconnected = network.WLAN(network.STA_IF).isconnected()
        self.statusPin.value(1 if not isconnected else 0)

    def switchClicked(self, switch):
        utils.printInfo('SONOFF', 'switch pressed')
        self._mqttClient.publishEvent('gpio/switch', 'The switch has been pressed.')
        (r, l, s) = switch
        r.value((r.value() + 1) % 2)
        if l:
            l.value((l.value() + 1) % 2)

    def getState(self):
        data = {}
        for i in range(len(self.switches)):
            (r, l, s) = self.switches[i]
            data[str(i)] = r.value()
        return data

    def processSwitch(self, switch, mode):
        (r, l, s) = switch
        if mode == 'switch':
            r.value((r.value() + 1) % 2)
        else:
            r.value(1 if mode == 'on' else 0)
        if l:
            l.value((value + 1) % 2)

    def process(self, command, data):
        if command == '/gpio/status/':
            self._mqttClient.publishDevice('gpio/status', self.getState())
        elif command == '/gpio/set/':
            try:
                if 'pin' in data:
                    self.processSwitch(self.switches[data['pin']], data['mode'])
                else:
                    for switch in self.switches:
                        self.processSwitch(switch, data['mode'])
                self._mqttClient.publishEvent('gpio/state', 'New state has been set.')
                self._mqttClient.publishDevice('gpio/status', self.getState())
            except Exception as e:
                utils.printWarn('SONOFF', 'exception during process')
                utils.printWarn('SONOFF', e)
