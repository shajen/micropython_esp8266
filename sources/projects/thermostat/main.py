import config
import machine
import server
import status_server_controller
import temperature_sensor
import thermostat_server_controller
import utils
import utime

utils.printLog("NODEMCU", "thermostat boot up")

_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(14))
_switchPin = machine.Pin(0, machine.Pin.IN)
_relayPin = machine.Pin(12, machine.Pin.OUT)
_ledPin = machine.Pin(13, machine.Pin.OUT)

_thermostat_server_controller = thermostat_server_controller.initInstance(_temperature_sensor, _relayPin, _switchPin, _ledPin)

def timeout1second(timer):
    _temperature_sensor.update()
    _thermostat_server_controller.update()

def timeout1minute(timer):
    _temperature_sensor.upload()

def timeout10minutes(timer):
    utils.syncDatetime()

timeout1minute(None)
timeout10minutes(None)

tim1 = machine.Timer(0)
tim1.init(period=1000, mode=machine.Timer.PERIODIC, callback=timeout1second)
tim2 = machine.Timer(1)
tim2.init(period=60000, mode=machine.Timer.PERIODIC, callback=timeout1minute)
tim3 = machine.Timer(2)
tim3.init(period=600000, mode=machine.Timer.PERIODIC, callback=timeout10minutes)

_controllers = [_thermostat_server_controller]

statusController = status_server_controller.StatusServerController('Thermostat', _controllers)
_server = server.Server(config.SERVER_PORT, _controllers + [statusController])
_server.run()
