from config import SERVER_PORT
from machine import Timer
from utils import syncDatetime, printLog
import devices
import server
import status_server_controller
import water_can_controller

printLog("NODEMCU", "water can boot up")

_devices = devices.Devices()

def timeout1second(timer):
    _devices.update()
    waterCanController.update()

def timeout1minute(timer):
    _devices.upload()

def timeout10minutes(timer):
    pass

def timeout24hour(timer):
    syncDatetime()

timeout1minute(None)
timeout10minutes(None)
timeout24hour(None)

tim1 = Timer(0)
tim1.init(period=1000, mode=Timer.PERIODIC, callback=timeout1second)
tim2 = Timer(1)
tim2.init(period=60000, mode=Timer.PERIODIC, callback=timeout1minute)
tim3 = Timer(2)
tim3.init(period=600000, mode=Timer.PERIODIC, callback=timeout10minutes)
tim4 = Timer(3)
tim4.init(period=86400000, mode=Timer.PERIODIC, callback=timeout24hour)

waterCanController = water_can_controller.WaterCanController()
statusController = status_server_controller.StatusServerController([])
_server = server.Server(SERVER_PORT, [statusController])
_server.run()
