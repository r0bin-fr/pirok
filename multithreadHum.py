import os
import glob
import time
import threading
import readMaxim
import subprocess

#import Adafruit_DHT
#import RPi.GPIO as pigpio
#import pigpio
#import DHT22

class TaskPrintHum(threading.Thread): 

    def __init__(self, taskid = 0, mData = readMaxim.MaximData()): 
        threading.Thread.__init__(self) 
        self.taskid = taskid
        self._stopevent = threading.Event( ) 
	self.mData = mData

    def run(self):
    	print "thread capteur no", self.taskid, "is readry!"
	while not self._stopevent.isSet():
		timestamp = time.time()
		
		try:
			task = subprocess.Popen(['sudo','python','/home/pi/pygame/AdafruitDHT.py','2302','17'],stdout=subprocess.PIPE)
			t,h = task.stdout.readline().split(' ')
			temperature = float(t)
			humidity = float(h)
		except:
			humidity = 0
			temperature = 0

		if ( humidity == 0 ) and (temperature == 0):
			print "Pas de donnees"
      		else:
			print 'Time={0:d} Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format((int(time.time())),temperature, humidity)	
			self.mData.setTempHum(temperature, humidity)

		# Try to grab a sensor reading.  Use the read_retry method which will retry up
		# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
#		humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)

		# Note that sometimes you won't get a reading and
		# the results will be null (because Linux can't
		# guarantee the timing of calls to read the sensor).
		# If this happens try again!
#		if humidity is not None and temperature is not None:
 #       		print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)	
#			self.mData.setTempHum(temperature, humidity)
#		else:
 #       		print 'Failed to get reading. Try again!'

		#wait at least 3 seconds to avoid sensor hang
		#timewaited = time.time() - timestamp
		#if timewaited < 3:
		#	self._stopevent.wait(3 - timewaited) 

		#wait for 30 seconds before new read, we don't need so much updates on the hygrometry
		self._stopevent.wait(30)

    def stop(self): 
	print "stopping thread no", self.taskid
        self._stopevent.set( ) 
