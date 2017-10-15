from utils import printLog, printDebug
import ujson

class RstripServerController():
    def __init__(self):
        self.gpio = {}
        self.gpio['status'] = 0
        data = {}
        data['0'] = 0
        data['1'] = 1
        data['2'] = 1
        data['3'] = 0
        data['4'] = 1
        self.gpio['data'] = data

    def name(self):
        return 'remote control socket'

    def process(self, url, params):
        if url == '/GPIO/':
            return ujson.dumps(self.gpio)
        elif url == '/GPIO/SET/':
            try:
                self.gpio['data'][params['PIN']] = 1 if params['MODE'] == 'ON' else 0
            except:
                pass
            return ujson.dumps(self.gpio)
        return None
