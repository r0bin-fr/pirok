import os
import glob
import time
import threading
import SSRControl
import readMaxim


class TaskControlPID(threading.Thread): 

    #default target temp is 118C
    def __init__(self, taskid = 0, maximBoiler = None, tTarget = 118): 
        threading.Thread.__init__(self) 
 	self.lok = threading.Lock()
        self.taskid = taskid
        self._stopevent = threading.Event( ) 
        self.maximBoiler = maximBoiler
	self.currentDrive = 0
	#init regulator values
	self.m_timeStep = 1.0
	self.m_targetTemp = tTarget
	self.m_latestTemp = 20.0
	self.m_latestPower = 0.0
	#init PID values
	self.m_dState = 0.0
	self.m_iState = 0.0 
	self.m_iMin  = -1.0
	self.m_iMax  = 1.0
	self.m_iGain = 0.0
	self.m_pGain = 1.0 
	self.m_dGain = 0.0


    #based on James Ward's PID algorithm
    def pid_update(self,error = 0.0, position = 0.0):
	# calculate proportional term
	pTerm = self.m_pGain * error

	# calculate integral state with appropriate limiting
	self.m_iState += error
	if ( self.m_iState > self.m_iMax ):
		self.m_iState = self.m_iMax
	if ( self.m_iState < self.m_iMin ):
		self.m_iState = self.m_iMin

	#calculate integral term
	iTerm = self.m_iGain * self.m_iState

	#calculate derivative term
	dTerm = self.m_dGain * (self.m_dState - position)
	self.m_dState = position

	return pTerm + dTerm + iTerm



    def run(self):
    	print "Thread PID no", self.taskid, "is readry!\n > Based on James Ward's PID algorithm"
	
	drive = 0.0
	lastdrive = 0.0
	#based on James Ward's PID algorithm	
	while not self._stopevent.isSet(): 
		#PID computation
		#timestamp
		next = time.time()
		#get current boiler temp
		latestTemp = self.maximBoiler.getTemp()
		#controle de la chaudiere
		lastdrive = drive	
		
		#if temperature read is correct, start algorithm
		if ( latestTemp > 0.5 ):
			#calculate next time step
			next += self.m_timeStep
			#calculate PID update
			drive = self.pid_update( self.getTargetTemp() - latestTemp, latestTemp )
		
		#clamp the output power to sensible range
		if ( drive > 1.0 ):
			drive = 1.0
		if ( drive < 0.0 ):
			drive = 0.0

		#update the boiler power (with PWM) if last state changed
		if ( drive != lastdrive ):
			drv = int(drive * 100)
			self.setCurrentDrive( drv )
			SSRControl.setBoilerPWM( drv )

		#wait the remaining time (typically, slot = 1 second)
		remain = next - time.time()
		if ( remain > 0.0 ):
			self._stopevent.wait(remain)

    def stop(self): 
	print "stopping thread no", self.taskid
        self._stopevent.set( ) 

    def getTargetTemp(self):
        #protect concurrent access with mutex
	self.lok.acquire()
        tt = self.m_targetTemp 
        self.lok.release()
	return tt

    def setTargetTemp(self,ttemp=115):
        #protect concurrent access with mutex
	self.lok.acquire()
        self.m_targetTemp = ttemp
        self.lok.release()

    def getCurrentDrive(self):
        #protect concurrent access with mutex
        self.lok.acquire()
        tt = self.currentDrive
        self.lok.release()
        return tt

    def setCurrentDrive(self,drive=0):
        #protect concurrent access with mutex
        self.lok.acquire()
        self.currentDrive = drive
        self.lok.release()

 
