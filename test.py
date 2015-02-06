import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import datetime
import requests
import json
from Adafruit_CharLCD import Adafruit_CharLCD
import bluetooth

def LoginUser(USERNAME,PASSWORD):
	url = 'https://api.parse.com/1/login'

	headers = {'content-type':'application/json',
	    'X-Parse-Application-Id': 'OW1IJfhxLt0wIJ5WTowtvDv9suPyMaWMA3BtYG1F',
	    'X-Parse-REST-API-Key': 'vTJjmpVQGM43RdUhTCXv0aOAbQ3sNm8RkyOmc7kh'}	

	payload = {"username":USERNAME,"password":PASSWORD}
	r = requests.get(url,params=payload, headers=headers)
	r = json.loads(r.text)
	return r['sessionToken'], r['objectId']


def CheckIgloosenseStatus(SENSOR_ID,SESSION_TOKEN,MY_LCD):

	url = 'https://api.parse.com/1/Igloosense/' + SENSOR_ID

	headers = {'content-type':'application/json',
	    'X-Parse-Application-Id': 'OW1IJfhxLt0wIJ5WTowtvDv9suPyMaWMA3BtYG1F',
	    'X-Parse-REST-API-Key': 'vTJjmpVQGM43RdUhTCXv0aOAbQ3sNm8RkyOmc7kh',
	    'X-Parse-Session-Token': SESSION_TOKEN }


	messageChange = False
	try:
		r = requests.get(url, headers=headers)
		#print r.text
		r = json.loads(r.text)
		messageChange = r['messageChange']
		#print messageChange
		if messageChange:
			myMessage = r['message']
			#print myMessage
			MY_LCD.clear()
			MY_LCD.message(myMessage)
			data = {'messageChange':False}
			g = requests.put(url,data=json.dumps(data),headers=headers)
			#print g
			#print g.text


	except Exception,e:
		print "Failed connecting with error at status check: ",e
	return messageChange




def ResolveLight(score):
    LOWEST = 70     #brightest
    HIGHEST = 175   #darkest
    score = (score - LOWEST) / float(HIGHEST - LOWEST)
    return score

def RcAnalog(pin):
	try:
		counter = 0
		
		#Discharge capicator, set output to low
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin,GPIO.LOW)
		time.sleep(1)
		GPIO.setup(pin,GPIO.IN)
		#count loops until voltage across capicator reads high on GPIO
		while(GPIO.input(pin)==GPIO.LOW and counter<200):
			#print "My Pin current: ", GPIO.input(pin)
			counter += 1
			#time.sleep(0.1)
		#print GPIO.input(pin)
		return 1 - ResolveLight(counter)
	except Exception,e:
		print "Error with light sensing with error : ",e
		return 0

def MotionSensing(pin):
	try:
		GPIO.setup(pin,GPIO.IN)      # Echo
		#print "Waiting for PIR to settle ...", datetime.datetime.now()
		# Loop until PIR output is 0
		current_state = GPIO.input(pin)
		#wait 3 second before polling the pin to get results
		time.sleep(3)
		return GPIO.input(pin)
	except Exception,e:
		print "Error with motion sensing with error : ", e
		return 0

def BluetoothDiscovery():
	try:
		nearby_devices = bluetooth.discover_devices(lookup_names = True)
		#for addr, name in nearby_devices:
		#	print("  %s - %s" % (addr, name))
		return nearby_devices
	except Exception,e:
		print "Error with bluetooth discovery with error : ", e
		return None



