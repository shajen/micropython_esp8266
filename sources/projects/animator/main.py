import animator_server_controller
import config
import machine
import mqtt_client
import status_server_controller
import utils

_mqttClient = mqtt_client.MqttClient()
utils.__LOG_CALLBACK = lambda level, label, message: _mqttClient.publishLog(level, label, message)
utils.printInfo("ANIMATOR", "boot up")
utils.createSyncDateTimeTimer()
_statusController = status_server_controller.StatusServerController(_mqttClient, 'Animator')
_animatorServerController = animator_server_controller.AnimatorServerController(_mqttClient, machine.Pin(config.ANIMATOR_PIN, machine.Pin.OUT))
_mqttClient.setControllers([_statusController, _animatorServerController])

try:
    _mqttClient.run()
except KeyboardInterrupt:
    utils.printInfo("ANIMATOR", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printWarn("ANIMATOR", "exception during mqtt client run: %s" % e)
    machine.reset()
