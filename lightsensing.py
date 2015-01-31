import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

#Tested that with given configuration, it is between 70 (bright) to 175 (dark)

def Resolve_Light(score):
    LOWEST = 70     #brightest
    HIGHEST = 175   #darkest
    score = (score - LOWEST) / float(HIGHEST - LOWEST)
    return score

def RC_Analog(pin):
	counter = 0
	
	#Discharge capicator, set output to low
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin,GPIO.LOW)

	time.sleep(1)
	print "Complete discharging of capacitance\n"
	GPIO.setup(pin,GPIO.IN)
	#count loops until voltage across capicator reads high on GPIO
	while(GPIO.input(pin)==GPIO.LOW):
		#print "My Pin current: ", GPIO.input(pin)
		counter += 1
		#time.sleep(0.1)
	print GPIO.input(pin)
	return Resolve_Light(counter)


LIGHT_SENSING_PIN = 26
#GPIO.setup(LIGHT_SENSING_PIN,GPIO.IN)
try:
	while True:
		print "My measurement of strength of light via counting of loops :",RC_Analog(LIGHT_SENSING_PIN)
		#time.sleep(10)
except KeyboardInterrupt:
	print "Quit"
finally:
	GPIO.cleanup()

