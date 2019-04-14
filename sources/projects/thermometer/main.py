import config
import temperature_sensor
import display
import machine
import server
import status_server_controller
import utils

utils.printLog("THERMOMETER", "boot up")
utils.createSyncDateTimeTimer()
_i2c = machine.I2C(scl=machine.Pin(config.I2C_SCL_PIN), sda=machine.Pin(config.I2C_SDA_PIN), freq=400000)
_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.DS18B20_PIN))
_display = display.Display(_i2c, _temperature_sensor, 'Thermometer')
_statusController = status_server_controller.StatusServerController('Thermometer', [])
_server = server.Server(config.SERVER_PORT, [_statusController])

try:
    _server.run()
except KeyboardInterrupt:
    utils.printLog("THERMOMETER", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printLog("THERMOMETER", "exception during server run: %s" % e)
    machine.reboot()
