#!/usr/bin/python

# -*- coding: latin-1 -*-
import pygame
import pygame.gfxdraw
import math
import time
import calendar
import mygauge
import myplot
import mywatergauge
import readMaxim
import readHSR
import multithreadTemp
import multithreadHum
import multithreadRange
import multithreadPID
import SSRControl
import signal
import sys
from subprocess import call

#Debug file
DEBUGFILE = 0
#Temperature file backup
TEMPBACKUP = '/home/pi/pygame/settings'

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREY	 = ( 127, 127, 127)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
BLEUNEST = (   0,  60, 236) #bleu roi nest
BLEUINT  = ( 164, 202, 255) #bleu clair
PLOT1    = ( 124, 181, 236) #bleu pastel
PLOT2    = ( 144, 237, 125) #vert pastel
PLOT3    = ( 247, 163,  97) #orange pastel

#init pygame lib 
pygame.init() 

# Set the width and height of the screen [width, height]
size = (800, 480)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.NOFRAME )

#load logo image
rlogo = pygame.image.load("/home/pi/pygame/logov4.gif")
rcommande = pygame.image.load("/home/pi/pygame/plusmoins.gif")

#hide mouse cursor
#pygame.mouse.set_visible( False )

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# value for test
rot = -10
lasttct = 0

# global values for data handling
maximT1 = readMaxim.MaximData(0)
maximT2 = readMaxim.MaximData(0)
maximT3 = readMaxim.MaximData(0)
dhtData = readMaxim.MaximData(0)
hsrData = readHSR.HSRData(0)

#launch thread to update the temp values and other (hum, range etc)
task1 = multithreadTemp.TaskPrintTemp(0,maximT1)
task2 = multithreadTemp.TaskPrintTemp(1,maximT2)
task3 = multithreadTemp.TaskPrintTemp(2,maximT3)
task4 = multithreadHum.TaskPrintHum(3,dhtData)
task5 = multithreadRange.TaskPrintRange(4,hsrData)
#maximT2 is the boiler temp sensor, target = 117C
temptarget=117
task6PID = multithreadPID.TaskControlPID(5,maximT2,temptarget)
consigneSpecialePID = 0
lastTargetTemp = temptarget

task1.start()
task2.start()
task3.start()
task4.start()
task5.start() 
task6PID.start()

#how to quit application nicely
def quitApplicationNicely():
	done = True
	#be sure to shut down the boiler as well
	SSRControl.setBoilerPWM(0)
	saveSettings()
	task1.stop()
	task2.stop()
	task3.stop()
	task4.stop()
	task5.stop()
	task6PID.stop()
	time.sleep(0.1)
	pygame.quit()
        sys.exit(0)

#signal handler
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
	quitApplicationNicely()

#current flow counter (handle deltas)
deltaFlow = 0
currentFlow = 0

#get current flow counter
def getFlow():
	global currentFlow,deltaFlow
	device_file = '/sys/kernel/flow/flow'
        try:
                f = open(device_file, 'r')
                lines = f.read()#lines()
                f.close()
		currentFlow = int(lines)
		return currentFlow - deltaFlow

        except IOError as e:
                print "Erreur fichier ", device_file," (ouverture, lecture ou fermeture)"
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                return -1
        except:
                print "Erreur fichier ", device_file," (ouverture, lecture ou fermeture)", sys.exc_info()[0]
                return -1



#intercept control c for nice quit
signal.signal(signal.SIGINT, signal_handler)

chronoRuning = False
topdepart = 0.0
finchrono = 0.0
fontChrono = pygame.font.SysFont('dejavusans', 22, True, False)
fontSmall = pygame.font.SysFont('dejavusans', 12, True, False)


def startChrono(ndfl):
	global currentFlow,deltaFlow
	global chronoRuning, topdepart, finchrono
	if(chronoRuning == False):
		chronoRuning = True
		topdepart = time.time()
		#deltaFlow = ndfl
		#deltaFlow = currentFlow	

def stopChrono():
	global chronoRuning, topdepart, finchrono
	if(chronoRuning == True):
                chronoRuning = False
                finchrono = time.time()

