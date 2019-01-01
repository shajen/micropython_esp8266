import machine
import ujson

class PinServerController():
    def __init__(self, pins):
        self.pins = []
        for p in pins:
            self.pins.append(machine.Pin(p, machine.Pin.OUT))

    def name(self):
        return 'remote control socket'

    def getState(self):
        data = {}
        for i in range(len(self.pins)):
            data[str(i)] = self.pins[i].value()
        return ujson.dumps({'status': 0, 'data' : data})

    def processPin(self, pin, mode):
        if mode == 'SWITCH':
            pin.value((pin.value() + 1) % 2)
        else:
            pin.value(1 if mode == 'ON' else 0)
        if l:
            l.value((value + 1) % 2)

    def process(self, url, params):
        if url == '/GPIO/':
            return self.getState()
        elif url == '/GPIO/SET/':
            try:
                if 'PIN' in params:
                    self.processPin(self.pins[int(params['PIN'])], params['MODE'])
                else:
                    for pin in self.pins:
                        self.processPin(pin, params['MODE'])
            except:
                pass
            return self.getState()
        return None
