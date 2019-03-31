import config
import temperature_sensor
import display
import machine
import server
import status_server_controller
import utils

utils.printLog("THERMOMETER", "boot up")

_i2c = machine.I2C(scl=machine.Pin(config.D2), sda=machine.Pin(config.D1), freq=400000)
_syncDateTimeTimer = utils.createSyncDateTimeTimer()
_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.D3))
_display = display.Display(_i2c, _temperature_sensor)
_statusController = status_server_controller.StatusServerController('Thermometer', [])
_server = server.Server(config.SERVER_PORT, [_statusController])

try:
    _server.run()
except KeyboardInterrupt:
    _server.__del__()
    _statusController.__del__()
    _temperature_sensor.__del__()
    _display.__del__()
    _syncDateTimeTimer.deinit()
    utils.printLog("THERMOMETER", "stopped by the user")
except Exception as e:
    utils.printLog("THERMOMETER", "exception during server run: %s" % e)
    machine.reboot()
