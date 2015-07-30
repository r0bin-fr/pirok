# -*- coding: latin-1 -*-
import pygame
import pygame.gfxdraw
import math

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
BLEUNEST = (   0,  60, 236) #bleu roi nest
BLEUINT  = ( 164, 202, 255) #bleu clair 
BLEUWATER = (  63, 185, 238) #bleu "eau"
WARNING  = ( 255, 113,  45) #orange warning
PLOT1	 = ( 124, 181, 236) #bleu pastel
PLOT2 	 = ( 144, 237, 125) #vert pastel
PLOT3	 = ( 247, 163,  97) #orange pastel 

#fonction qui affiche la jauge du niveau d'eau
def drawRGauge(x,y,haut,larg,range, rmin, rmax):
	screen = pygame.display.get_surface()

#	print "range:",range,"rmin=",rmin,"rmax=",rmax
	if(range > rmin):
		range = rmin
	if(range < rmax):
		range = rmax
	
	rpercent = 1.0 - ((range - rmax) / (rmin-rmax))
	#print "Range = ",rpercent * 100,"%"	

	#gauge color
	barcolor = BLEUNEST
	if(rpercent < 0.4):
		barcolor = BLEUWATER
	if(rpercent < 0.2):
		barcolor = WARNING
	if(rpercent < 0.1):
		barcolor = RED

	#draw half round
	radius=larg/2
	haut = haut - radius
	pygame.draw.circle(screen,barcolor,[x+radius,y+haut],radius,0)
	pygame.draw.circle(screen,WHITE,[x+radius,y+haut],radius,1)
	#hide part of the round
	pygame.draw.rect(screen,BLACK, (x,y+haut-radius,larg,radius),0)
	#fill bar inside
	rangeypos = int(y+haut-(haut*rpercent))
	rangeh    = int(haut*rpercent)
	pygame.draw.rect(screen,barcolor, (x+1,rangeypos,larg-2,rangeh),0)	
	#draw bar outside
	pygame.draw.rect(screen,WHITE,(x,y,larg,haut),1)
	#remove top and bottom white bar
	pygame.draw.line(screen,BLACK, [x+1,y],[x+larg-1,y], 1)	
	pygame.draw.line(screen,barcolor, [x+1,y+haut-1],[x+larg-1,y+haut-1], 1)	

	#draw text	
	buf = "%3.0d" % int(rpercent * 100)
	buf = buf+"%"
	if(rpercent <= 0.0):
		buf = "0%"
	mafont = pygame.font.SysFont('dejavusans', 14, True, False)
        text = mafont.render(buf, True, WHITE)
        # blit to screen
        screen.blit(text, (x+5,y+haut+radius+5))


