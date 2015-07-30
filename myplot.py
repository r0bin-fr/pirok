# -*- coding: latin-1 -*-
import pygame
import pygame.gfxdraw
import math
#import time
#from datetime import datetime
#import datetime as DT
from collections import deque

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
PLOT4    = ( 169, 248, 252) #bleu très clair
GRILLE	 = (  72,  72,  72)

PI = 3.141592653
 
#font list
#[u'freemono', u'droidsans', u'dejavuserif', u'robotocondensed', u'freesans', u'freeserif', u'roboto', u'dejavusansmono', u'droidserif', u'dejavusans', u'droidsansmono']

#3 listes de donnees
tdata = [deque(),deque(),deque(),deque()]
maxdata = 100
def addGraphVal(v1,v2,v3,v4):
	#si le tableau est plein, on decale les donnees
	if(len(tdata[0]) >= maxdata):
		tdata[0].pop()
		tdata[1].pop()
		tdata[2].pop()
		tdata[3].pop()
        #ajouter les valeurs dans les donnees
	tdata[0].appendleft(v1)
	tdata[1].appendleft(v2)
	tdata[2].appendleft(v3)
	tdata[3].appendleft(v4)


def getValTranslated(val,minv,maxv,y,h):
	return int((((1-((val-minv)/float(maxv-minv)))*h)+y))
#getvaltr(   0 -10 85 25 300 ) zeropos= 25
#drawcircle 32 -10 52 25 300 -9323

def drawGraph(x,y,larg,haut,blow,bhigh):
	screen = pygame.display.get_surface()
	stepdata = (larg/maxdata)
	stepx = stepdata * 10 #toutes les 5 secondes
	stepy = 1 #tous les 10 degres

	lend=len(tdata[0])
	if(lend == 0):
		return

	maxval = int(max(max(tdata[0]),max(tdata[1]),max(tdata[2])))
	minval = int(min(min(tdata[0]),min(tdata[1]),min(tdata[2])))
	if( (maxval-minval) < (stepy) ):
		maxval = maxval + stepy 
		minval = minval - stepy
#		maxval = maxval - (maxval % stepy)+stepy 
#		minval = minval - (minval % stepy)
#		stepy = int((maxval-minval) / 4)
		
#	maxval = bhigh
#	minval = blow

	#ligne verticale, toujours au meme endroit
	pygame.gfxdraw.vline(screen,x,y,y+haut,WHITE)

	if(minval >= 0):
		zeropos=y+haut
	if(minval < 0):
		zeropos=getValTranslated(0,minval,maxval,y,haut) #((1-(0-minval/(maxval-minval)))*haut)+y

	#affichage de la legende et grille
        mafont = pygame.font.SysFont('dejavusans', 12, True, False)
	
	#lignes hozizontales
	for i in xrange(minval,maxval):
		if((i % stepy) == 0):
			ligney = getValTranslated(i,minval,maxval,y,haut)
			pygame.gfxdraw.hline(screen,x,x+larg,ligney,GRILLE)
			text = mafont.render(str(i) + chr(176), True, WHITE)
        		screen.blit(text, [x-text.get_width(),ligney-text.get_height()])
	pygame.gfxdraw.hline(screen,x,x+larg,y,GRILLE)

	#lignes verticales
	ts = 0
	for i in xrange(x+larg,x,-stepx):
		pygame.gfxdraw.vline(screen,i,y+haut,y,GRILLE)
		text = mafont.render(str(ts)+"s", True, WHITE)
       		screen.blit(text, [i-text.get_width()/2,y+haut])
		ts = ts + ((stepx/stepdata) / 2)

	#ligne horizontale, selon la position du zero
	pygame.gfxdraw.hline(screen,x,x+larg,zeropos,WHITE)
			
	#dessin des plots et lignes
	oldpy1 = 0
	oldpy2 = 0
	oldpy3 = 0
	oldpy4 = 0
	for mval in xrange(0,lend):
		px = (x+larg)-(mval*stepdata)
		#gestion des températures
		py1=getValTranslated(tdata[0][mval],minval,maxval,y,haut)
		py2=getValTranslated(tdata[1][mval],minval,maxval,y,haut)
		py3=getValTranslated(tdata[2][mval],minval,maxval,y,haut)
		#gestion du flowmeter
		py4=tdata[3][mval]
		#if(py4 > 6):  #6ml maxi
		#	py4 = 6 
		py4=int((y+haut)-((haut * py4) / 6))
		#tracé de ronds (pour la valeur actuelle)
		if(mval == 0):
			pygame.gfxdraw.filled_circle(screen,px,py1,2,PLOT1)
			pygame.gfxdraw.filled_circle(screen,px,py2,2,PLOT2)
			pygame.gfxdraw.filled_circle(screen,px,py3,2,PLOT3)
			pygame.gfxdraw.filled_circle(screen,px,py4,2,PLOT4)
		#tracé de droites (pour les anciennes valeurs)
		if(mval > 0):
			pygame.gfxdraw.line(screen,px,oldpy1,px-stepdata,py1,PLOT1)	
			pygame.gfxdraw.line(screen,px,oldpy2,px-stepdata,py2,PLOT2)	
			pygame.gfxdraw.line(screen,px,oldpy3,px-stepdata,py3,PLOT3)	
			pygame.gfxdraw.line(screen,px,oldpy4,px-stepdata,py4,PLOT4)	
		oldpy1 = py1
	        oldpy2 = py2
        	oldpy3 = py3
		oldpy4 = py4

