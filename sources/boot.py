import webrepl
import network
import machine

def detectSoftReboot():
	try:
		import utime
		if utime.ticks_ms() >= 1000:
			import machine
			machine.reset()
	except:
		pass

def doConnect():
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

detectSoftReboot()
print('Bolomajster - micropython')
print('Reset cause %d' % machine.reset_cause())
doConnect()
webrepl.start()
