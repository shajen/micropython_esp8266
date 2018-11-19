import strip_animation
import full_smooth_transition_animation
import rainbow_animation

class AnimatorServerController():
    def __init__(self, np):
        self.animations = []
        self.animations.append(strip_animation.StripAnimation(np))
        self.animations.append(full_smooth_transition_animation.FullSmoothTransitionAnimation(np))
        self.animations.append(rainbow_animation.RainbowAnimation(np))

    def name(self):
        return 'animator'

    def tick(self):
        self.animations[2].tick()

    def process(self, url, params):
        return None
