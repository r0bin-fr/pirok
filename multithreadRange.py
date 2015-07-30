import os
import glob
import time
import threading
import readHSR


class TaskPrintRange(threading.Thread): 

    def __init__(self, taskid = 0, mData = readHSR.HSRData()): 
        threading.Thread.__init__(self) 
        self.taskid = taskid
        self._stopevent = threading.Event( ) 
	self.mData = mData
	self.buffer = 0.0

    def run(self):
    	print "thread capteur no", self.taskid, "is readry!"
	
	while not self._stopevent.isSet(): 
		NB_READ_RANGE = 10
		#x lectures pour faire une moyenne
		for i in xrange(NB_READ_RANGE):
			xyz = readHSR.read_range()
			if(xyz != None):
				self.buffer += xyz
#				print "lecture ",i," valeur=",xyz
			else:
				i = i-1
			#attende de 100ms entre chaque lecture
			self._stopevent.wait(0.1)
			
		#apres x lectures, faire la moyenne
		mrange = self.buffer / NB_READ_RANGE
		self.mData.setRange(mrange)
		self.buffer = 0.0
		self._stopevent.wait(0.8) 

    def stop(self): 
	print "stopping thread no", self.taskid
        self._stopevent.set( ) 

