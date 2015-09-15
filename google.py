#!/usr/bin/python

import json
import sys
import time
import datetime

# libraries
import sys
import urllib2
import json
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

# custom functions
from ds18b20 import ds18b20_read_temp
import luxreader

# Instance of TSL2561 Class
luxrdr = luxreader.TSL2561()

# Config
am2302Pin = 22

# Oauth JSON File
GDOCS_OAUTH_JSON       = 'Mini Weather Station-f68343d4a35a.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'Sensors'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 30


def login_open_sheet(oauth_key_file, spreadsheet):
	"""Connect to Google Docs spreadsheet and return the first worksheet."""
	try:
		json_key = json.load(open(oauth_key_file))
		credentials = SignedJwtAssertionCredentials(json_key['client_email'],
													json_key['private_key'],
													['https://spreadsheets.google.com/feeds'])
		gc = gspread.authorize(credentials)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except Exception as ex:
		print 'Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!'
		print 'Google sheet login failed with error:', ex
		sys.exit(1)


print 'Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print 'Press Ctrl-C to quit.'
worksheet = None
while True:
	# Login if necessary.
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

	# Attempt to get sensor reading.

    	humidity, temperature1 = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302 , am2302Pin)
	sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
	pressure = sensor.read_pressure()
	altitude = sensor.read_altitude()
	slpressure = sensor.read_sealevel_pressure()
	temperature2 = sensor.read_temperature()
	temperature3 = ds18b20_read_temp()
	lux = luxrdr.readLux()
	avgTemp = ((temperature1 + temperature2 + temperature3) / 3)

	print 'Temp Sensor 1 = {0:0.1f} *C'.format(temperature1)
	print 'Humidity={0:0.1f}%'.format(humidity)
	print 'BMP180:'
	print 'Temp Sensor 2 = {0:0.2f} *C'.format(temperature2)
	print 'Pressure = {0:0.2f} Pa'.format(pressure)
	print 'Altitude = {0:0.2f} m'.format(altitude)
	print 'Sealevel Pressure = {0:0.2f} Pa'.format(slpressure)
	print 'Temp Sensor 3 = {0:0.3f} *C'.format(temperature3)
	print 'Lux: ' + str(lux)
	print "Average: " + str(avgTemp)

	# Append the data in the spreadsheet, including a timestamp
	try:
		worksheet.append_row((datetime.datetime.now(), altitude,humidity,lux,pressure,slpressure,temperature1,temperature2,temperature3,avgTemp))
	except:
		# Error appending data, most likely because credentials are stale.
		# Null out the worksheet so a login is performed at the top of the loop.
		print 'Append error, logging in again'
		worksheet = None
		time.sleep(FREQUENCY_SECONDS)
		continue

	# Wait 30 seconds before continuing
	print 'Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME)
	time.sleep(FREQUENCY_SECONDS)
