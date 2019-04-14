import config
import machine
import server
import status_server_controller
import temperature_sensor
import thermostat_server_controller
import utils

utils.printLog("THERMOSTAT", "boot up")
utils.createSyncDateTimeTimer()
_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.DS18B20_PIN))
_relay_pin = machine.Pin(config.THERMOSTAT_RELAY_PIN, machine.Pin.OUT)
_switch_pin = machine.Pin(config.THERMOSTAT_SWITCH_PIN, machine.Pin.IN)
_led_pin = machine.Pin(config.THERMOSTAT_LED_PIN, machine.Pin.OUT)
_thermostat_server_controller = thermostat_server_controller.ThermostatServerController(_temperature_sensor, _relay_pin, _switch_pin, _led_pin)
_controllers = [_thermostat_server_controller]
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
