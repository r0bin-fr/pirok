# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola, updated by r0bin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import glob
import time
import threading
import sys

import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855

# Uncomment one of the blocks of code below to configure your Pi or BBB to use
# software or hardware SPI.

# Raspberry Pi software SPI configuration.
#CLK = 23 #25
#CS  = 24
#DO  = 21 #18
#sensor = MAX31855.MAX31855(CLK, CS, DO)

# Raspberry Pi hardware SPI configuration.
SPI_PORT   = 0
SPI_DEVICE = 0
sensor = MAX31855.MAX31855(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

 
def read_temp_raw():
	try:
		temp = sensor.readTempC()
		buf = "%.1f OK" % temp
        	return buf

	except IOError as e:
		print "SPI I/O error({0}): {1}".format(e.errno, e.strerror)
		return "SPI READ ERROR"
	except:
		print "Erreur generique SPI", sys.exc_info()[0]
		return "SPI GENERAL ERROR"
 
def read_temp(no_capteur):
        lines = read_temp_raw()
        while lines.strip()[-2:] != 'OK':
            time.sleep(0.2)
            lines = read_temp_raw()
	position_espace = lines.find(' ')
        if position_espace != -1:
            range_string = lines[0:position_espace]
            range_float = float(range_string)
            return range_float
	#error case: return none
        print "pas d'espace trouve, retourne None, erreur chelou:",lines
        return None


