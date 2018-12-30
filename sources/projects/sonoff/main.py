import machine
import sonoff_server_controller
import server
import status_server_controller
import utils

utils.printLog("NODEMCU", "sonoff")

def timeout10minutes():
    utils.syncDatetime()

tim0 = machine.Timer(0)
tim0.init(period=600000, mode=machine.Timer.PERIODIC, callback=lambda t: timeout10minutes())
timeout10minutes()

relayPin = machine.Pin(12, machine.Pin.OUT)
ledPin = machine.Pin(13, machine.Pin.OUT)
switchPin = machine.Pin(0, machine.Pin.IN)

sonoffServerController = sonoff_server_controller.SonoffServerController(relayPin, ledPin, switchPin)
controllers = [sonoffServerController]
statusController = status_server_controller.StatusServerController('Sonoff', controllers)
_server = server.Server(33455, controllers + [statusController])
_server.run()
