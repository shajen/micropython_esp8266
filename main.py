from machine import Pin, I2C, Timer
import devices
import brew
import display
import server

i2c = I2C(scl=Pin(4), sda=Pin(5), freq=400000)

_display = display.Display(i2c)
_devices = devices.Devices()
_brew = brew.Brew(_devices)
_server = server.Server(33455, _devices, _brew)

tim = Timer(-1)
tim.init(period=1000, mode=Timer.PERIODIC, callback=_display.update)

_server.run()
