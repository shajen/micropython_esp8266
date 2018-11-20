import full_smooth_transition_animation
import rainbow_animation
import strip_animation
import ujson
import uos
import utime

MAX_SPEED = 100

class AnimatorServerController():
    def __init__(self, np):
        self.np = np
        self.animations = []
        self.animations.append(rainbow_animation.RainbowAnimation(np))
        self.animations.append(strip_animation.StripAnimation(np))
        self.animations.append(full_smooth_transition_animation.FullSmoothTransitionAnimation(np))
        self.config = {'speed' : MAX_SPEED, 'animation' : -1, 'leds' : self.np.n, 'currentAnimation' : 0, 'secondsPerAnimation' : 60}
        self.tickCount = 0
        self.lastChangedAnimation = utime.ticks_ms()

    def name(self):
        return 'animator'

    def tick(self):
        if utime.ticks_ms() - self.lastChangedAnimation > self.config['secondsPerAnimation'] * 1000 and self.config['animation'] == -1:
            self.config['currentAnimation'] = (self.config['currentAnimation'] + 1) % len(self.animations)
            self.lastChangedAnimation = utime.ticks_ms()

        if self.tickCount % (MAX_SPEED - self.config['speed'] + 1) == 0:
            self.animations[self.config['currentAnimation']].tick()

        self.tickCount = (self.tickCount + 1) % MAX_SPEED

    def process(self, url, params):
        if url == '/ANIMATOR/':
            return ujson.dumps(self.config)
        elif url == '/ANIMATOR/SET/' and "KEY" in params and "VALUE" in params:
            key = params['KEY']
            value = int(params['VALUE'])
            if key == 'SPEED' and value in range(1, MAX_SPEED + 1):
                self.config['speed'] = value
            elif key == 'ANIMATION' and value in range(-1, len(self.animations)):
                self.config['animation'] = value
                if value == -1:
                    self.config['currentAnimation'] = uos.urandom(1)[0] % len(self.animations)
                else:
                    self.config['currentAnimation'] = value
            elif key == 'LEDS' and value > 0:
                self.config['leds'] = value
                self.np.n = value
            elif key == 'SECONDS_PER_ANIMATION' and value > 0:
                self.config['secondsPerAnimation'] = value
            return ujson.dumps(self.config)
        return None
