import RPi.GPIO as GPIO
import time
from ds18b20 import ds18b20_read_temp
from twilio.rest import TwilioRestClient

ACCOUNT_SID = "YOUR SID"
AUTH_TOKEN = "YOUR KEY"

threshold = 79

sent = False

while True:
    temp = 9.0/5.0 * ds18b20_read_temp() + 32

    print(temp)
    if ((temp > threshold) & (sent == False)):
            client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(
                to="YOUR PHONE",
                from_="YOUR TWILIO PHONE",
                body="Temperature is above the threshold at " + str(temp),
            )
            sent = True

    time.sleep(1)

GPIO.cleanup()

