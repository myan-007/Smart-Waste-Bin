from gpiozero import AngularServo
from time import sleep

servo1 = AngularServo(17 ,min_pulse_width=0.00075, max_pulse_width=0.00225)
servo2 = AngularServo(18,min_pulse_width=0.00075, max_pulse_width=0.00225)


while(True):
	i = 0
	while i <= 1000:
	 i = i+1
	 print("OK")
	 sleep(30)
	servo1.angle = 0
	servo2.angle = 0
	sleep(2)
	servo1.angle = 45
	servo2.angle = 0
	sleep(2)
	servo2.angle = 45
	sleep(2)
	servo1.angle = 0
	servo2.angle = 0

	
while(True):
	servo1.angle = 0
	servo2.angle = 0
	sleep(2)
	servo1.angle = 45
	sleep(2)
	servo1.angle = -45
	sleep(2)
	servo2.angle = -45
	sleep(2)
	servo2.angle = 0
	sleep(2)
	servo1.angle = 0

'''
while(True):
	servo2.angle = 0
	sleep(2)
	servo2.angle = -25
	sleep(2)'''
