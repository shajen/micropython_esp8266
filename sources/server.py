import usocket
import ure
from helper import printLog, printDebug

class Server():
    def __init__(self, port, controller):
        self.port = port
        self.controller = controller
        self.re = ure.compile("GET (.*) HTTP")

    def run(self):
        printLog('SERVER', ('listening on port %s' % self.port))
        addr = usocket.getaddrinfo('0.0.0.0', self.port)[0][-1]
        socket = usocket.socket()
        socket.bind(addr)
        socket.listen(1)

        while True:
            cl, addr = socket.accept()
            printDebug('SERVER', 'client connected from %s:%s' % (addr[0], addr[1]))
            data = cl.recv(4096).decode("utf-8").upper()
            match = self.re.search(data)
            if match:
                (url, params) = self.parseUrl(match.group(1))
                printDebug('SERVER', 'GET %s %s' % (url, params))
                response = self.controller.process(url, params)
                printDebug('SERVER', 'response: %s' % response)
                cl.send(response + '\r\n')
            else:
                printDebug('SERVER', 'can not parase request')
            cl.close()

    def parseUrl(self, url):
        if '?' in url:
            p = url.split("?")
            pairs = map(lambda s: s.split('=') if '=' in s else [s, ''], p[1].split('&'))
            return (self.uniteUrl(p[0]), dict((k,v) for [k,v] in pairs))
        else:
            return (self.uniteUrl(url), {})

    def uniteUrl(self, url):
        return url if url.endswith('/') else url + '/'
