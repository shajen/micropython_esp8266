import config
import machine
import mqtt_client
import pin_server_controller
import status_server_controller
import temperature_sensor
import utils

_mqttClient = mqtt_client.MqttClient()
utils.__LOG_CALLBACK = lambda level, label, message: _mqttClient.publishLog(level, label, message)
utils.printInfo("REMOTE_SOCKET", "boot up")
utils.createSyncDateTimeTimer()
_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.DS18B20_PIN), _mqttClient)
statusController = status_server_controller.StatusServerController(_mqttClient, 'Remote Socket')
pinServerController = pin_server_controller.PinServerController(_mqttClient, config.REMOTE_SOCKET_PINS)
_mqttClient.setControllers([statusController, pinServerController])

try:
    _mqttClient.run()
except KeyboardInterrupt:
    utils.printInfo("REMOTE_SOCKET", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printWarn("REMOTE_SOCKET", "exception during server run: %s" % e)
    machine.reset()
