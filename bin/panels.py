#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
	if rect is None: rect = surface.get_rect()
	x1,x2 = rect.left, rect.right
	y1,y2 = rect.top, rect.bottom
	if vertical: h = y2-y1
	else:		h = x2-x1
	if forward: a, b = color, gradient
	else:	   b, a = color, gradient
	rate = (
		float(b[0]-a[0])/h,
		float(b[1]-a[1])/h,
		float(b[2]-a[2])/h
	)
	fn_line = pygame.draw.line
	if vertical:
		for line in range(y1,y2):
			color = (
				min(max(a[0]+(rate[0]*(line-y1)),0),255),
				min(max(a[1]+(rate[1]*(line-y1)),0),255),
				min(max(a[2]+(rate[2]*(line-y1)),0),255)
			)
			fn_line(surface, color, (x1,line), (x2,line))
	else:
		for col in range(x1,x2):
			color = (
				min(max(a[0]+(rate[0]*(col-x1)),0),255),
				min(max(a[1]+(rate[1]*(col-x1)),0),255),
				min(max(a[2]+(rate[2]*(col-x1)),0),255)
			)
			fn_line(surface, color, (col,y1), (col,y2))

class panels:
    def __init__(self, window):
        self.window = window
        
        self.panelWidth = self.window.width
        self.panelHeight = 36
        
        self.panelBg = Surface((self.panelWidth, self.panelHeight))
        
        self.panel1 = Surface((self.panelWidth, self.panelHeight))
        self.panel2 = Surface((self.panelWidth, self.panelHeight))
        
        fill_gradient(self.panelBg, (60, 60, 60), (15, 15, 13))
        
        self.panel1.blit(self.panelBg, (0, 0))
        self.panel2.blit(self.panelBg, (0, 0))
    
    def resize(self):
        self.panelWidth = self.window.width
        
        self.panelBg = Surface((self.panelWidth, self.panelHeight))
        
        self.panel1 = Surface((self.panelWidth, self.panelHeight))
        self.panel2 = Surface((self.panelWidth, self.panelHeight))
        
        fill_gradient(self.panelBg, (60, 60, 60), (15, 15, 13))
        
        self.panel1.blit(self.panelBg, (0, 0))
        self.panel2.blit(self.panelBg, (0, 0))
        
    def draw(self):
        self.window.screen.blit(self.panel1, (0, 0))
        
        self.window.screen.blit(self.panel2, (0, self.window.height - self.panelHeight))
        
