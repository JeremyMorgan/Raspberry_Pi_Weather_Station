import os
import RPi.GPIO as GPIO
import time
from ds18b20 import ds18b20_read_temp
from twilio.rest import TwilioRestClient

# put your own credentials here
ACCOUNT_SID = "AC659a0e8b39db4bb242e9b4670ae0e3f2"
AUTH_TOKEN = "[AuthToken]"


pin = 16                                ## These are our LEDs
ourdelay = .1                           ## Delay
# pins 4,17,18,21,22,23,24,25

threshold = 80

GPIO.setmode(GPIO.BOARD)                ## Use BOARD pin numbering
GPIO.setup(pin, GPIO.OUT)               ## set output

## function to save code

def activateLED( pin, delay ):
    GPIO.output(pin, GPIO.HIGH)           ## set HIGH (LED ON)
    time.sleep(delay)                     ## wait
    GPIO.output(pin, GPIO.LOW)            ## set LOW (LED OFF)
    return

led = False
os.system("clear")

while True:
    temp = 9.0/5.0 * ds18b20_read_temp() + 32
    print(temp)

    if ((temp > threshold) & (led == False)):
        activateLED(pin,ourdelay)
        led = True
    else:
        if ((led == True) &(temp < threshold)):
            led = False
            activateLED(pin,ourdelay)

    time.sleep(1)


GPIO.cleanup()                          ## close down library