def getChrono():
	global chronoRuning, topdepart, finchrono
	if(chronoRuning == True):
		return time.time() - topdepart
	else:
		return finchrono - topdepart

def drawChrono(): 
	global screen,fontChrono
    	# display chrono
	buf = "%.1f s" % getChrono()
    	ctext = fontChrono.render(buf, True, WHITE)
	stext = fontSmall.render("Chrono:",True,WHITE)
	# blit to screen
    	screen.blit(stext,(500,25))
    	screen.blit(ctext,(500,40))

def getTempTarget(): 
	print "getTemp"
	try:
                tfile = open(TEMPBACKUP, "r")
                line = tfile.readline()
                tfile.close()
		#conversion en entier
		ttarget = int(line)
 	except IOError as e:
		print "Erreur fichier ", TEMPBACKUP," (ouverture, lecture ou fermeture)"
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
		ttarget = 0
        except:
                print "Erreur fichier ", TEMPBACKUP," (ouverture, lecture ou fermeture)", sys.exc_info()[0]
		ttarget = 0
	return ttarget

def loadSettings():
	global temptarget
	print "loadsettings"
	val = getTempTarget()
	#default: 115C
	if(val == 0):
		temptarget = 115
		print "Load settings: using default temptarget value of 115C"
	else:
		temptarget = val	
		print "Load settings: temptarget value is now ",temptarget,"C"
		

def saveSettings():
	#recuperation de la consigne reelle
	if(consigneSpecialePID == 1):
        	temptosave = lastTargetTemp	
	else:
		temptosave = temptarget
	#a-t-on vraiment besoin d'ecrire dans la flash? (abime)
	val = getTempTarget()
	if ((val > 0) and (val == temptosave)):
		print "pas besoin d'ecrire dans la flash"
		return
	#nouvelle valeur: ecriture dans un fichier  
	buf = "%d" % temptosave
	buf = buf + "\n"
	print "Saving temptarget", buf, "ok?"
	try:
                tfile = open(TEMPBACKUP, "w")
                tfile.write(buf)
                tfile.close()
 	except IOError as e:
		print "Erreur fichier ", TEMPBACKUP," (ouverture, lecture ou fermeture)"
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
                print "Erreur fichier ", TEMPBACKUP," (ouverture, lecture ou fermeture)", sys.exc_info()[0]

#init vars
FLOWAJUST = 4.2
fl = getFlow() / FLOWAJUST
deltaFlow = currentFlow
loadSettings()

# -------- Main Program Loop -----------
while not done:
    #try to respect as much as possible the time slot
    timestamp = time.time()

    #event loop    
    for event in pygame.event.get(): 
	# Case user click exit button (never happen we are fullscreen)
        if event.type == pygame.QUIT:
            done = True 
    	#did we clicked somewhere?
  	if (event.type == pygame.MOUSEBUTTONDOWN) :
		mpx,mpy = event.pos
		print "Mouse click detected at", mpx, ",", mpy
		if( (mpx > 700) and (mpy < 100) ):
			print "mouse click exiting..."
			done = True
		if( (mpx > 700) and (mpy > 400) ):
			print "reset flow"
			deltaFlow = currentFlow			
		#ajust boiler temp
		if( (mpx > 650) and (mpx < 700) and (mpy > 200) and (mpy < 250) ):
			print "click on ROCKET"
			if(consigneSpecialePID == 0):
				lastTargetTemp = temptarget
				consigneSpecialePID = 1
 			temptarget = 124
			task6PID.setTargetTemp(temptarget)
		if( (mpx > 600) and (mpx < 650) and (mpy > 250) and (mpy < 300) ):
			print "click on MOINS"
			if(consigneSpecialePID == 1):
				temptarget = lastTargetTemp
				consigneSpecialePID = 0
			else:
				temptarget -= 1
			task6PID.setTargetTemp(temptarget)
		if( (mpx > 700) and (mpx < 750) and (mpy > 250) and (mpy < 300) ):
			print "click on PLUS"
			if(consigneSpecialePID == 1):
                                temptarget = lastTargetTemp
                                consigneSpecialePID = 0
                        else:
				temptarget += 1
			task6PID.setTargetTemp(temptarget)
		if( (mpx > 650) and (mpx < 700) and (mpy > 300) and (mpy < 350) ):
			print "click on STOP"
			if(consigneSpecialePID == 0):
                                lastTargetTemp = temptarget
                                consigneSpecialePID = 1
			temptarget = 20
			task6PID.setTargetTemp(temptarget)

    # Clear the screen and set the screen background
    screen.fill(BLACK)
    rquit = pygame.Rect(750,0,50,50)
    screen.fill(RED,rquit)
    screen.blit(rlogo,(800-rlogo.get_width(), 0))
    screen.blit(rcommande,(600,200))

    #add plus/minus buttons
