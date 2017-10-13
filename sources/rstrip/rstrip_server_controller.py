from utils import printLog, printDebug
import ujson

class RstripServerController():
    def __init__(self):
        self.gpio = {}
        self.gpio['status'] = 0
        data = {}
        data['0'] = 0
        data['1'] = 0
        data['2'] = 1
        data['3'] = 1
        data['4'] = 1
        self.gpio['data'] = data

    def process(self, url, params):
        if url == '/GPIO/':
            return ujson.dumps(self.gpio)
        elif url == '/GPIO/SET/':
            try:
                self.gpio['data'][params['PIN']] = 1 if params['MODE'] == 'ON' else 0
            except:
                pass
            return ujson.dumps(self.gpio)
        return self.error(101, "Not supported")

    def error(self, number, message):
        return ujson.dumps({"status": number, "message": message})
