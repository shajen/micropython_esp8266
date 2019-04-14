import ujson
import usocket
import utils
import time
import uasyncio as asyncio

class Server():
    def __init__(self, port, controllers):
        utils.printLog('SERVER', 'init')
        self.port = port
        self.controllers = controllers

    def run(self):
        utils.printLog('SERVER', ('listening on port %s' % self.port))
        loop = asyncio.get_event_loop()
        loop.create_task(asyncio.start_server(self.process, '0.0.0.0', self.port))
        loop.run_forever()
        loop.close()
            
    async def process(self, reader, writer):
        try:
            utils.printDebug('SERVER', 'client connected')
            (url, params, useHtml) = await self.parseRequest(reader)
            if url:
                utils.printDebug('SERVER', 'GET %s %s (http:%s)' % (url, params, useHtml))
                send = False
                for controller in self.controllers:
                    response = controller.process(url, params)
                    if response:
                        await self.sendResponse(writer, response, 200, useHtml)
                        send = True
                        break
                if not send:
                    response = utils.jsonResponse(404, "Not found")
                    await self.sendResponse(writer, response, 404, useHtml)
            else:
                response = utils.jsonResponse(400, "Bad Request")
                await self.sendResponse(writer, response, 400, useHtml)
        except Exception as e:
            try:
                utils.printDebug('SERVER', 'exception %s' % str(e))
                response = utils.jsonResponse(500, "Internal Server Error")
                await self.sendResponse(writer, response, 500, True)
            except Exception as e:
                utils.printDebug('SERVER', 'exception during sendResponse %s' % str(e))

    async def sendResponse(self, writer, response, status, useHtml):
        utils.printDebug('SERVER', 'response status: %s' % status)
        utils.printDebug('SERVER', 'response: %s' % response)
        response = response.rstrip() + "\r\n"
        if useHtml:
            await writer.awrite('HTTP/1.1 %d OK\r\n' % status)
            await writer.awrite('Content-Type: application/javascript\r\n')
            await writer.awrite('Content-Length: %d\r\n' % len(response))
            await writer.awrite('Connection: Closed\r\n')
            await writer.awrite('\r\n')
        await writer.awrite(response)
        writer.aclose()

    async def parseRequest(self, reader):
        url = None
        params = None
        useHtml = False
        try:
            while True:
                line = await reader.readline()
                if not line:
                    break
                line = line.decode("utf-8").upper() ### TODO: fix it
                if line == '\r\n':
                    break
                if line.startswith('GET '):
                    startPos = line.find(' ') + 1
                    endPos = line.rfind(' ')
                    (url, params) = self.parseUrl(line[startPos:endPos])
                useHtml = useHtml or 'HOST:' in line
            if url == None:
                utils.printDebug('SERVER', 'can not parse request')
        except Exception as e:
            while True:
                line = await reader.readline()
                if not line:
                    break
                line = line.decode("utf-8").upper() ### TODO: fix it
                if line == '\r\n':
                    break
            utils.printDebug('SERVER', 'exception during parse request: %s' % str(e))
            useHtml = True
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