#    rplus = pygame.Rect(675,200,50,50)
#    screen.fill(RED,rplus)
#    rmoins = pygame.Rect(675,300,50,50)
#    screen.fill(GREEN,rmoins)

    #display current target temp 
    buf = "%d" % temptarget
    buf = buf + chr(176) #"c"
    ctext = fontChrono.render(buf, False, WHITE)
    screen.blit(ctext,(650,260))
    #display current PID load
    buf2 = "  %d" % task6PID.getCurrentDrive()
    buf2 = buf2 + "%"
    stext = fontSmall.render(buf2,False,GREY)
    screen.blit(stext,(650,285))

    #affiche les jauges
    t1 = maximT1.getTemp()
    t2 = maximT2.getTemp()
    t3 = maximT3.getTemp()
    t4,h4 = dhtData.getTempHum()
    r5 = hsrData.getRange()
    oldfl = fl
    fl = getFlow() / FLOWAJUST 

    mygauge.drawGauge("Extra",chr(176), 100,400, t1,-10,100,False,False,PLOT1) 
    mygauge.drawGauge("Chaudiere", chr(176),250,400, t2,-10,100,False,False,PLOT2) 
    mygauge.drawGauge("Nez",chr(176),400,400, t3,-10,100,False,False,PLOT3) 
    mygauge.drawGauge("Hum","%", 550,400, h4,0,100,False,False,WHITE) 
    mygauge.drawGauge("Flow"," ml",  700,400, fl ,0,60,False,False,WHITE) 

    #affiche la jauge d'eau
    mywatergauge.drawRGauge(500+10,85,240,24,r5,224.0,50.0)

    #gestion du chrono
    if(fl > oldfl):
	startChrono(oldfl)

    if(fl == oldfl):
	stopChrono()
    drawChrono()

    #ajoute les valeurs au graphe
    tfl=fl-oldfl
    if(tfl < 0):
        tfl=0
    myplot.addGraphVal(t1,t2,t3,tfl)

    #affiche le graphique
    myplot.drawGraph(50,25,400,300,85,100)
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second (unused)
    #clock.tick(60)
    
    rot = rot + 3
    if(rot > 100):
       rot = 0


    #log to file
    if(DEBUGFILE == 1):
    	#add values to our database
    	tct = int(time.time())
	if( tct != lasttct ):
    		ligne = "%d:%0.1f:%0.1f:%0.1f:%0.1f:%0.1f\n" % (tct,t1,t2,t3,t4,h4)
		try:	
			#file to log temperatures
			tfile = open("/var/tmp/temp.data", "a")
			tfile.write(ligne)	
			tfile.close()
		except IOError as e:
        	        print "Erreur fichier ", device_file," (ouverture, lecture ou fermeture)"
        	        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        	except:
        	        print "Erreur fichier ", device_file," (ouverture, lecture ou fermeture)", sys.exc_info()[0]
    		lasttct = tct

    #only sleep the time we need to respect the clock
    remainingTimeToSleep = time.time() - timestamp
    remainingTimeToSleep = 0.5 - remainingTimeToSleep

    if(remainingTimeToSleep > 0):
       time.sleep(remainingTimeToSleep)
 #   time.sleep(0.1)

#end the tasks nicely
quitApplicationNicely()

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
