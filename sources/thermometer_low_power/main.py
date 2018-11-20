import utils
import devices
import machine

utils.printLog("NODEMCU", "thermometer low power boot up")

_devices = devices.Devices()
_devices.update()
_devices.upload()

rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
rtc.alarm(rtc.ALARM0, 60000)

machine.deepsleep()
