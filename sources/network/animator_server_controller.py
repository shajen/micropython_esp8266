import full_smooth_transition_animation
import rainbow_animation
import strip_animation
import ujson
import uos
import utils
import utime

_MAX_SPEED = 100
_MAX_LEDS = 180
_CONFIG_FILE = "animator.data"

class AnimatorServerController():
    def __init__(self, np):
        self.np = np
        self.np.buf = bytearray([0] * (_MAX_LEDS * 3))
        self.np.write()
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

    def name(self):
        return 'animator'

    def tick(self):
        if self.config['powered_on'] == 0:
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
            value = int(params['VALUE'])
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
            utils.writeJson(_CONFIG_FILE, self.config)
            return ujson.dumps(self.config)
        elif url == '/ANIMATOR/RESET/':
            self.resetConfig()
            utils.writeJson(_CONFIG_FILE, self.config)
            return ujson.dumps(self.config)
        return None

    def resetConfig(self):
        SPEED = _MAX_SPEED - 10
        self.config = {'powered_on' : 1, 'speed' : SPEED, 'animation' : -1, 'leds' : self.np.n, 'current_animation' : 0, 'seconds_per_animation' : 60}

    def powerOffIfNeeded(self):
        if self.config['powered_on'] == 0:
            self.np.buf = bytearray([0] * (self.np.n * 3))
            self.np.write()
