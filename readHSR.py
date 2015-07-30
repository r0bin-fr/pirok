import os
import glob
import time
import threading
import sys

device_folder = '/sys/kernel/hcsr04/range'

 
def read_range_raw():
        device_file = device_folder
	try:
        	f = open(device_file, 'r')
        	lines = f.readlines()
        	f.close()
        	return lines
	except IOError as e:
		print "Erreur fichier ", device_file," (ouverture, lecture ou fermeture)"
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		return "READ ERROR"
	except:
		print "Erreur fichier ", device_file," (ouverture, lecture ou fermeture)", sys.exc_info()[0]
		return "READ ERROR"

def read_range():
        lines = read_range_raw()
        while lines[0].strip()[-1:] != '1':
#		print "lecture hcsr04 echoue: ",lines
            	time.sleep(0.1)
	    	lines = read_range_raw()
        position_espace = lines[0].find(' ')
       	if position_espace != -1:
            range_string = lines[0][0:position_espace]
            range_float = float(range_string)
            return range_float
        #error case: return none
	print "pas d'espace trouve, retourne None, erreur chelou:",lines
        return None


class HSRData:
	def __init__(self,range=0.0):
		self.range = range
		self.lastrange = range
		self.lok = threading.Lock()

	def setRange(self,range):
		#protect concurrent access with mutex
		self.lok.acquire()
		self.lastrange = self.range
		self.range = range
		self.lok.release()

	def getRange(self):
		#protect concurrent access with mutex
		self.lok.acquire()
		xyz = (self.range + self.lastrange) / 2
		self.lok.release()
		return xyz

