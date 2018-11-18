from config import SERVER_PORT, REBOOT_EVERY_HOUR
from machine import Pin, Timer, reset
from utils import syncDatetime, printDebug, printLog
import server
import status_server_controller
import animator_server_controller

printLog("NODEMCU", "animator boot up")

animatorServerController = animator_server_controller.AnimatorServerController()
statusController = status_server_controller.StatusServerController([animatorServerController])

def timeout10milliseconds(timer):
    animatorServerController.tick()

def timeout10minutes(timer):
    syncDatetime()

def timeout1hours(timer):
    if REBOOT_EVERY_HOUR:
        reset()

timeout10minutes(None)

tim1 = Timer(0)
tim1.init(period=10, mode=Timer.PERIODIC, callback=timeout10milliseconds)
tim3 = Timer(2)
tim3.init(period=600000, mode=Timer.PERIODIC, callback=timeout10minutes)
tim4 = Timer(3)
tim4.init(period=3600000, mode=Timer.PERIODIC, callback=timeout1hours)

_server = server.Server(SERVER_PORT, [statusController, animatorServerController])
_server.run()
