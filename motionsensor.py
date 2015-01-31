"""
import RPi.GPIO as GPIO
import time
import datetime


def motion(mypin):
    print "My input:", + str(GPIO.input(mypin))
    print mypin
    if GPIO.input(mypin):
        print "Motion Detected!"
        print GPIO.input(mypin)
        print datetime.datetime.now()
    else:
        print "Motion Dropping"
        print GPIO.input(mypin)
        print datetime.datetime.now()

GPIO.setmode(GPIO.BCM) #GPIO.BCM uses GPIO number, GPIO.BOARD uses board number
PIR_PIN = 7
GPIO.setup(PIR_PIN,GPIO.IN)
print "PIR Module Test (CTRL+C to exit)"
time.sleep(1)
print "Ready"


while True:
    print "My current GPIO state:", GPIO.input(PIR_PIN)
    print datetime.datetime.now()
    time.sleep(3)
"""

"""
    try:
    GPIO.add_event_detect(PIR_PIN,GPIO.FALLING,callback=motion,bouncetime=300)
    while True:
    time.sleep(3)
    except KeyboardInterrupt:
    print "Quit"
    finally:
    GPIO.cleanup()
"""





# Import required Python libraries
import RPi.GPIO as GPIO
import time
import datetime

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_PIR = 13

print "PIR Module Test (CTRL-C to exit)"

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo

Current_State  = 0
Previous_State = 0

try:
    
    print "Waiting for PIR to settle ...", datetime.datetime.now()
    
    # Loop until PIR output is 0
    while GPIO.input(GPIO_PIR)==1:
        Current_State  = 0
    
    print "  Ready to check for motion.", datetime.datetime.now()
    
    # Loop until users quits with CTRL-C
    while True :
        
        # Read PIR state
        Current_State = GPIO.input(GPIO_PIR)
        
        if Current_State==1 and Previous_State==0:
            # PIR is triggered
            print "  +++ Motion detected!", datetime.datetime.now()
            # Record previous state
            Previous_State=1
        elif Current_State==0 and Previous_State==1:
            # PIR has returned to ready state
            print "  --- Motion removed.", datetime.datetime.now()
            Previous_State=0
        
        # Wait for 10 milliseconds
        time.sleep(0.1)

except KeyboardInterrupt:
    print "  Quit"
    # Reset GPIO settings
    GPIO.cleanup()











