import animator_server_controller
import config
import machine
import server
import status_server_controller
import utils

utils.printLog("ANIMATOR", "boot up")
utils.createSyncDateTimeTimer()
animatorServerController = animator_server_controller.AnimatorServerController(machine.Pin(config.D4, machine.Pin.OUT))
statusController = status_server_controller.StatusServerController('Animator', [animatorServerController])
_server = server.Server(config.SERVER_PORT, [statusController, animatorServerController])

try:
    _server.run()
except KeyboardInterrupt:
    utils.printLog("ANIMATOR", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printLog("ANIMATOR", "exception during server run: %s" % e)
    machine.reboot()
