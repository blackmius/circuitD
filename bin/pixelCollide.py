#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

def pixelCollide(rect1, rect2, mask1, mask2):
	rect = rect1.clip(rect2)
	if rect.width==0 or rect.height==0:
		return False
	
	x1,y1,x2,y2 = rect.x-rect1.x,rect.y-rect1.y,rect.x-rect2.x,rect.y-rect2.y
	
	for x in xrange(rect.width):
		for y in xrange(rect.height):
			if mask1[x1+x][y1+y] and mask2[x2+x][y2+y]:
				return True
			
			else:
				continue
   
	return False

def getMask(image):
	image.convert_alpha()
	
	mask=[]
	
	for x in range(image.get_size()[0]):
		mask.append([])
		
		for y in range(image.get_size()[1]):
			if image.get_at((x, y))[3] != 0:
				mask[x].append(True)
			else:
				mask[x].append(False)
   
	return mask
