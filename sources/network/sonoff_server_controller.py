import machine
import ujson
import utime

class SonoffServerController():
    def __init__(self, relayPin, ledPin, switchPin):
        self.relayPin = relayPin
        self.ledPin = ledPin
        self.switchPin = switchPin

        self.ledPin.value(1)
        for i in range(1, 11):
            self.ledPin.value((self.ledPin.value() + 1) % 2)
            utime.sleep_ms(100)

        self.relayPin.value(0)
        self.ledPin.value(1)

        switchPin.irq(trigger=machine.Pin.IRQ_RISING, handler=lambda p:self.switchClicked())

    def name(self):
        return 'sonoff'

    def switchClicked(self):
        self.relayPin.value((self.relayPin.value() + 1) % 2)
        self.ledPin.value((self.ledPin.value() + 1) % 2)

    def getState(self):
        data = {
            "1" : self.relayPin.value()
        }
        return ujson.dumps({'data' : data})

    def process(self, url, params):
        if url == '/GPIO/':
            return self.getState()
        elif url == '/GPIO/SET/':
            try:
                if params['PIN'] == '1':
                    value = 1 if params['MODE'] == 'ON' else 0
                    self.relayPin.value(value)
                    self.ledPin.value((value + 1) % 2)
            except:
                pass
            return self.getState()
        return None
