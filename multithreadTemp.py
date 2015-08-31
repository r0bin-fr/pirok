import os
import glob
import time
import threading
import readMaxim
import readMaximSPI
import math

class TaskPrintTemp(threading.Thread): 

    def __init__(self, taskid = 0, mData = readMaxim.MaximData()): 
        threading.Thread.__init__(self) 
        self.taskid = taskid
        self._stopevent = threading.Event( ) 
	self.mData = mData
	self.lastTemp = 0.0

    def run(self):
    	print "thread capteur no", self.taskid, "is readry!"
	while not self._stopevent.isSet(): 
	#	print "capteur", self.taskid,"temp=",readMaxim.read_temp(self.taskid)

		#SPI read
		if(self.taskid == 5):
			xyz = readMaximSPI.read_temp(self.taskid)
		#regular read
		else:
			xyz = readMaxim.read_temp(self.taskid)

		#take only valid numbers
		if(xyz != None):
			#cover cases where we get NaN (safety) 
			if(math.isnan(xyz) == False):
				#avoid glitches
				if(int(xyz) != 0):
					xyz = (xyz + self.lastTemp)/2
					self.mData.setTemp(xyz)
					self.lastTemp = xyz				
		#wait a little
		self._stopevent.wait(0.2) 

    def stop(self): 
	print "stopping thread no", self.taskid
        self._stopevent.set( ) 

