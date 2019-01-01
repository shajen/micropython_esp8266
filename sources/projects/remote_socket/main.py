import config
import machine
import pin_server_controller
import server
import status_server_controller
import temperature_sensor
import utils

utils.printLog("NODEMCU", "rstrip boot up")

_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.D6))

def timeout1minute(timer):
    _temperature_sensor.update()
    _temperature_sensor.upload()

def timeout10minutes(timer):
    utils.syncDatetime()

tim0 = machine.Timer(0)
tim0.init(period=60000, mode=machine.Timer.PERIODIC, callback=timeout1minute)
tim1 = machine.Timer(1)
tim1.init(period=600000, mode=machine.Timer.PERIODIC, callback=lambda t: timeout10minutes())
timeout1minute(None)
timeout10minutes(None)

pinServerController = pin_server_controller.PinServerController([config.D1, config.D2, config.D5, config.D7, config.D8])
controllers = [pinServerController]
statusController = status_server_controller.StatusServerController('Remote Socket', controllers)
_server = server.Server(33455, controllers + [statusController])
_server.run()
