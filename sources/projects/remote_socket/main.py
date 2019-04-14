import config
import machine
import pin_server_controller
import server
import status_server_controller
import temperature_sensor
import utils

utils.printLog("REMOTE_SOCKET", "boot up")
utils.createSyncDateTimeTimer()
_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.D6))
pinServerController = pin_server_controller.PinServerController([config.D1, config.D2, config.D5, config.D7, config.D8])
controllers = [pinServerController]
statusController = status_server_controller.StatusServerController('Remote Socket', controllers)
_server = server.Server(33455, controllers + [statusController])

try:
    _server.run()
except KeyboardInterrupt:
    utils.printLog("REMOTE_SOCKET", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printLog("REMOTE_SOCKET", "exception during server run: %s" % e)
    machine.reboot()
