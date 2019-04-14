import config
import machine
import sonoff_server_controller

relayPin1 = machine.Pin(config.SONOFF_RELAY1_PIN, machine.Pin.OUT)
switchPin1 = machine.Pin(config.SONOFF_SWITCH1_PIN, machine.Pin.IN)

relayPin2 = machine.Pin(config.SONOFF_RELAY2_PIN, machine.Pin.OUT)
switchPin2 = machine.Pin(config.SONOFF_SWITCH2_PIN, machine.Pin.IN)

switch1 = (relayPin1, None, switchPin1)
switch2 = (relayPin2, None, switchPin2)

sonoff_server_controller.initInstance([switch1, switch2])
