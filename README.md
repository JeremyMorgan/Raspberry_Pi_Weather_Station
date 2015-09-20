# Raspberry Pi Mini Weather Station

<img src="http://i.imgur.com/0fuAdsS.jpg" width="600px">

##Raspberry Pi Weather Station

Measures:

* Temperature
* Humidity
* Atmospheric Pressure
* Lux

[Check out the dashboard!](http://jeremymorgan.github.io/Raspberry_Pi_Weather_Station/#/)

##Parts you'll need:

* <a href="http://www.adafruit.com/products/393">AM2302</a> Temperature / Humidity Sensor
* <a href="http://www.adafruit.com/products/1603">BMP180</a> Temperature / Barometric Pressure Sensor
* <a href="http://www.adafruit.com/products/374">DS18B20</a> Waterproof Temperature Sensor
* <a href="http://www.adafruit.com/products/439">TSL2561</a> Digital Lumosity Sensor

##Installation Instructions:

These instructions have been tested with the latest version of Raspian, however they should run in most distributions of Linux fairly easily. 

Wire up the sensors as shown here: 
<img src="http://i.imgur.com/5uoNdbp.png" width="650px" height="538">

###Setup the AM302

Here we set up the <a href="http://www.adafruit.com/products/393">AM2302</a> Humidity Sensor. 

Clone the Adafruit Python DHT Library
```
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
```
Build some tools

```
sudo apt-get update

sudo apt-get install build-essential python-dev python-openssl

sudo python setup.py install
```

###Setup the DSB18B20

You will need to add One Wire Support:

```
sudo nano /boot/config.txt
```

Add the following line:
```
dtoverlay=w1-gpio
```

Reboot the Pi:

```
sudo reboot
```

Add smbus and i2c tools:

```
sudo apt-get install python-smbus
sudo apt-get install i2c-tools
```

You may get "already installed" Messages from this

```
sudo nano /etc/modules
```

Add the following:

```
i2c-bcm2708 
i2c-dev
```
Modify boot config:

```
sudo nano /boot/config.txt
```

Add the following lines:

```
dtparam=i2c1=on
dtparam=i2c_arm=on
```
Reboot the Pi:

```
sudo reboot
```

###Setup the TSL2561

cd ~/sources 

```
wget https://raw.githubusercontent.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/master/Adafruit_I2C/Adafruit_I2C.py
wget https://raw.githubusercontent.com/seanbechhofer/raspberrypi/master/python/TSL2561.py
```

(Thanks to Sean!)

###Setup the BMP 180

```
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP
sudo python setup.py install
```

###Test the sensors

```
git clone https://github.com/JeremyMorgan/Raspberry_Pi_Weather_Station.git reader
cd reader
sudo python readings.py dryrun
```




