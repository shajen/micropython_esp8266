import machine
import network
import ujson
import utils

class SonoffServerController():
    def __init__(self, switches, statusPin):
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

    def name(self):
        return 'sonoff'

    def switchClicked(self, switch):
        (r, l, s) = switch
        r.value((r.value() + 1) % 2)
        if l:
            l.value((l.value() + 1) % 2)

    def getState(self):
        data = {}
        for i in range(len(self.switches)):
            (r, l, s) = self.switches[i]
            data[str(i)] = r.value()
        return ujson.dumps({'status': 0, 'data' : data})

    def processSwitch(self, switch, mode):
        (r, l, s) = switch
        if mode == 'SWITCH':
            r.value((r.value() + 1) % 2)
        else:
            r.value(1 if mode == 'ON' else 0)
        if l:
            l.value((value + 1) % 2)

    def process(self, url, params):
        if url == '/GPIO/':
            return self.getState()
        elif url == '/GPIO/SET/':
            try:
                if 'PIN' in params:
                    self.processSwitch(self.switches[int(params['PIN'])], params['MODE'])
                else:
                    for switch in self.switches:
                        self.processSwitch(switch, params['MODE'])
            except:
                pass
            return self.getState()
        return None
