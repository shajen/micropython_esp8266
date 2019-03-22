import config
import temperature_sensor
import machine
import server
import status_server_controller
import utils
import utime

utils.printLog("NODEMCU", "thermostat boot up")

_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(14))

def timeout1second(timer):
    _temperature_sensor.update()

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

statusController = status_server_controller.StatusServerController('Thermostat', [])
_server = server.Server(config.SERVER_PORT, [statusController])
_server.run()
