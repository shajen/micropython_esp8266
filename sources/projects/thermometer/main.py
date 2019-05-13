import config
import temperature_sensor
import display
import machine
import mqtt_client
import status_server_controller
import utils

_mqttClient = mqtt_client.MqttClient()
utils.__LOG_CALLBACK = lambda level, label, message: _mqttClient.publishLog(level, label, message)
utils.printInfo("THERMOMETER", "boot up")
_temperature_sensor = temperature_sensor.TemperatureSensor(_mqttClient, machine.Pin(config.DS18B20_PIN), config.UPLOAD_SENSORS_INTERVAL_MS)
_rtc = machine.RTC()

if config.THERMOMETER_LOW_POWER_MODE and int(_rtc.memory().decode('utf-8')) <= 1:
    _temperature_sensor.update()
    _temperature_sensor.upload()
    _rtc.irq(trigger=_rtc.ALARM0, wake=machine.DEEPSLEEP)
    _rtc.alarm(_rtc.ALARM0, config.UPLOAD_SENSORS_INTERVAL_MS)
    utils.printInfo("THERMOMETER", "deep sleep for %d seconds" % (config.UPLOAD_SENSORS_INTERVAL_MS / 1000))
    machine.deepsleep()
else:
    _rtc.memory('0')
    utils.createSyncDateTimeTimer()
    if config.THERMOMETER_LOW_POWER_MODE:
        utils.createBlinkPinTimer(config.LED_STATUS_PIN, 500, 100, True)
    _i2c = machine.I2C(scl=machine.Pin(config.I2C_SCL_PIN), sda=machine.Pin(config.I2C_SDA_PIN), freq=400000)
    _display = display.Display(_i2c, _temperature_sensor, 'Thermometer')
    _statusController = status_server_controller.StatusServerController(_mqttClient, 'Thermometer')
    _mqttClient.setControllers([_statusController])

    try:
        _mqttClient.run()
    except KeyboardInterrupt:
        utils.printInfo("THERMOMETER", "stopped by the user")
        utils.deleteTimers()
    except Exception as e:
        utils.printWarn("THERMOMETER", "exception during mqtt client run: %s" % e)
        machine.reset()
