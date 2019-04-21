import config
import machine
import mqtt_client
import sonoff_server_controller
import status_server_controller
import utils

_mqttClient = mqtt_client.MqttClient()
utils.__LOG_CALLBACK = lambda level, label, message: _mqttClient.publishLog(level, label, message)
utils.printInfo("SONOFF", "boot up")
utils.createSyncDateTimeTimer()
relayPin1 = machine.Pin(config.SONOFF_RELAY1_PIN, machine.Pin.OUT)
switchPin1 = machine.Pin(config.SONOFF_SWITCH1_PIN, machine.Pin.IN)
relayPin2 = machine.Pin(config.SONOFF_RELAY2_PIN, machine.Pin.OUT)
switchPin2 = machine.Pin(config.SONOFF_SWITCH2_PIN, machine.Pin.IN)
switch1 = (relayPin1, None, switchPin1)
switch2 = (relayPin2, None, switchPin2)
statusPin = machine.Pin(config.SONOFF_STATUS_PIN, machine.Pin.OUT)
statusController = status_server_controller.StatusServerController(_mqttClient, 'Sonoff')
sonoffServerController = sonoff_server_controller.SonoffServerController(_mqttClient, [switch1, switch2], statusPin)
_mqttClient.setControllers([statusController, sonoffServerController])

try:
    _mqttClient.run()
except KeyboardInterrupt:
    utils.printInfo("SONOFF", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printWarn("SONOFF", "exception during mqtt client run: %s" % e)
    machine.reset()
