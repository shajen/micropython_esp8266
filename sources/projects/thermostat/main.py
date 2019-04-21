import config
import machine
import mqtt_client
import status_server_controller
import temperature_sensor
import thermostat_server_controller
import utils

_mqttClient = mqtt_client.MqttClient()
utils.__LOG_CALLBACK = lambda level, label, message: _mqttClient.publishLog(level, label, message)
utils.printInfo("THERMOSTAT", "boot up")
utils.createSyncDateTimeTimer()
_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.DS18B20_PIN), _mqttClient)
_relay_pin = machine.Pin(config.THERMOSTAT_RELAY_PIN, machine.Pin.OUT)
_switch_pin = machine.Pin(config.THERMOSTAT_SWITCH_PIN, machine.Pin.IN)
_led_pin = machine.Pin(config.THERMOSTAT_LED_PIN, machine.Pin.OUT)
_statusController = status_server_controller.StatusServerController(_mqttClient, 'Thermostat')
_thermostat_server_controller = thermostat_server_controller.ThermostatServerController(_mqttClient, _temperature_sensor, _relay_pin, _switch_pin, _led_pin)
_mqttClient.setControllers([_statusController, _thermostat_server_controller])

try:
    _mqttClient.run()
except KeyboardInterrupt:
    utils.printInfo("THERMOSTAT", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printWarn("THERMOSTAT", "exception during mqtt client run: %s" % e)
    machine.reset()
