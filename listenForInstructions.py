from Pubnub import Pubnub

pubnub = Pubnub(publish_key="pub-c-e6b9a1fd-eed2-441a-8622-a3ef7cc5853a", 
	subscribe_key="sub-c-7e14a542-b148-11e4-9beb-02ee2ddab7fe")

channel = "elFtIHZGjA"

def _callback(message, channel):
	print("Message received from channel: ", message)
	if message['airconStatus']:
		if message['airconStatus'] == 'on':
			print "Lets turn on air con now"
		else:
			print "lets turn off aircon now"
	if message['targetTemperature']:
		print "Lets turn aircon to : ", message['targetTemperature']

def _error(message):
	print("Error: ",message)


pubnub.subscribe(channel, callback=_callback, error=_error)