def SendDataToParse(data,USER_ID,SESSION_TOKEN,SENSOR_ID):
	url = 'https://api.parse.com/1/classes/IgloosenseData'

	payload = {'temperature':data['temperature'],
		'motion':data['motion'],
		'brightness':data['brightness'],
		'humidity':data['humidity'],
		'numBluetoothDevicesDetected':data['numBluetoothDevicesDetected'],
		'bluetoothDevicesDetected':data['bluetoothDevicesDetected'],
		'ACL':{USER_ID:{'write':True,'read':True}},
		'igloosense':{"__type":"Pointer","className":"Igloosense","objectId":SENSOR_ID}}		#sets the access control list to restrict access

	headers = {'content-type':'application/json',
	    'X-Parse-Application-Id': 'OW1IJfhxLt0wIJ5WTowtvDv9suPyMaWMA3BtYG1F',
	    'X-Parse-REST-API-Key': 'vTJjmpVQGM43RdUhTCXv0aOAbQ3sNm8RkyOmc7kh',
	    'X-Parse-Session-Token': SESSION_TOKEN}
	try:
		r = requests.post(url, data=json.dumps(payload), headers=headers)
		#print r.text
	except Exception,e:
		print "Failed connecting with error at sending sensor data to parse: ",e

	url = 'https://api.parse.com/1/classes/Igloosense/' + SENSOR_ID

	payload = {'lastTemperature':data['temperature'],
            'lastHumidity':data['humidity'],
            'lastBrightness':data['brightness'],
            'lastMotion':data['motion'],
            'lastNumBluetoothDevicesDetected':data['numBluetoothDevicesDetected'],
            'lastBluetoothPresenceArray':data['bluetoothDevicesDetected'],
            'ACL':{USER_ID:{'write':True,'read':True}}}
	r = requests.put(url, data=json.dumps(payload), headers=headers)
	print r.text


def main(USERNAME,PASSWORD,SENSOR_ID):

	sessionToken, objectID = LoginUser(USERNAME,PASSWORD)
	messageDelayCountdown = 0
	GPIO.setmode(GPIO.BCM)

	lcd = Adafruit_CharLCD()
	lcd.clear()
	while True:
	    
		data = {'temperature':0,
				'motion':0,
				'brightness':0,
				'humidity':0,
				'numBluetoothDevicesDetected':0,
				'bluetoothDevicesDetected':[]}

		# Available sensors
		sensor_args = { '11': Adafruit_DHT.DHT11,
		    '22': Adafruit_DHT.DHT22,
		    '2302': Adafruit_DHT.AM2302}


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
			data['humidity'] = humidity
			data['temperature'] = temperature
			#print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)

			if messageDelayCountdown == 0:
				lcd.clear()
				lcd.message("Your temperature\n"+"Temp={0:0.1f}*C".format(temperature))
		else:
			#print 'Failed to get reading. Try again!'
			data['humidity'] = 0
			data['temperature'] = 0

		LIGHT_SENSING_PIN = 26
		light_strength = RcAnalog(LIGHT_SENSING_PIN)

		data['brightness'] = light_strength

		#print "My measurement of strength of light via counting of loops :", light_strength

		MOTION_SENSING_PIN = 13
		motion = MotionSensing(MOTION_SENSING_PIN)
		data['motion'] = motion
		
		#print "Performing inquiry ... "
		myDevicesDiscovered = BluetoothDiscovery()
		devices_array = []
		num_devices = 0
		#print "Devices discovered : ", myDevicesDiscovered
		if myDevicesDiscovered is not None:
			num_devices = len(myDevicesDiscovered)
			for addr, name in myDevicesDiscovered:
				devices_array.append((addr,name))


		data['numBluetoothDevicesDetected'] = num_devices
		data['bluetoothDevicesDetected'] = devices_array

		#print "Motion boolean : ", motion
		#print "Sending data to parse ... "


		SendDataToParse(data,objectID,sessionToken,SENSOR_ID)

		detectedMessageChange = CheckIgloosenseStatus(SENSOR_ID,sessionToken,lcd)
		if detectedMessageChange:
			messageDelayCountdown = 2

		if messageDelayCountdown > 0:
			messageDelayCountdown -= 1

		time.sleep(2)


if __name__ == '__main__':
	if len(sys.argv) == 1:
			USERNAME = 'igloo'
			PASSWORD = 'igloo'
			SENSOR_ID = 'elFtIHZGjA'
			main(USERNAME,PASSWORD,SENSOR_ID)
	else:
		print """---usage: python test.py once OR python test.py repeat
					once: poll all sensors once and fire to parse.
					repeat: poll all sensors in intervals of 5 seconds and fire to parse."""





