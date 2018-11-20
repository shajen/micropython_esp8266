import machine
import pin_server_controller
import server
import status_server_controller
import utils

utils.printLog("NODEMCU", "rstrip boot up")

def timeout10minutes():
    utils.syncDatetime()

tim0 = machine.Timer(0)
tim0.init(period=600000, mode=Timer.PERIODIC, callback=lambda t: timeout10minutes())
timeout10minutes()

pinServerController = pin_server_controller.PinServerController()
controllers = [pinServerController]
statusController = status_server_controller.StatusServerController(controllers)
_server = server.Server(33455, controllers + [statusController])
_server.run()
