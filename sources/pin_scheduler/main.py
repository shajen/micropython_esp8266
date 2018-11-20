import config
import devices
import machine
import pin_scheduler
import server
import status_server_controller
import utils

utils.printLog("NODEMCU", "water can boot up")

_devices = devices.Devices()
pinScheduler = pin_scheduler.PinScheduler()
statusController = status_server_controller.StatusServerController([])
_server = server.Server(config.SERVER_PORT, [statusController])

def timeout1second(timer):
    _devices.update()
    pinScheduler.update()

def timeout1minute(timer):
    if not pinScheduler.isTimeNearScheduler():
        _devices.upload()

def timeout10minutes(timer):
    pass

def timeout1hour(timer):
    if not pinScheduler.isTimeNearScheduler():
        utils.syncDatetime()

timeout1minute(None)
timeout10minutes(None)
timeout1hour(None)

tim1 = machine.Timer(0)
tim1.init(period=1000, mode=Timer.PERIODIC, callback=timeout1second)
tim2 = machine.Timer(1)
tim2.init(period=60000, mode=Timer.PERIODIC, callback=timeout1minute)
tim3 = machine.Timer(2)
tim3.init(period=600000, mode=Timer.PERIODIC, callback=timeout10minutes)
tim4 = machine.Timer(3)
tim4.init(period=3600000, mode=Timer.PERIODIC, callback=timeout1hour)

_server.run()
