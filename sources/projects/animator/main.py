import animator_server_controller
import config
import machine
import server
import status_server_controller
import utils

utils.printLog("NODEMCU", "animator boot up")

animatorServerController = animator_server_controller.AnimatorServerController(machine.Pin(config.D4, machine.Pin.OUT))
statusController = status_server_controller.StatusServerController('Animator', [animatorServerController])

def timeoutTick(timer):
    animatorServerController.tick()

def timeout10minutes(timer):
    utils.syncDatetime()

timeout10minutes(None)

tim1 = utils.timer()
tim1.init(period=1, mode=machine.Timer.PERIODIC, callback=timeoutTick)
tim3 = utils.timer()
tim3.init(period=600000, mode=machine.Timer.PERIODIC, callback=timeout10minutes)

_server = server.Server(config.SERVER_PORT, [statusController, animatorServerController])
_server.run()
