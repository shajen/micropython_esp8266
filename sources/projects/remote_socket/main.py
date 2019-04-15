import config
import machine
import pin_server_controller
import server
import status_server_controller
import temperature_sensor
import utils

utils.printInfo("REMOTE_SOCKET", "boot up")
utils.createSyncDateTimeTimer()
_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.DS18B20_PIN))
pinServerController = pin_server_controller.PinServerController(config.REMOTE_SOCKET_PINS)
controllers = [pinServerController]
statusController = status_server_controller.StatusServerController('Remote Socket', controllers)
_server = server.Server(config.SERVER_PORT, controllers + [statusController])

try:
    _server.run()
except KeyboardInterrupt:
    utils.printInfo("REMOTE_SOCKET", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printWarn("REMOTE_SOCKET", "exception during server run: %s" % e)
    machine.reboot()
