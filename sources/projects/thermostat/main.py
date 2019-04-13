import config
import machine
import pre_boot
import server
import status_server_controller
import utils

utils.printLog("THERMOSTAT", "boot up")

_syncDateTimeTimer = utils.createSyncDateTimeTimer()
_controllers = [pre_boot._thermostat_server_controller]
_statusController = status_server_controller.StatusServerController('Thermostat', _controllers)
_server = server.Server(config.SERVER_PORT, _controllers + [_statusController])
try:
    _server.run()
except KeyboardInterrupt:
    _server.__del__()
    _statusController.__del__()
    pre_boot._thermostat_server_controller.__del__()
    pre_boot._temperature_sensor.__del__()
    _syncDateTimeTimer.deinit()
    utils.printLog("THERMOSTAT", "stopped by the user")
except Exception as e:
    utils.printLog("THERMOSTAT", "exception during server run: %s" % e)
    machine.reboot()
