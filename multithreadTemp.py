import os
import glob
import time
import threading
import readMaxim


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
		#self.mData.setTemp(readMaxim.read_temp(self.taskid))
		xyz = readMaxim.read_temp(self.taskid)
	
		if(xyz != None):
			#avoid glitches
			if(int(xyz) != 0):
				xyz = (xyz + self.lastTemp)/2
				self.mData.setTemp(xyz)
				self.lastTemp = xyz				
#			#it might be normal if we read it two times?
#			if (int(xyz) == 0) and (int(self.lastTemp) == 0) :
#				self.mData.setTemp(xyz)
#				xyz = (xyz + self.lastTemp)/2
#				self.mData.setTemp(xyz)				
		self._stopevent.wait(0.2) 

    def stop(self): 
	print "stopping thread no", self.taskid
        self._stopevent.set( ) 

