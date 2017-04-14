from config import I2C_SCL_PIN, I2C_SDA_PIN, I2C_CLOCK
from machine import Pin, I2C, Timer
from helper import syncDatetime, printDebug
import devices
import brew
import display
import server

syncDatetime()
i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_CLOCK)

_devices = devices.Devices()
_brew = brew.Brew(_devices)
_display = display.Display(i2c, _devices)
_server = server.Server(33455, _devices, _brew, _display)

def update(timer):
    printDebug("UPDATE", "start")
    _display.update()
    _devices.update()
    printDebug("UPDATE", "finish")

tim1 = Timer(0)
tim1.init(period=1000, mode=Timer.PERIODIC, callback=update)
tim2 = Timer(1)
tim2.init(period=60000, mode=Timer.PERIODIC, callback=lambda t: _devices.upload())

_server.run()
