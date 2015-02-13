from Pubnub import Pubnub
import requests
import sys
import time
import json

def LoginUser(USERNAME,PASSWORD):
	"""
		Function takes in username and password and returns the session token and object id
		Retries to login again if error
	"""
	sessionToken = None
	objectId = None

	while (sessionToken == None and objectId == None):
		print "Logging in ..."
		url = 'https://api.parse.com/1/login'

		headers = {'content-type':'application/json',
		    'X-Parse-Application-Id': 'OW1IJfhxLt0wIJ5WTowtvDv9suPyMaWMA3BtYG1F',
		    'X-Parse-REST-API-Key': 'vTJjmpVQGM43RdUhTCXv0aOAbQ3sNm8RkyOmc7kh'}	

		payload = {"username":USERNAME,"password":PASSWORD}
		try:
			r = requests.get(url,params=payload, headers=headers)
			r = json.loads(r.text)
			sessionToken = r['sessionToken']
			objectId = r['objectId']
			
		except Exception,e:
			print "Failed logging in with error : ", e
			time.sleep(2)

	return sessionToken, objectId


def SendDataToParse(data,USER_ID,SESSION_TOKEN,SENSOR_ID):
	"""
		Function sends data to parse.
		- sends to IgloosenseData and sets the ACL of the data object to only readable by the Igloosense User
		- sends to Igloosense to set the lastTemperature, lastHumidity etc. This object has an ACL to the Igloosense User, so if it failed submiting, it sets a flag that asks Igloosese to re-login
	"""

	needToReLogin = False

	url = 'https://api.parse.com/1/classes/IgloosenseData'

	payload = {'status':data['status'],
				'targetTemperature':data['targetTemperature'],
				'ACL':{USER_ID:{'write':True,'read':True}},
				'igloosense':{"__type":"Pointer","className":"Igloosense","objectId":SENSOR_ID}}		#sets the access control list to restrict access

	headers = {'content-type':'application/json',
	    'X-Parse-Application-Id': 'OW1IJfhxLt0wIJ5WTowtvDv9suPyMaWMA3BtYG1F',
	    'X-Parse-REST-API-Key': 'vTJjmpVQGM43RdUhTCXv0aOAbQ3sNm8RkyOmc7kh'}
	try:
		r = requests.post(url, data=json.dumps(payload), headers=headers)
		#print r.text
	except Exception,e:
		print "Failed connecting with error at sending sensor data to parse: ",e

	url = 'https://api.parse.com/1/classes/Igloosense/' + SENSOR_ID

	headers = {'content-type':'application/json',
	    'X-Parse-Application-Id': 'OW1IJfhxLt0wIJ5WTowtvDv9suPyMaWMA3BtYG1F',
	    'X-Parse-REST-API-Key': 'vTJjmpVQGM43RdUhTCXv0aOAbQ3sNm8RkyOmc7kh',
	    'X-Parse-Session-Token': SESSION_TOKEN}

	payload = {'lastStatus':data['status'],
				'targetTemperature':data['targetTemperature']}
	try:
		r = requests.put(url, data=json.dumps(payload), headers=headers)
		#print r.text
	except Exception,e:
		print "Failed updating igloosense object with error: ",e
		needToReLogin = True

	return needToReLogin

def main(USERNAME,PASSWORD,SENSOR_ID):

	sessionToken, objectID = LoginUser(USERNAME,PASSWORD)

	pubnub = Pubnub(publish_key="pub-c-e6b9a1fd-eed2-441a-8622-a3ef7cc5853a", 
		subscribe_key="sub-c-7e14a542-b148-11e4-9beb-02ee2ddab7fe")

	channel = SENSOR_ID

	def _callback(message, channel):
		print("Message received from channel: ", message)
		data = {'status':None,'targetTemperature':None}
		if message['airconStatus']:
			if message['airconStatus'] == 'on':
				print "Lets turn on air con now"
			else:
				print "lets turn off aircon now"
			data['status'] = message['airconStatus']	
		if message['targetTemperature']:
			print "Lets turn aircon to : ", message['targetTemperature']
			data['targetTemperature'] = message['targetTemperature']
		needToReLogin = SendDataToParse(data,objectID,sessionToken,SENSOR_ID)

	def _error(message):
		print("Error: ",message)


	pubnub.subscribe(channel, callback=_callback, error=_error)


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








