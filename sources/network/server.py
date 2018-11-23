import ujson
import ure
import usocket
import utils

class Server():
    def __init__(self, port, controllers):
        self.port = port
        self.controllers = controllers
        self.re = ure.compile("GET (.*) HTTP")

    def run(self):
        utils.printLog('SERVER', ('listening on port %s' % self.port))
        addr = usocket.getaddrinfo('0.0.0.0', self.port)[0][-1]
        socket = usocket.socket()
        socket.bind(addr)
        socket.listen(1)

        while True:
            cl, addr = socket.accept()
            utils.printDebug('SERVER', 'client connected from %s:%s' % (addr[0], addr[1]))
            (url, params, useHtml) = self.parseRequest(cl)
            if url:
                utils.printDebug('SERVER', 'GET %s %s (http:%s)' % (url, params, useHtml))
                send = False
                for controller in self.controllers:
                    response = controller.process(url, params)
                    if response:
                        utils.printDebug('SERVER', 'response: %s' % response)
                        self.sendResponse(cl, response, 200, useHtml)
                        send = True
                        break
                if not send:
                    response = self.error(101, "Not supported")
                    utils.printDebug('SERVER', 'response: %s' % response)
                    self.sendResponse(cl, response, 404, useHtml)
            else:
                self.sendResponse(cl, 'can not parse request', 404, useHtml)

    def sendResponse(self, cl, response, status, useHtml):
        response = response.rstrip() + "\r\n"
        if useHtml:
            cl.send('HTTP/1.1 %d OK\r\n' % status)
            cl.send('Content-Type: application/javascript\r\n')
            cl.send('Content-Length: %d\r\n' % len(response))
            cl.send('Connection: Closed\r\n')
            cl.send('\r\n')
        cl.send(response)
        cl.close()

    def parseRequest(self, cl):
        url = None
        params = None
        useHtml = False
        try:
            cl_file = cl.makefile('rwb', 0)
            while True:
                line = cl_file.readline().decode("utf-8").upper() ### TODO: fix it
                if not line or line == '\r\n':
                    break
                match = self.re.search(line)
                if match:
                    (url, params) = self.parseUrl(match.group(1))
                useHtml = useHtml or 'HOST:' in line
            if url == None:
                utils.printDebug('SERVER', 'can not parse request')
        except:
            utils.printDebug('SERVER', 'exception during parse request')
        return (url, params, useHtml)

    def parseUrl(self, url):
        if '?' in url:
            p = url.split("?")
            pairs = map(lambda s: s.split('=') if '=' in s else [s, ''], p[1].split('&'))
            return (self.uniteUrl(p[0]), dict((k,v) for [k,v] in pairs))
        else:
            return (self.uniteUrl(url), {})

    def uniteUrl(self, url):
        return url if url.endswith('/') else url + '/'

    def error(self, number, message):
        return ujson.dumps({"status": number, "message": message})