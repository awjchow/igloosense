import sys
import time
import datetime
import requests
import json
import RPi.GPIO as GPIO
from Adafruit_CharLCD import Adafruit_CharLCD



def checkUserStatus(USER_ID):
	url = 'https://api.parse.com/1/users/' + USER_ID

	headers = {'content-type':'application/json',
	    'X-Parse-Application-Id': 'OW1IJfhxLt0wIJ5WTowtvDv9suPyMaWMA3BtYG1F',
	    'X-Parse-REST-API-Key': 'vTJjmpVQGM43RdUhTCXv0aOAbQ3sNm8RkyOmc7kh'}
	try:
		r = requests.get(url, headers=headers)
		print r.text
		airconStatus = r['airconStatusChange']
		temperatureChange = r['airconTemperatureChange']
		messageChange = r['messageChange']
		if (airconStatusChange or temperatureChange or messageChange):
			if messageChange:
				myMessage = r['message']
				lcd = Adafruit_CharLCD()
				lcd.clear()
				lcd.message(message)
				data = {'messageChange':False}
				g = requests.post(url,data=json.dump(data),headers=headers)
				


	except Exception,e:
		print "Failed connecting with error: ",e


def main():
	USER_ID = 'L5WgX2wJez'
	checkUserStatus(USER_ID)

if __name__ == '__main__':
	main()



