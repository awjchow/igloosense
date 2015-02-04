import sys
import time
import datetime
import requests
import json
#import RPi.GPIO as GPIO
#from Adafruit_CharLCD import Adafruit_CharLCD


def LoginUser(USERNAME,PASSWORD):
	url = 'https://api.parse.com/1/login'

	headers = {'content-type':'application/json',
	    'X-Parse-Application-Id': 'OW1IJfhxLt0wIJ5WTowtvDv9suPyMaWMA3BtYG1F',
	    'X-Parse-REST-API-Key': 'vTJjmpVQGM43RdUhTCXv0aOAbQ3sNm8RkyOmc7kh'}	

	payload = {"username":USERNAME,"password":PASSWORD}
	r = requests.get(url,params=payload, headers=headers)
	r = json.loads(r.text)
	return r['sessionToken'], r['objectId']


def CheckUserStatus(USER_ID,SESSION_TOKEN):
	url = 'https://api.parse.com/1/users/' + USER_ID

	headers = {'content-type':'application/json',
	    'X-Parse-Application-Id': 'OW1IJfhxLt0wIJ5WTowtvDv9suPyMaWMA3BtYG1F',
	    'X-Parse-REST-API-Key': 'vTJjmpVQGM43RdUhTCXv0aOAbQ3sNm8RkyOmc7kh',
	    'X-Parse-Session-Token': SESSION_TOKEN }
	try:
		r = requests.get(url, headers=headers)
		print r.text
		r = json.loads(r.text)
		airconStatusChange = r['airconStatusChange']
		temperatureChange = r['airconTemperatureChange']
		messageChange = r['messageChange']
		print messageChange
		if (airconStatusChange or temperatureChange or messageChange):
			if messageChange:
				myMessage = r['message']
				print myMessage
				#lcd = Adafruit_CharLCD()
				#lcd.clear()
				#lcd.message(message)
				data = {'messageChange':False}
				g = requests.put(url,data=json.dumps(data),headers=headers)
				print g
				print g.text


	except Exception,e:
		print "Failed connecting with error: ",e




def main():
	USERNAME = 'igloo'
	PASSWORD = 'igloo'
	#USER_ID = 'L5WgX2wJez'
	#
	sessionToken, objectID = LoginUser(USERNAME,PASSWORD)
	CheckUserStatus(objectID,sessionToken)

if __name__ == '__main__':
	main()



