import animator_server_controller
import config
import machine
import neopixel
import server
import status_server_controller
import utils

utils.printLog("NODEMCU", "animator boot up")

np = neopixel.NeoPixel(machine.Pin(config.WS2811_PIN), 60)
animatorServerController = animator_server_controller.AnimatorServerController(np)
statusController = status_server_controller.StatusServerController([animatorServerController])

def timeout10milliseconds(timer):
    animatorServerController.tick()

def timeout10minutes(timer):
    utils.syncDatetime()

def timeout1hours(timer):
    if config.REBOOT_EVERY_HOUR:
        machine.reset()

timeout10minutes(None)

tim1 = machine.Timer(0)
tim1.init(period=10, mode=machine.Timer.PERIODIC, callback=timeout10milliseconds)
tim3 = machine.Timer(2)
tim3.init(period=600000, mode=machine.Timer.PERIODIC, callback=timeout10minutes)
tim4 = machine.Timer(3)
tim4.init(period=3600000, mode=machine.Timer.PERIODIC, callback=timeout1hours)

_server = server.Server(config.SERVER_PORT, [statusController, animatorServerController])
_server.run()
