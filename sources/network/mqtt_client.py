import config
import machine
import ubinascii
import ujson
import umqtt.simple
import utime
import utils

__MAX_CONNECT_PROBES = 5

class MqttClient():
    def __init__(self):
        self._controllers = []
        id = machine.unique_id()
        self._id = 'esp8266_%2X%2X%2X' % (id[2], id[1], id[0])
        self.client = umqtt.simple.MQTTClient(self._id, config.MQTT_SERVER, port=config.MQTT_PORT, user=config.MQTT_USER, password=config.MQTT_PASSWORD)
        self.client.set_callback(lambda t, m: self._receiveData(t, m))
        self._connect()
        self.publishDevice('hello', '')

    def _connect(self):
        for i in range(0, __MAX_CONNECT_PROBES):
            try:
                self.client.connect()
                self.client.subscribe('/device/%s/api/#' % self._id)
                self.client.subscribe('/devices/api/#')
            except OSError as e:
                utils.printWarn('MQTT', 'exception during connection: %s' % e, False)
            finally:
                utils.printInfo('MQTT', 'connection successful', False)
                break

    def _publish(self, topic, data):
        message = ujson.dumps(data)
        try:
            try:
                self.client.publish(topic, message)
            except OSError as e:
                self._connect()
                self.client.publish(topic, message)
        except OSError as e:
            utils.printWarn('MQTT', 'exception during publish: %s' % e, False)

    def publishDevice(self, topic, data):
        self._publish("/device/%s/%s" % (self._id, topic), data)

    def _publishSensor(self, type, id, value):
        data = {"value":value}
        self.publishDevice('sensor/%s/%s' % (type, id), data)

    def publishTemperature(self, id, value):
        self._publishSensor('temperature', id, value)

    def publishLog(self, level, label, message):
        year, month, day, _, hour, minute, second, ms = machine.RTC().datetime()
        time = "%d-%02d-%02d %02d:%02d:%02d:%03d" % (year, month, day, hour, minute, second, ms)
        ms = utime.ticks_ms()
        uptime = "%d.%03d" % (ms / 1000, ms % 1000)
        data = {
            "level":level,
            "time":time,
            "uptime":uptime,
            "label":label,
            "message":message,
        }
        self.publishDevice('log', data)

    def publishEvent(self, type, message):
        data = {
            'message':message
        }
        self.publishDevice('event/%s' % type, data)

    def _receiveData(self, topic, message):
        topic = topic.decode('utf-8')
        message = message.decode('utf-8')
        if topic.startswith('/devices/api/'):
            command = topic[12:]
        elif topic.startswith('/device/%s/api/' % self._id):
            command = topic[(12 + len(self._id)):]
        else:
            return

        if not command.endswith('/'):
            command = command + '/'

        try:
            data = ujson.loads(message)
        except Exception as e:
            utils.printWarn('MQTT', 'exception during json loads: %s' % e, False)
            data = message
        for c in self._controllers:
            c.process(command, data)

    def setControllers(self, controllers):
        self._controllers = controllers

    def run(self):
        while True:
            try:
                self.client.wait_msg()
            except OSError as e:
                self._connect()
