from machine import Timer
from utils import syncDatetime, printDebug, printLog
import rstrip_server_controller
import server

printLog("NODEMCU", "boot up")
syncDatetime()

tim0 = Timer(0)
tim0.init(period=600000, mode=Timer.PERIODIC, callback=lambda t: syncDatetime())

_controller = rstrip_server_controller.RstripServerController()
_server = server.Server(33455, _controller)
_server.run()
