import config
import machine
import mqtt_client
import temperature_sensor
import utils

_mqttClient = mqtt_client.MqttClient()
utils.__LOG_CALLBACK = lambda level, label, message: _mqttClient.publishLog(level, label, message)
utils.printInfo("THERMOMETERLP", "boot up")
_temperature_sensor = temperature_sensor.TemperatureSensor(_mqttClient, machine.Pin(config.DS18B20_PIN), config.UPLOAD_SENSORS_INTERVAL_MS)
_temperature_sensor.update()
_temperature_sensor.upload()

rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
rtc.alarm(rtc.ALARM0, config.UPLOAD_SENSORS_INTERVAL_MS)

utils.printInfo("THERMOMETERLP", "deep sleep for %d seconds" % (config.UPLOAD_SENSORS_INTERVAL_MS / 1000))
machine.deepsleep()
