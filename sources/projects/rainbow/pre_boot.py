import config
import esp
import machine
import utils

utils.printLog('ANIMATOR', 'fast set leds')
_config = utils.readJson('animator.data')
if _config:
    pin = machine.Pin(config.WS2811_PIN, machine.Pin.OUT)
    esp.neopixel_write(pin, bytearray([0xff] * _config['leds'] * 3), 1)
utils.printLog('ANIMATOR', 'finish')
