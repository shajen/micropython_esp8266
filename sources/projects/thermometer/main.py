import config
import temperature_sensor
import display
import machine
import server
import status_server_controller
import utils
import utime

utils.printLog("NODEMCU", "thermometer boot up")

i2c = machine.I2C(scl=machine.Pin(config.I2C_SCL_PIN), sda=machine.Pin(config.I2C_SDA_PIN), freq=config.I2C_CLOCK)

_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.DALLAS_PIN))
_display = display.Display(i2c, _temperature_sensor)

def timeout1second(timer):
    _temperature_sensor.update()
    hour = utime.localtime(utime.time())[3]
    _display.setBacklight(7 <= hour and hour <= 22)
    _display.update()

def timeout1minute(timer):
    _temperature_sensor.upload()

def timeout10minutes(timer):
    utils.syncDatetime()

def timeout1hours(timer):
    if config.REBOOT_EVERY_HOUR:
        machine.reset()

timeout1minute(None)
timeout10minutes(None)

tim1 = machine.Timer(0)
tim1.init(period=1000, mode=machine.Timer.PERIODIC, callback=timeout1second)
tim2 = machine.Timer(1)
tim2.init(period=60000, mode=machine.Timer.PERIODIC, callback=timeout1minute)
tim3 = machine.Timer(2)
tim3.init(period=600000, mode=machine.Timer.PERIODIC, callback=timeout10minutes)
tim4 = machine.Timer(3)
tim4.init(period=3600000, mode=machine.Timer.PERIODIC, callback=timeout1hours)

statusController = status_server_controller.StatusServerController('Thermometer', [])
_server = server.Server(config.SERVER_PORT, [statusController])
_server.run()
