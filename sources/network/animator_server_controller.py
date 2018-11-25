import full_smooth_transition_animation
import rainbow_animation
import strip_animation
import ubinascii
import ujson
import uos
import utils
import utime
import ure

_MAX_SPEED = 100
_MAX_LEDS = 180
_CONFIG_FILE = "animator.data"

class AnimatorServerController():
    def __init__(self, np):
        self.np = np
        self.resetConfig()
        self.config = utils.readJson(_CONFIG_FILE) or self.config
        self.np.n = self.config['leds']
        self.powerOffIfNeeded()
        self.animations = []
        self.animations.append(rainbow_animation.RainbowAnimation(np))
        self.animations.append(strip_animation.StripAnimation(np))
        self.animations.append(full_smooth_transition_animation.FullSmoothTransitionAnimation(np))
        self.tickCount = 0
        self.lastChangedAnimation = utime.ticks_ms()
        self.forceRefreshColor = True

    def name(self):
        return 'animator'

    def tick(self):
        if self.config['powered_on'] == 0:
            return

        if self.forceRefreshColor and self.config['use_color']:
            self.forceRefreshColor = False
            bytes = ubinascii.unhexlify(self.config['color'])
            color = [bytes[1], bytes[0], bytes[2]]
            self.np.buf = bytearray(color * self.np.n)
            self.np.write()
            return

        if self.config['use_color']:
            return

        if utime.ticks_ms() - self.lastChangedAnimation > self.config['seconds_per_animation'] * 1000 and self.config['animation'] == -1:
            self.config['current_animation'] = (self.config['current_animation'] + 1) % len(self.animations)
            self.lastChangedAnimation = utime.ticks_ms()

        if self.tickCount % (_MAX_SPEED - self.config['speed'] + 1) == 0:
            self.animations[self.config['current_animation']].tick()

        self.tickCount = (self.tickCount + 1) % _MAX_SPEED

    def process(self, url, params):
        if url == '/ANIMATOR/':
            return ujson.dumps(self.config)
        elif url == '/ANIMATOR/SET/' and "KEY" in params and "VALUE" in params:
            key = params['KEY']
            try:
                value = int(params['VALUE'])
            except:
                pass
            if key == 'SPEED' and value in range(1, _MAX_SPEED + 1):
                self.config['speed'] = value
            elif key == 'ANIMATION' and value in range(-1, len(self.animations)):
                self.config['animation'] = value
                if value == -1:
                    self.config['current_animation'] = uos.urandom(1)[0] % len(self.animations)
                else:
                    self.config['current_animation'] = value
            elif key == 'LEDS' and 2 <= value and value <= _MAX_LEDS:
                self.config['leds'] = value
                self.np.n = value
            elif key == 'SECONDS_PER_ANIMATION' and value > 0:
                self.config['seconds_per_animation'] = value
            elif key == 'POWERED_ON' and (value == 0 or value == 1):
                self.config['powered_on'] = value
                self.powerOffIfNeeded()
            elif key == 'USE_COLOR' and (value == 0 or value == 1):
                self.config['use_color'] = value
                self.forceRefreshColor = True
            elif key == 'COLOR' and ure.match("^[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]$", params['VALUE']):
                self.config['color'] = params['VALUE']
                self.forceRefreshColor = True
            utils.writeJson(_CONFIG_FILE, self.config)
            return ujson.dumps(self.config)
        elif url == '/ANIMATOR/RESET/':
            self.resetConfig()
            utils.writeJson(_CONFIG_FILE, self.config)
            return ujson.dumps(self.config)
        return None

    def resetConfig(self):
        SPEED = _MAX_SPEED - 10
        self.config = {
            'powered_on' : 1,
            'speed' : SPEED,
            'animation' : -1,
            'leds' : self.np.n,
            'current_animation' : 0,
            'seconds_per_animation' : 60,
            'use_color' : 1,
            'color' : 'FFFFFF'
        }

    def powerOffIfNeeded(self):
        if self.config['powered_on'] == 0:
            self.np.buf = bytearray([0] * (self.np.n * 3))
            self.np.write()
