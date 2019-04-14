import config
import temperature_sensor
import machine
import pin_scheduler
import server
import status_server_controller
import utils

utils.printLog("PIN_SCHEDULER", "boot up")
_temperature_sensor = temperature_sensor.TemperatureSensor(machine.Pin(config.D3))
pinScheduler = pin_scheduler.PinScheduler(machine.Pin(config.D5, machine.Pin.OUT), [((19, 0, 0), 36)])
statusController = status_server_controller.StatusServerController('Pin Scheduler', [])
_server = server.Server(config.SERVER_PORT, [statusController])

try:
    _server.run()
except KeyboardInterrupt:
    utils.printLog("PIN_SCHEDULER", "stopped by the user")
    utils.deleteTimers()
except Exception as e:
    utils.printLog("PIN_SCHEDULER", "exception during server run: %s" % e)
    machine.reboot()
