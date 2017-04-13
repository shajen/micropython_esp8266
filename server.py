from helper import printLog, printDebug
import socket
import ure as re
import ujson as json
import utime as time
import gc

REDIRECT_HEADERS = "HTTP/1.1 302\nLocation: %s\n"
RESPONSE_HEADERS = "HTTP/1.1 200 OK\nContent-Length: %d\nContent-Type: %s\nAccess-Control-Allow-Origin: *\nConnection: Closed\r\n\r\n%s"
JSON_TYPE_HEADER = "application/json"
HTML_TYPE_HEADER = "text/html"
SERVER = "http://192.168.0.203:20380/shajen/beer"
ERROR = "Not supported"

class Server:
    def __init__(self, port, devices, brew, display):
        self.addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        self.devices = devices
        self.brew = brew
        self.display = display

    def run(self):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(self.addr)
        s.listen(1)
        printLog('SERVER', 'listening...')
        while True:
            gc.collect()
            cl, self.addr = s.accept()
            (url, parameters) = self.parseRequest(cl)
            printDebug('SERVER', 'GET %s PARAMS %s' % (url, parameters))
            response = None
            if url != None:
                response = self.processRequest(url.upper(), parameters)
            if response == None:
                if url != None:
                    response = Server.generateResponseRedirect(SERVER + url)
                else:
                    response = Server.generateMessageResponse(100, ERROR)
            cl.send(response)
            cl.close()

    def parseRequest(self, cl):
        url = None
        parameters = {}

        for line in cl.recv(1024).decode("utf-8").split('\n'):
            if url == None and line.startswith('GET'):
                 url = line.split(' ')[1]

        if url != None and '?' in url:
            (url, parametersString) = url.split('?')
            for parameterString in parametersString.upper().split('&'):
                parameter = parameterString.split('=')
                parameters[parameter[0]] = parameter[1]

        if url != None and url.endswith('/'):
            url = url[:-1]
        return (url, parameters)

    @staticmethod
    def generateResponse(text, type):
        return RESPONSE_HEADERS % (len(text), type, text)

    @staticmethod
    def generateMessageResponse(status, message):
        return Server.generateResponse(json.dumps({'STATUS':status, 'MESSAGE':message}), JSON_TYPE_HEADER)

    @staticmethod
    def generateResponseJsonData(status, data):
        return Server.generateResponse(json.dumps({'STATUS':status, 'DATA':data}), JSON_TYPE_HEADER)

    @staticmethod
    def generateResponseRedirect(url):
        return REDIRECT_HEADERS % url

    def processRequest(self, url, data):
        if url == "":
            f = open('index.html')
            if f:
                return Server.generateResponse(f.read(), HTML_TYPE_HEADER)
        if url.startswith('/API'):
            return self.processApi(url[4:], data)

    def processApi(self, url, data):
        if url == '/STATUS':
            return self.apiStatus()
        elif url == '/PUMP' and 'LEVEL' in data:
            self.devices.setPump(int(data['LEVEL']))
            return self.apiStatus()
        elif url == '/HEATER' and 'LEVEL' in data:
            self.devices.setHeater(int(data['LEVEL']))
            return self.apiStatus()
        elif url == '/FAN' and 'LEVEL' in data:
            self.devices.setFan(int(data['LEVEL']))
            return self.apiStatus()
        elif url == '/SETTINGS':
            if 'SOUND' in data:
                self.devices.setSound(data['SOUND'] == 'PLAY')
            if 'BACKLIGHT' in data:
                self.display.setBacklight(data['BACKLIGHT'] == 'ENABLE')
            return self.apiStatus()
        elif url == '/BREW':
            if 'TEMP' in data:
                self.brew.setTemperature(int(data['TEMP']))
            if 'ACTION' in data:
                if data['ACTION'] == 'START':
                    self.brew.start()
                if data['ACTION'] == 'STOP':
                    self.brew.stop()
            if 'MODE' in data:
                self.brew.setMode(data['MODE'])
            if 'BREAKS' in data:
                self.brew.setBreaks(json.loads(data['BREAKS'].replace('%22', '"')))
            return self.apiStatus()
        else:
            return None

    def apiStatus(self):
        gc.collect()
        free = gc.mem_free()
        data = {}

        data['NODE'] = {}
        data['NODE']['HEAP'] = free
        data['NODE']['UPTIME'] = int(time.ticks_ms() / 1000)
        data['NODE']['VOLTAGE'] = 0
        data['NODE']['WIFI'] = {}
        data['NODE']['WIFI']['SIGNAL'] = 0
        data['NODE']['WIFI']['SSID'] = ''
        data['NODE']['WIFI']['MAC'] = ''

        data['SETTINGS'] = {}
        data['SETTINGS']['SOUND'] = self.devices.getSound()
        data['SETTINGS']['BACKLIGHT'] = self.display.getBacklight()

        data['DEVICES'] = {}
        data['DEVICES']['PUMP'] = self.devices.getPump()
        data['DEVICES']['HEATER'] = self.devices.getHeater()
        data['DEVICES']['FAN'] = self.devices.getFan()

        data['TEMP'] = {}
        data['TEMP']['INTERNAL'] = self.devices.getInternalTemperature()
        data['TEMP']['EXTERNAL'] = self.devices.getExternalTemperatures()
        data['TEMP']['AVERAGE_EXTERNAL'] = self.devices.getAverageExternalTemperature()

        data['BREW'] = {}
        data['BREW']['MODE'] = self.brew.getMode()
        data['BREW']['TEMP'] = self.brew.getTemperature()
        data['BREW']['BREAKS'] = self.brew.getBreaks()
        data['BREW']['STARTED'] = self.brew.isStarted()
        return Server.generateResponseJsonData(0, data)
