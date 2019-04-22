import ws2812_server_controller
import config
import machine
import mqtt_client
import status_server_controller
import utils

_mqttClient = mqtt_client.MqttClient()
utils.__LOG_CALLBACK = lambda level, label, message: _mqttClient.publishLog(level, label, message)
utils.printInfo("WS2812", "boot up")
utils.createSyncDateTimeTimer()
_statusController = status_server_controller.StatusServerController(_mqttClient, 'WS2812')
_ws2812ServerController = ws2812_server_controller.Ws2812ServerController(_mqttClient, machine.Pin(config.WS2812_PIN, machine.Pin.OUT))
_mqttClient.setControllers([_statusController, _ws2812ServerController])

try:
    _mqttClient.run()
except KeyboardInterrupt:
    utils.printInfo("WS2812", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printWarn("WS2812", "exception during mqtt client run: %s" % e)
    machine.reset()
