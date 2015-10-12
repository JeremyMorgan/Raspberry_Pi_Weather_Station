__author__ = 'jeremymorgan'

# libraries
import sys
import urllib2
import json
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085

# custom functions
from ds18b20 import ds18b20_read_temp
import luxreader

# Instance of TSL2561 Class
luxrdr = luxreader.TSL2561()

# Config
am2302Pin = 22

# Check if this is a dry run
if len(sys.argv) > 1:
    if(sys.argv[1] == 'dryrun'):
        dryrun = True
else:
    dryrun = False

# Start Output
if dryrun:
    print 'Sensor Reading Dry Run'
    print '************************'

# Select Sensors to Use
useAM2302 = True
useBMP180 = True
useDS18B20 = True
useTSL2561 = True

## AM2302 Humidity / Temp Sensor
if useAM2302:
    humidity, temperature1 = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302 , am2302Pin)
    if (dryrun):
        print 'AM2302:'
        print 'Temp Sensor 1 = {0:0.1f} *C'.format(temperature1)
        print 'Humidity={0:0.1f}%'.format(humidity) + '\n'
else:
    humidity,temperature1 = 0,0

# BMP180 Barometric Pressure Sensor
if useBMP180:
    #sensor = BMP085.BMP085()
    #sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRALOWPOWER)
    #sensor = BMP085.BMP085(mode=BMP085.BMP085_STANDARD)
    #sensor = BMP085.BMP085(mode=BMP085.BMP085_STANDARD)
    #sensor = BMP085.BMP085(mode=BMP085.BMP085_HIGHRES)
    sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

    pressure = sensor.read_pressure()
    altitude = sensor.read_altitude()
    slpressure = sensor.read_sealevel_pressure()
    temperature2 = sensor.read_temperature()

    if dryrun:
        print 'BMP180:'
        print 'Temp Sensor 2 = {0:0.2f} *C'.format(temperature2)
        print 'Pressure = {0:0.2f} Pa'.format(pressure)
        print 'Altitude = {0:0.2f} m'.format(altitude)
        print 'Sealevel Pressure = {0:0.2f} Pa'.format(slpressure) + '\n'
else:
    sensor,pressure,altitude,slpressure,temperature2 = 0,0,0,0,0

## DS18B20 Waterproof Temperature Probe
if useDS18B20:
    temperature3 = ds18b20_read_temp()
    if dryrun:
        print 'DS18B20:'
        print 'Temp Sensor 3 = {0:0.3f} *C'.format(temperature3) + '\n'

else:
    temperature3 = 0

## TSL2561 Lux Sensor
if useTSL2561:
    lux = luxrdr.readLux()      # Auto
    #lux = luxrdr.readLux(1)     # Low Gain
    #lux = luxrdr.readLux(16)    # High Gain

    lux = luxrdr.readLux()

    if dryrun:
        print 'TSL2561:'
        print 'Lux: ' + str(lux) + '\n'
else:
    lux = 0


## Get Average Temperature

avgTemp = ((temperature1 + temperature2 + temperature3) / 3)
tempList = [temperature1,temperature2,temperature3]
highestTemp = max(tempList)
lowestTemp = min(tempList)

if dryrun:
    print "Highest: " + str(highestTemp)
    print "Lowest: " + str(lowestTemp)
    print "Average: " + str(avgTemp)
    print "Variance: " + str(highestTemp - lowestTemp) + '\n'
    print '************************\n'
else:
    url = '[YOUR URL]'

    postdata = {
        'Altitude': altitude,
        'Humidity': humidity,
        'Lux': lux,
        'Pressure': pressure,
        'SeaLevelPressure': slpressure,
        'TempSensor1': temperature1,
        'TempSensor2': temperature2,
        'TempSensor3': temperature3,
        'TempSensorAvg': avgTemp
    }

    req = urllib2.Request(url)
    req.add_header('Content-Type','application/json')
    data = json.dumps(postdata)

    response = urllib2.urlopen(req,data)
