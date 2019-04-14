import config
import machine
import utils
import vl53l0x

utils.printLog("NODEMCU", "radar boot up")

i2c = machine.I2C(scl=machine.Pin(config.I2C_SCL_PIN), sda=machine.Pin(config.I2C_SDA_PIN), freq=400000)

distanceSensor = vl53l0x.VL53L0X(i2c, 0x29)

def timeout100ms(timer):
    utils.printLog("RADAR", distanceSensor.read())

tim1 = utils.timer()
tim1.init(period=100, mode=machine.Timer.PERIODIC, callback=timeout100ms)
