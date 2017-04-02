from machine import Pin, I2C, Timer
import devices
import brew
import display
import server

i2c = I2C(scl=Pin(4), sda=Pin(5), freq=400000) #D2 D1

_devices = devices.Devices()
_brew = brew.Brew(_devices)
_display = display.Display(i2c, _devices)
_server = server.Server(33455, _devices, _brew)

tim1 = Timer(0)
tim1.init(period=1000, mode=Timer.PERIODIC, callback=_display.update)
tim2 = Timer(1)
tim2.init(period=1000, mode=Timer.PERIODIC, callback=_devices.update)
tim3 = Timer(2)
tim3.init(period=60000, mode=Timer.PERIODIC, callback=_devices.upload)

_server.run()
