from time import sleep
from gpiozero import DigitalInputDevice
from signal import pause

sensor = DigitalInputDevice(17)

try:
	while(True):
		
		if sensor.value == 0:
			print("Sensor is activated")
		else: 
			print("Sensor is deactivated")	
		sleep(0.5)
except KeyboardInterrupt:
	print("Khatam hogaya BC") 





