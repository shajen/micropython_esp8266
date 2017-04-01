from machine import Pin, PWM

PWM_CLOCK = 1000
DALLAS_PIN = 0
PUMP_PIN = 2
HEATER_PIN = 14
FAN_PIN = 12

class Devices:
    def __init__(self):
        self.pumpPwm = PWM(Pin(PUMP_PIN), freq=PWM_CLOCK, duty=0)
        self.heaterPwm = PWM(Pin(HEATER_PIN), freq=PWM_CLOCK, duty=0)
        self.fanPwm = PWM(Pin(FAN_PIN), freq=PWM_CLOCK, duty=0)
        self.sound = False

    @staticmethod
    def calculateDutyToPercent(value):
        return int(round(value / 1023.0 * 100.0))

    @staticmethod
    def calculatePercentToDuty(value):
        return int(round(value / 100.0 * 1023.0))

    def getPump(self):
        return Devices.calculateDutyToPercent(self.pumpPwm.duty())

    def setPump(self, value):
        self.pumpPwm.duty(Devices.calculatePercentToDuty(value))

    def getHeater(self):
        return Devices.calculateDutyToPercent(self.heaterPwm.duty())

    def setHeater(self, value):
        self.heaterPwm.duty(Devices.calculatePercentToDuty(value))

    def getFan(self):
        return Devices.calculateDutyToPercent(self.fanPwm.duty())

    def setFan(self, value):
        self.fanPwm.duty(Devices.calculatePercentToDuty(value))

    def getSound(self):
        return self.sound

    def setSound(self, value):
        self.sound = value
