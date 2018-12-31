import machine
import ujson
import utime

class SonoffServerController():
    def __init__(self, switches):
        self.switches = switches

        for switch in self.switches:
            (r, l, s) = switch
            r.value(0)
            if l:
                l.value(1)
            s.irq(trigger=machine.Pin.IRQ_RISING, handler=lambda p, switch=switch:self.switchClicked(switch))

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
        return ujson.dumps({'data' : data})

    def process(self, url, params):
        if url == '/GPIO/':
            return self.getState()
        elif url == '/GPIO/SET/':
            try:
                switch = self.switches[int(params['PIN'])]
                (r, l, s) = switch
                value = 1 if params['MODE'] == 'ON' else 0
                r.value(value)
                if l:
                    l.value((value + 1) % 2)
            except:
                pass
            return self.getState()
        return None

__INSTANCE__ = None

def initInstance(switches):
    global __INSTANCE__
    if not __INSTANCE__:
        __INSTANCE__ = SonoffServerController(switches)

def getInstance():
    global __INSTANCE__
    return __INSTANCE__
