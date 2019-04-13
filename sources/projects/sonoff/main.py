import machine
import sonoff_server_controller
import server
import status_server_controller
import utils
import network

utils.printLog("NODEMCU", "sonoff")

statusPin = machine.Pin(13, machine.Pin.OUT)

def timeout1seconds():
    isconnected = network.WLAN(network.STA_IF).isconnected()
    statusPin.value(1 if not isconnected else 0)

def timeout10minutes():
    utils.syncDatetime()

tim0 = utils.timer()
tim0.init(period=1000, mode=machine.Timer.PERIODIC, callback=lambda t: timeout1seconds())
tim1 = utils.timer()
tim1.init(period=600000, mode=machine.Timer.PERIODIC, callback=lambda t: timeout10minutes())
timeout10minutes()

sonoffServerController = sonoff_server_controller.getInstance()
controllers = [sonoffServerController]
statusController = status_server_controller.StatusServerController('Sonoff', controllers)
_server = server.Server(33455, controllers + [statusController])
_server.run()
