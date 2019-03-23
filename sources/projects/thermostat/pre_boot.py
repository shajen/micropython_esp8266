import machine
import temperature_sensor
import thermostat_server_controller

_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(14))
_relay_pin = machine.Pin(12, machine.Pin.OUT)
_switch_pin = machine.Pin(0, machine.Pin.IN)
_led_pin = machine.Pin(13, machine.Pin.OUT)

_thermostat_server_controller = thermostat_server_controller.ThermostatServerController(_temperature_sensor, _relay_pin, _switch_pin, _led_pin)
