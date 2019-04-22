import config
import machine
import mqtt_client
import pin_scheduler
import status_server_controller
import temperature_sensor
import utils

_mqttClient = mqtt_client.MqttClient()
utils.__LOG_CALLBACK = lambda level, label, message: _mqttClient.publishLog(level, label, message)
utils.printInfo("PIN_SCHEDULER", "boot up")
_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.DS18B20_PIN), _mqttClient)
pinScheduler = pin_scheduler.PinScheduler(machine.Pin(config.SCHEDULER_PIN, machine.Pin.OUT), [((19, 0, 0), 36)])
statusController = status_server_controller.StatusServerController(_mqttClient, 'Sonoff')
_mqttClient.setControllers([statusController])

try:
    _mqttClient.run()
except KeyboardInterrupt:
    utils.printInfo("PIN_SCHEDULER", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printWarn("PIN_SCHEDULER", "exception during mqtt client run: %s" % e)
    machine.reset()
