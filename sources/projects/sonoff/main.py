import config
import machine
import server
import sonoff_server_controller
import status_server_controller
import utils

utils.printLog("SONOFF", "boot up")
utils.createSyncDateTimeTimer()
relayPin1 = machine.Pin(config.SONOFF_RELAY1_PIN, machine.Pin.OUT)
switchPin1 = machine.Pin(config.SONOFF_SWITCH1_PIN, machine.Pin.IN)
relayPin2 = machine.Pin(config.SONOFF_RELAY2_PIN, machine.Pin.OUT)
switchPin2 = machine.Pin(config.SONOFF_SWITCH2_PIN, machine.Pin.IN)
switch1 = (relayPin1, None, switchPin1)
switch2 = (relayPin2, None, switchPin2)
statusPin = machine.Pin(config.SONOFF_STATUS_PIN, machine.Pin.OUT)
sonoffServerController = sonoff_server_controller.SonoffServerController([switch1, switch2], statusPin)
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
