# -*- coding: latin-1 -*-
import pygame
import pygame.gfxdraw
import math
#import time
#from datetime import datetime
#import datetime as DT

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
BLEUNEST = (   0,  60, 236) #bleu roi nest
BLEUINT  = ( 164, 202, 255) #bleu clair 
PLOT1	 = ( 124, 181, 236) #bleu pastel
PLOT2 	 = ( 144, 237, 125) #vert pastel
PLOT3	 = ( 247, 163,  97) #orange pastel 

PI = 3.141592653
 
#fonction pour tracer un cercle plein anti-aliase
def drawAAcircle(s,x,y,d,c):
	pygame.gfxdraw.aacircle(s,x,y,d,c)
	pygame.gfxdraw.filled_circle(s,x,y,d,c)

#fonction pour tracer un arc plein
def drawMATpie(s,x,y,d,a1,a2,c):
	pygame.gfxdraw.pie(s,x,y,d,a1,a2,c)
	for ang in xrange(a1,a2):
		pygame.gfxdraw.pie(s,x,y,d,ang,ang,c)

#melangeur de couleur, du bleu au rouge
def getColorTemperature(position):
	posbasse = 100
	poshaute = 200
	blue = 255
	green = 255
	red = 255
	if(position < posbasse):
		blue = 255
		red =  255 * (position / float(posbasse))
		green = red
		green = red
	if(position > poshaute):
		red = 255
		blue = 255 * (1-((position - poshaute)/float(300-poshaute)))
		green = blue
	return (red,green,blue)


#fonction qui affiche la jauge de température
def drawGauge(nom,unite,px,py,ptemp,tmin,tmax,isPartial,isColored,textcolor):
	screen = pygame.display.get_surface()
	pdiam = 60

	# get the exact position of the slider in degree
	posit = ptemp
	if (ptemp < tmin):
		posit = tmin
	if(ptemp > tmax):
		posit = tmax
	degree = ((posit - tmin) * 300) / (tmax - tmin)
	degree = int(degree + 120)
	if(degree > 360):
		degree = degree - 360

	#draw the arc
	lowd = 60
	highd = 360
	if(isPartial):
		if(degree < 60):
			lowd = degree
		if(degree > 120):
			lowd = 0
			highd = degree
	for i in xrange (0, lowd, 6):
		if(isColored):
			gcolor = getColorTemperature(i+300-60)
		else:
			gcolor = WHITE#BLEUINT
#		pygame.gfxdraw.pie(screen,px,py,pdiam -10,i,i,gcolor)
		
	for i in xrange (120,highd,6):
		if(isColored):
                        gcolor = getColorTemperature(i-120)
                else:
                        gcolor = WHITE#BLEUINT
#		pygame.gfxdraw.pie(screen,px,py,pdiam -10,i,i,gcolor)
#	drawAAcircle(screen, px, py, pdiam-20, BLACK)
	
	#draw the current slider
	pygame.gfxdraw.pie(screen,px,py,pdiam-5,degree-2,degree+2,WHITE)
	pygame.gfxdraw.pie(screen,px,py,pdiam-5,degree-3,degree+3,WHITE)
	
	#erase the base of the pie -18
	drawAAcircle(screen, px, py, pdiam-22, BLACK)
		

	# DRAW TEMP
    	mafont = pygame.font.SysFont('dejavusans', 22, True, False) 
    	# display temperature with symbol
	buf = "%.1f" % ptemp
	buf = buf + unite #chr(176) 
    	text = mafont.render(buf, True, textcolor)#WHITE)
	# blit to screen
    	screen.blit(text, [px-(text.get_width()/2),py-(2*text.get_height()/3)])
	
	# DRAW NAME
	mafont = pygame.font.SysFont('dejavusans', 12, False, False)
        text = mafont.render(nom, True, WHITE)
        # blit to screen
        screen.blit(text, [px-(text.get_width()/2),py+(text.get_height()/2)])

	#font list
	#[u'freemono', u'droidsans', u'dejavuserif', u'robotocondensed', u'freesans', u'freeserif', u'roboto', u'dejavusansmono', u'droidserif', u'dejavusans', u'droidsansmono']

