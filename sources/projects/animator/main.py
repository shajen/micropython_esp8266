import animator_server_controller
import config
import machine
import server
import status_server_controller
import utils

utils.printInfo("ANIMATOR", "boot up")
utils.createSyncDateTimeTimer()
animatorServerController = animator_server_controller.AnimatorServerController(machine.Pin(config.ANIMATOR_PIN, machine.Pin.OUT))
statusController = status_server_controller.StatusServerController('Animator', [animatorServerController])
_server = server.Server(config.SERVER_PORT, [statusController, animatorServerController])

try:
    _server.run()
except KeyboardInterrupt:
    utils.printInfo("ANIMATOR", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printWarn("ANIMATOR", "exception during mqtt client run: %s" % e)
    machine.reboot()
