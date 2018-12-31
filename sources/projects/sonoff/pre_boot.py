import machine
import sonoff_server_controller

### GPIO SONOFF SWITCH ###
# 0 - switch
# 12 - relay
# 13 - led

### GPIO SONOFF TOUCH###
# 0 - left switch
# 4 - buzzer
# 5 - right led and relay
# 9 - right switch
# 12 - left led and relay
# 13 - top led

relayPin1 = machine.Pin(12, machine.Pin.OUT)
switchPin1 = machine.Pin(0, machine.Pin.IN)

relayPin2 = machine.Pin(5, machine.Pin.OUT)
switchPin2 = machine.Pin(9, machine.Pin.IN)

switch1 = (relayPin1, None, switchPin1)
switch2 = (relayPin2, None, switchPin2)

sonoff_server_controller.initInstance([switch1, switch2])
