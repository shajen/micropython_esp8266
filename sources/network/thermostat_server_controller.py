import machine
import utils

_CONFIG_FILE = "thermostat.data"
_UPDATE_INTERVAL_MS = 1000

class ThermostatServerController():
    def __init__(self, mqttClient, temperature_sensor, relay_pin, switch_pin, led_pin):
        utils.printInfo('THERMOSTAT', 'init')
        self._mqttClient = mqttClient
        self._temperature_sensor = temperature_sensor
        self._relay_pin = relay_pin
        self._led_pin = led_pin
        self._config = utils.readJson(_CONFIG_FILE) or self._default_config()
        self._update()
        self._timer = utils.timer()
        self._timer.init(period=_UPDATE_INTERVAL_MS, mode=machine.Timer.PERIODIC, callback=lambda t: self._update())
        switch_pin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=lambda p: self._switch_clicked(p))
        utils.printInfo('THERMOSTAT', 'config:\n%s' % (self._config))

    def process(self, command, data):
        if command == '/thermostat/state/':
            self._mqttClient.publishStatus('thermostat/state', self._get_state())
        elif command == '/thermostat/set/':
            try:
                if 'is_heater' in data:
                    self._config['is_heater'] = data['is_heater']
                if 'desired_temperature' in data:
                    desired_temperature = data['desired_temperature']
                    if 0.0 <= desired_temperature and desired_temperature <= 100.0:
                        self._config['desired_temperature'] = desired_temperature
                if 'hysteresis' in data:
                    hysteresis = data['hysteresis']
                    if 0.1 <= hysteresis and hysteresis <= 5.0:
                        self._config['hysteresis'] = hysteresis
            except Exception as e:
                utils.printWarn('THERMOSTAT', 'exception during process')
                utils.printWarn('THERMOSTAT', e)
            utils.writeJson(_CONFIG_FILE, self._config)
            self._mqttClient.publishEvent('thermostat/state', 'New state has been set.')
            self._mqttClient.publishStatus('thermostat/state', self._get_state())

    def _switch_clicked(self, pin):
        self._config['switch_force_working_mode'] = (pin.value() + 1) % 2
        self._update()

    def _update_working_mode(self):
        utils.printDebug('THERMOSTAT', 'working_mode %d' % self._config['working_mode'])
        utils.printDebug('THERMOSTAT', 'switch_force_working_mode %d' % self._config['switch_force_working_mode'])
        working_mode = self._config['working_mode'] or self._config['switch_force_working_mode']
        utils.printDebug('THERMOSTAT', 'calucalated working_mode %d' % working_mode)
        self._relay_pin.value(working_mode)
        self._led_pin.value((working_mode + 1) % 2)

    def _get_state(self):
        try:
            temperature = self._temperature_sensor.getAverageExternalTemperature()
        except:
            temperature = 0.0

        data = self._config
        data['current_temperature'] = temperature
        data['is_working'] = self._relay_pin.value()
        return data

    def _default_config(self):
        return {
            'is_heater': False,
            'desired_temperature': 17.0,
            'hysteresis': 0.5,
            'working_mode': 0,
            'switch_force_working_mode': 0,
        }

    def _update(self):
        try:
            temperature = self._temperature_sensor.getAverageExternalTemperature()
            desired_temperature = self._config['desired_temperature']
            hysteresis = self._config['hysteresis']
            if self._config['is_heater']:
                if temperature >= desired_temperature + hysteresis:
                    self._config['working_mode'] = 0
                elif temperature <= desired_temperature - hysteresis:
                    self._config['working_mode'] = 1
            else:
                if temperature >= desired_temperature + hysteresis:
                    self._config['working_mode'] = 1
                elif temperature <= desired_temperature - hysteresis:
                    self._config['working_mode'] = 0
        except Exception as e:
            utils.printWarn('THERMOSTAT', 'exception during update')
            utils.printWarn('THERMOSTAT', e)
        self._update_working_mode()
