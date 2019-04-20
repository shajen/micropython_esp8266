import config
import machine
import ubinascii
import umqtt.simple
import utime

class MqttClient():
    def __init__(self):
        self._id = ubinascii.hexlify(machine.unique_id()[:-1]).decode('utf-8')
        self.client = umqtt.simple.MQTTClient(self._id, config.MQTT_SERVER, port=config.MQTT_PORT, user=config.MQTT_USER, password=config.MQTT_PASSWORD)
        self.client.connect()
        self._publishDevice('hello', '')

    def _publishDevice(self, topic, message):
        self.client.publish("/device/%s/%s" % (self._id, topic), message)

    def _publishSensor(self, type, id, value):
        self._publishDevice('sensor/%s' % type, '{"id":"%s", "value":%.6f}' % (id, value))

    def publishTemperature(self, id, value):
        self._publishSensor('temperature', id, value)

    def publishLog(self, level, label, message):
        year, month, day, _, hour, minute, second, ms = machine.RTC().datetime()
        time = "%d-%02d-%02d %02d:%02d:%02d:%03d" % (year, month, day, hour, minute, second, ms)
        ms = utime.ticks_ms()
        uptime = "%d.%03d" % (ms / 1000, ms % 1000)
        self._publishDevice('log', '{"level":%d,"time":"%s","uptime":"%s","label":"%s","message":"%s"}' % (level, time, uptime, label, message))
