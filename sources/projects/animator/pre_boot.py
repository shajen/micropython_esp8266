import config
import esp
import machine
import utils
import ubinascii

utils.printInfo('ANIMATOR', 'fast set leds')
_config = utils.readJson('animator.data')
if _config and _config['powered_on'] and _config['use_color']:
    pin = machine.Pin(config.ANIMATOR_PIN, machine.Pin.OUT)
    bytes = ubinascii.unhexlify(_config['color'])
    color = [bytes[1], bytes[0], bytes[2]]
    esp.neopixel_write(pin, bytearray(color * _config['leds']), 1)
utils.printInfo('ANIMATOR', 'finish')
