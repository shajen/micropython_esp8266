D0 = 16
D1 = 5
D2 = 4
D3 = 0
D4 = 2
D5 = 14
D6 = 12
D7 = 13
D8 = 15
D9 = 3
D10 = 1

I2C_SDA_PIN = D1
I2C_SCL_PIN = D2
I2C_CLOCK = 400000

def timeToSecondsFromMidnight(hours, minutes, seconds):
    return (hours * 60 + minutes) * 60 + seconds

DALLAS_PIN = D3
PUMP_PIN = D5
PUMP_START = [timeToSecondsFromMidnight(0, 6, 45), timeToSecondsFromMidnight(0, 7, 25)]
PUMP_TIME = 10

UPLOADER_KEY = 'YOUR_API_KEY'

SERVER_PORT = 33455
REBOOT_EVERY_HOUR = True
BACKLIGHT = True
DEBUG = True
