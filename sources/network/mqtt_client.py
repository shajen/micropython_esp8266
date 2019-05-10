import config
import machine
import ujson
import umqtt.simple
import utime
import utils

__MAX_CONNECT_PROBES = 5

class MqttClient():
    def __init__(self):
        utils.printInfo('MQTT', 'init', False)
        self._controllers = []
        self._id = 'esp8266_%s' % utils.chipId()
        utils.printInfo('MQTT', 'client id: %s' % (self._id), False)
        self.client = umqtt.simple.MQTTClient(self._id, config.MQTT_SERVER, port=config.MQTT_PORT, user=config.MQTT_USER, password=config.MQTT_PASSWORD)
        self.client.set_callback(lambda t, m: self._receiveData(t, m))
        self._connect()

    def _connect(self):
        for i in range(0, __MAX_CONNECT_PROBES):
            try:
                self.client.connect()
                self.client.subscribe('/device/%s/query/#' % self._id)
                self.client.subscribe('/devices/query/#')
            except OSError as e:
                utils.printWarn('MQTT', 'exception during connection: %s' % e, False)
            finally:
                utils.printInfo('MQTT', 'connection successful', False)
                break

    def _publish(self, topic, data):
        topic = "/device/%s/%s" % (self._id, topic)
        message = ujson.dumps(data)
        try:
            try:
                self.client.publish(topic, message)
            except OSError as e:
                self._connect()
                self.client.publish(topic, message)
        except OSError as e:
            utils.printWarn('MQTT', 'exception during publish: %s' % e, False)

    def publishStatus(self, topic, data):
        self._publish('status/%s' % topic, data)

    def publishSensor(self, type, id, value):
        data = {"value":value}
        self._publish('sensor/%s/%s' % (type, id), data)

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
        self._publish('log', data)

    def publishEvent(self, type, message):
        data = {'message':message}
        self._publish('event/%s' % type, data)

    def _receiveData(self, topic, message):
        topic = topic.decode('utf-8').lower()
        message = message.decode('utf-8').lower()
        utils.printDebug('MQTT', 'received new message', False)
        utils.printDebug('MQTT', 'topic: %s' % topic, False)
        utils.printDebug('MQTT', 'message: %s' % message, False)

        if not topic.endswith('/'):
            topic = topic + '/'
        if not topic.startswith('/'):
            topic = '/' + topic

        if topic.startswith('/devices/query/'):
            command = topic[14:]
        elif topic.startswith('/device/%s/query/' % self._id):
            command = topic[(14 + len(self._id)):]
        else:
            return

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
