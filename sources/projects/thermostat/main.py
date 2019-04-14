import config
import machine
import pre_boot
import server
import status_server_controller
import utils

utils.printLog("THERMOSTAT", "boot up")
utils.createSyncDateTimeTimer()
_controllers = [pre_boot._thermostat_server_controller]
_statusController = status_server_controller.StatusServerController('Thermostat', _controllers)
_server = server.Server(config.SERVER_PORT, _controllers + [_statusController])

try:
    _server.run()
except KeyboardInterrupt:
    utils.printLog("THERMOSTAT", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printLog("THERMOSTAT", "exception during server run: %s" % e)
    machine.reboot()
