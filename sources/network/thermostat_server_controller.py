import machine
import ujson
import utils

_CONFIG_FILE = "thermostat.data"
_UPDATE_INTERVAL_MS = 1000

class ThermostatServerController():
    def __init__(self, temperature_sensor, relay_pin, switch_pin, led_pin):
        utils.printLog('THERMOSTAT', 'init')
        self._temperature_sensor = temperature_sensor
        self._relay_pin = relay_pin
        self._led_pin = led_pin
        self._config = utils.readJson(_CONFIG_FILE) or self._default_config()
        self._update()
        self._timer = utils.timer()
        self._timer.init(period=_UPDATE_INTERVAL_MS, mode=machine.Timer.PERIODIC, callback=lambda t: self._update())
        switch_pin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=lambda p: self._switch_clicked(p))
        utils.printLog('THERMOSTAT', 'config:\n%s' % (self._config))

    def __del__(self):
        utils.printLog('THERMOSTAT', 'delete')
        self._timer.deinit()

    def name(self):
        return 'thermostat'

    def process(self, url, params):
        if url == '/THERMOSTAT/':
            return self._get_state()
        elif url == '/THERMOSTAT/SET/':
            try:
                if 'IS_HEATER' in params:
                    self._config['is_heater'] = utils.str2bool(params['IS_HEATER'])
                if 'DESIRED_TEMPERATURE' in params:
                    desired_temperature = utils.str2float(params['DESIRED_TEMPERATURE'])
                    if 0.0 <= desired_temperature and desired_temperature <= 100.0:
                        self._config['desired_temperature'] = desired_temperature
                if 'HYSTERESIS' in params:
                    hysteresis = utils.str2float(params['HYSTERESIS'])
                    if 0.1 <= hysteresis and hysteresis <= 5.0:
                        self._config['hysteresis'] = hysteresis
            except Exception as e:
                utils.printLog('THERMOSTAT', 'exception during process')
                utils.printLog('THERMOSTAT', e)
            utils.writeJson(_CONFIG_FILE, self._config)
            return self._get_state()
        return None

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
        return ujson.dumps({'status': 0, 'data' : data})

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
            utils.printLog('THERMOSTAT', 'exception during update')
            utils.printLog('THERMOSTAT', e)
        self._update_working_mode()
