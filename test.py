import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import datetime


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
	GPIO.setup(pin,GPIO.IN)
	#count loops until voltage across capicator reads high on GPIO
	while(GPIO.input(pin)==GPIO.LOW):
		#print "My Pin current: ", GPIO.input(pin)
		counter += 1
		#time.sleep(0.1)
	#print GPIO.input(pin)
	return Resolve_Light(counter)

def Motion_Sensing(pin):
	GPIO.setup(pin,GPIO.IN)      # Echo

	Current_State  = 0
	Previous_State = 0
	print "Waiting for PIR to settle ...", datetime.datetime.now()
	# Loop until PIR output is 0
	while GPIO.input(pin)==1:
		Current_State  = 0
	#wait 1 second before polling the pin
	time.sleep(1)
	return GPIO.input(pin)


def main():
	GPIO.setmode(GPIO.BCM)
	# Available sensors
	sensor_args = { '11': Adafruit_DHT.DHT11,
	    '22': Adafruit_DHT.DHT22,
	    '2302': Adafruit_DHT.AM2302 }


	# Try to grab a sensor reading.  Use the read_retry method which will retry up
	# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
	TEMP_SENSOR = Adafruit_DHT.DHT22
	TEMP_SENSING_PIN = '17'
	

	humidity, temperature = Adafruit_DHT.read_retry(TEMP_SENSOR, TEMP_SENSING_PIN)

	# Note that sometimes you won't get a reading and
	# the results will be null (because Linux can't
	# guarantee the timing of calls to read the sensor).
	# If this happens try again!
	if humidity is not None and temperature is not None:
		print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
	else:
		print 'Failed to get reading. Try again!'

	LIGHT_SENSING_PIN = 26
	print "My measurement of strength of light via counting of loops :",RC_Analog(LIGHT_SENSING_PIN)

	MOTION_SENSING_PIN = 13
	print "Motion level : ",Motion_Sensing(MOTION_SENSING_PIN)


if __name__ == '__main__':
	main()
