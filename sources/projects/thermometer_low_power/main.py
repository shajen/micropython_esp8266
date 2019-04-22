import config
import machine
import mqtt_client
import temperature_sensor
import utils

_mqttClient = mqtt_client.MqttClient()
utils.__LOG_CALLBACK = lambda level, label, message: _mqttClient.publishLog(level, label, message)
utils.printInfo("NODEMCU", "thermometer low power boot up")
_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.DS18B20_PIN), _mqttClient)
_temperature_sensor.update()
_temperature_sensor.upload()

rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
rtc.alarm(rtc.ALARM0, 60000)

machine.deepsleep()
