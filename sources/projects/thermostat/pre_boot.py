import config
import machine
import temperature_sensor
import thermostat_server_controller

_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.DS18B20_PIN))
_relay_pin = machine.Pin(config.THERMOSTAT_RELAY_PIN, machine.Pin.OUT)
_switch_pin = machine.Pin(config.THERMOSTAT_SWITCH_PIN, machine.Pin.IN)
_led_pin = machine.Pin(config.THERMOSTAT_LED_PIN, machine.Pin.OUT)

_thermostat_server_controller = thermostat_server_controller.ThermostatServerController(_temperature_sensor, _relay_pin, _switch_pin, _led_pin)
