from config import I2C_SCL_PIN, I2C_SDA_PIN, I2C_CLOCK
from machine import Pin, I2C, Timer
from machine import Timer
from utils import syncDatetime, printDebug, printLog
import devices
import display
import server
import status_server_controller
import utime

printLog("NODEMCU", "boot up")

i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_CLOCK)

_devices = devices.Devices()
_display = display.Display(i2c, _devices)

def timeout1second(timer):
    _devices.update()
    hour = utime.localtime(utime.time())[3]
    _display.setBacklight(7 <= hour and hour <= 22)
    _display.update()

def timeout1minute(timer):
    _devices.upload()

def timeout10minutes(timer):
    syncDatetime()

timeout1minute(None)
timeout10minutes(None)

tim1 = Timer(0)
tim1.init(period=1000, mode=Timer.PERIODIC, callback=timeout1second)
tim2 = Timer(1)
tim2.init(period=60000, mode=Timer.PERIODIC, callback=timeout1minute)
tim3 = Timer(2)
tim3.init(period=600000, mode=Timer.PERIODIC, callback=timeout10minutes)

statusController = status_server_controller.StatusServerController()
_server = server.Server(33455, [statusController])
_server.run()
