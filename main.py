import server
import devices
import brew
import machine

_devices = devices.Devices()
_brew = brew.Brew(_devices)
_server = server.Server(33455, _devices, _brew)
_server.run()
