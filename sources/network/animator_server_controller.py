import esp
import full_smooth_transition_animation
import machine
import rainbow_animation
import strip_animation
import ubinascii
import ujson
import uos
import ure
import utils
import utime

_MAX_SPEED = 100
_MAX_LEDS = 180
_CONFIG_FILE = "animator.data"

class AnimatorServerController():
    def __init__(self, mqttClient, pin):
        self._mqttClient = mqttClient
        self.pin = pin
        self.resetConfig()
        self.config = utils.readJson(_CONFIG_FILE) or self.config
        self.powerOffIfNeeded()
        self.animations = []
        self.animations.append(rainbow_animation.RainbowAnimation(pin, self.config['leds']))
        self.animations.append(strip_animation.StripAnimation(pin, self.config['leds']))
        self.animations.append(full_smooth_transition_animation.FullSmoothTransitionAnimation(pin, self.config['leds']))
        self.tickCount = 0
        self.lastChangedAnimation = utime.ticks_ms()
        self.forceRefreshColor = True
        self.forceRefreshLeds = 0
        self.timer = utils.timer()
        self.timer.init(period=1, mode=machine.Timer.PERIODIC, callback=lambda t: self.tick())

    def tick(self):
        if self.config['powered_on'] == 0:
            return

        if self.forceRefreshColor and self.config['use_color']:
            self.forceRefreshColor = False
            bytes = ubinascii.unhexlify(self.config['color'])
            color = [bytes[1], bytes[0], bytes[2]]
            esp.neopixel_write(self.pin, bytearray(color * self.config['leds']), 1)
            return
        self.forceRefreshColor = False

        if self.forceRefreshLeds != 0:
            esp.neopixel_write(self.pin, bytearray([0] * 3 * self.forceRefreshLeds), 1)
            for animation in self.animations:
                animation.setup(self.config['leds'])
            self.forceRefreshLeds = 0

        if self.config['use_color']:
            return

        if utime.ticks_ms() - self.lastChangedAnimation > self.config['seconds_per_animation'] * 1000 and self.config['animation'] == -1:
            self.config['current_animation'] = (self.config['current_animation'] + 1) % len(self.animations)
            self.lastChangedAnimation = utime.ticks_ms()

        if self.tickCount % (_MAX_SPEED - self.config['speed'] + 1) == 0:
            self.animations[self.config['current_animation']].tick()

        self.tickCount = (self.tickCount + 1) % _MAX_SPEED

    def process(self, command, data):
        if command == '/animator/state/':
            self._mqttClient.publishStatus('animator/state', self.config)
        elif command == '/animator/set/':
            self.setValue(data)
            utils.writeJson(_CONFIG_FILE, self.config)
            self._mqttClient.publishEvent('animator/state', 'New state has been set.')
            self._mqttClient.publishStatus('animator/state', self.config)
        elif command == '/animator/reset/':
            self.resetConfig()
            utils.writeJson(_CONFIG_FILE, self.config)
            self._mqttClient.publishEvent('animator/state', 'New state has been set.')
            self._mqttClient.publishStatus('animator/state', self.config)

    def setValue(self, data):
        if 'speed' in data and data['speed'] in range(1, _MAX_SPEED + 1):
            self.config['speed'] = data['speed']
        elif 'animation' in data and data['animation'] in range(-1, len(self.animations)):
            self.config['animation'] = data['animation']
            if data['animation'] == -1:
                self.config['current_animation'] = uos.urandom(1)[0] % len(self.animations)
            else:
                self.config['current_animation'] = data['animation']
        elif 'leds' in data and 2 <= data['leds'] and data['leds'] <= _MAX_LEDS and self.config['leds'] != data['leds']:
            tmp = self.config['leds']
            self.config['leds'] = data['leds']
            self.forceRefreshLeds = tmp
        elif 'seconds_per_animation' in data and data['seconds_per_animation'] > 0:
            self.config['seconds_per_animation'] = data['seconds_per_animation']
        elif 'powered_on' in data and (data['powered_on'] == 0 or data['powered_on'] == 1):
            self.config['powered_on'] = data['powered_on']
            self.forceRefreshColor = True
            self.powerOffIfNeeded()
        elif 'use_color' in data and (data['use_color'] == 0 or data['use_color'] == 1):
            self.config['use_color'] = data['use_color']
            self.forceRefreshColor = True
        elif 'color' in data and ure.match("^[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]$", data['color']):
            self.config['color'] = data['color']
            self.forceRefreshColor = True

    def resetConfig(self):
        SPEED = _MAX_SPEED - 10
        self.config = {
            'powered_on' : 1,
            'speed' : SPEED,
            'animation' : -1,
            'leds' : 60,
            'current_animation' : 0,
            'seconds_per_animation' : 60,
            'use_color' : 1,
            'color' : 'FFFFFF'
        }

    def powerOffIfNeeded(self):
        if self.config['powered_on'] == 0:
            esp.neopixel_write(self.pin, bytearray([0] * 3 * self.config['leds']), 1)
