import RPi.GPIO as GPIO             ## Import GPIO Library
import time                         ## Import 'time' library (for 'sleep')

pin = 16                            ## These are our LEDs
ourdelay = 3                        ## Delay
# pins 4,17,18,21,22,23,24,25

GPIO.setmode(GPIO.BOARD)            ## Use BOARD pin numbering
GPIO.setup(pin, GPIO.OUT)        ## set output

## function to save code

def activateLED( pin, delay ):
  GPIO.output(pin, GPIO.HIGH)      ## set HIGH (LED ON)
  time.sleep(delay)                ## wait
  GPIO.output(pin, GPIO.LOW)       ## set LOW (LED OFF)
  return;

activateLED(pin,ourdelay)

GPIO.cleanup()                      ## close down library
