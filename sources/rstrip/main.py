from machine import Timer
from utils import syncDatetime, printDebug, printLog
import rstrip_server_controller
import status_server_controller
import server

printLog("NODEMCU", "rstrip boot up")

def timeout10minutes():
    syncDatetime()

tim0 = Timer(0)
tim0.init(period=600000, mode=Timer.PERIODIC, callback=lambda t: timeout10minutes())
timeout10minutes()

rstripController = rstrip_server_controller.RstripServerController()
controllers = [rstripController]
statusController = status_server_controller.StatusServerController(controllers)
_server = server.Server(33455, controllers + [statusController])
_server.run()
