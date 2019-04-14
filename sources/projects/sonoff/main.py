import config
import machine
import network
import server
import sonoff_server_controller
import status_server_controller
import utils

utils.printLog("SONOFF", "boot up")
utils.createSyncDateTimeTimer()

statusPin = machine.Pin(config.SONOFF_STATUS_PIN, machine.Pin.OUT)

def timeout1seconds():
    isconnected = network.WLAN(network.STA_IF).isconnected()
    statusPin.value(1 if not isconnected else 0)

tim0 = utils.timer()
tim0.init(period=1000, mode=machine.Timer.PERIODIC, callback=lambda t: timeout1seconds())

sonoffServerController = sonoff_server_controller.getInstance()
controllers = [sonoffServerController]
statusController = status_server_controller.StatusServerController('Sonoff', controllers)
_server = server.Server(config.SERVER_PORT, controllers + [statusController])

try:
    _server.run()
except KeyboardInterrupt:
    utils.printLog("SONOFF", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printLog("SONOFF", "exception during server run: %s" % e)
    machine.reboot()
