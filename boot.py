import webrepl
import network

def do_connect():
	sta_if = network.WLAN(network.STA_IF)
	ap_if = network.WLAN(network.AP_IF)
	if ap_if.active():
		ap_if.active(False)
	if not sta_if.isconnected():
		print('Connecting to network...')
		sta_if.active(True)
		sta_if.connect("SSID", "PASSWORD")
		while not sta_if.isconnected():
			pass
		print('Connected')
	print('Network configuration:', sta_if.ifconfig())

print('Bolomajster - micropython')
do_connect()
webrepl.start()
