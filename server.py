import socket

try:
    import ure as re
    import ujson as json
except:
    import re
    import json

REDIRECT_HEADERS = "HTTP/1.1 302\nLocation: %s\n"
RESPONSE_HEADERS = "HTTP/1.1 200 OK\nContent-Length: %d\nContent-Type: %s\nAccess-Control-Allow-Origin: *\nConnection: Closed\r\n\r\n%s"
JSON_TYPE_HEADER = "application/json"
HTML_TYPE_HEADER = "text/html"
SERVER = "http://192.168.0.203:20380/shajen/beer"
ERROR = "Not supported"

class Server:
    def __init__(self, port):
        self.addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]

    def run(self):
        s = socket.socket()
        s.bind(self.addr)
        s.listen(1)
        print('listening on', self.addr)
        while True:
            cl, self.addr = s.accept()
            # print('client connected from', self.addr)
            cl_file = cl.makefile('rwb', 0)
            response = None
            url = None
            data = {}
            while True:
                line = cl_file.readline().decode("utf-8")
                getMatch = re.match(r'GET (.*) HTTP.*', line)
                if getMatch:
                    url = getMatch.group(1)
                    paramMatch = re.match(r'(.*)\?(.*)=(.*)', url)
                    if paramMatch:
                        url = paramMatch.group(1)
                        data = {paramMatch.group(2).upper() : paramMatch.group(3).upper()}
                if not line or line == '\r\n':
                    break
            if url != None and url.endswith('/'):
                url = url[:-1]
            if url != None:
                response = self.processRequest(url.upper(), data)
            if response == None:
                response = Server.generateResponseRedirect(SERVER + url)
            cl.send(response)
            cl.close()

    @staticmethod
    def generateResponse(text, type):
        return RESPONSE_HEADERS % (len(text), type, text)

    @staticmethod
    def generateMessageResponse(status, message):
        return Server.generateResponse(json.dumps({'status':status, 'message':message}), JSON_TYPE_HEADER)

    @staticmethod
    def generateResponseJsonData(status, data):
        return Server.generateResponse(json.dumps({'status':status, 'data':data}), JSON_TYPE_HEADER)

    @staticmethod
    def generateResponseRedirect(url):
        return REDIRECT_HEADERS % url

    def processRequest(self, url, data):
        print('GET %s HTTP' % url)
        for key in data:
            print('  %s=%s' % (key, data[key]))
        if url == "":
            f = open('index.html')
            if f:
                return Server.generateResponse(f.read(), HTML_TYPE_HEADER)
