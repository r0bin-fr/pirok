import os
import glob
import time
import threading
import sys

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '3b*')

 
def read_temp_raw(no_capteur):
        device_file = device_folder[no_capteur] + '/w1_slave'
   #     print("capteur:",no_capteur," using file: ",device_file)
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
 
def read_temp(no_capteur):
        lines = read_temp_raw(no_capteur)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw(no_capteur)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
#            temp_f = temp_c * 9.0 / 5.0 + 32.0
#            print "Capteur no%i: %.2f C" % (no_capteur,temp_c) 
            return temp_c
        #error case: return none
        return None


class MaximData:
	def __init__(self,temp=0):
		self.temp = temp
		self.hum = 0.0
		self.lok = threading.Lock()

	def setTemp(self,temp):
		#protect concurrent access with mutex
		self.lok.acquire()
		self.temp = temp
		self.lok.release()

	def getTemp(self):
		#protect concurrent access with mutex
		self.lok.acquire()
		xyz = self.temp
		self.lok.release()
		return xyz

        def setTempHum(self,temp,hum):
                #protect concurrent access with mutex
                self.lok.acquire()
                self.temp = temp
		self.hum = hum
                self.lok.release()

        def getTempHum(self):
                #protect concurrent access with mutex
                self.lok.acquire()
                txy = self.temp
		hxy = self.hum
                self.lok.release()
                return txy , hxy

