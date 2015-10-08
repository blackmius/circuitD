#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

get_current_second = lambda: int(time.time())
get_current_milisecond = lambda: int(round(time.time() * 1000))

collide = lambda x1, x2, y1, y2, w1, w2, h1, h2: x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2 

def runfunction(function):
	if type(function) is str:
		eval(function)
	elif type(function) is tuple or type(function) is list:
		for i in function:
			runfunction(function)
	else:
		function()
		
def onclick(rect, button, function):
	if collide(rect[0], mouse.get_pos()[0], rect[1], mouse.get_pos()[1], rect[2], 1, rect[3], 1) and mouse.get_pressed()[button]:
		runfunction(function)
		return True
	return False





class inputbox:
	def __init__(self, x, y, width, height, whereupon, image = None, fontsize = 24, mode = 'INPUT', textposition = 'CENTER', offsetx = 0, offsety = 0, whereuponvars = [0, 0, display.Info().current_w, display.Info().current_h], textoffset = 0, textcolor = (0, 0, 0), borders = [0, 0, None, None], backlight = None, maxchars = None, funktodo = None, starttext = ''):
		self.mode = mode

		self.text = starttext
		self.lasttext = starttext

		self.maxchars = maxchars

		if starttext != None and self.mode == 'KEY':
			self.key = starttext
			self.lastkey = starttext

		self.updated = False

		self.image = image
		
		self.whereupon = whereupon

		self.x = x
		self.y = y

		self.offsetx = offsetx
		self.offsety = offsety

		self.width = width
		self.height = height

		self.whereuponX = whereuponvars[0]
		self.whereuponY = whereuponvars[1]

		self.whereuponW = whereuponvars[2]
		self.whereuponH = whereuponvars[3]

		self.textposition = textposition
		self.textoffset = textoffset

		self.textcolor = textcolor

		self.textbX = borders[0]
		self.textbY = borders[1]

		self.textbW = borders[2] if borders[2] != None else self.width
		self.textbH = borders[3] if borders[3] != None else self.height

		self.border = Surface((self.textbW, self.textbH)).convert_alpha()

		self.fontsize = fontsize
		self.font = font.Font('../data/fonts/pixelfont.ttf', self.fontsize)

		if self.image != None:
			self.surface = Surface((self.width, self.height)).convert_alpha()
			self.surface.fill((0, 0, 0, 0))		 
		else:
			self.surface = Surface((self.width, self.height))

		self.backlight = backlight
		if self.backlight != None:
			self.backlightsurf = Surface((self.width, self.height)).convert_alpha()
			self.backlightsurf.fill(self.backlight)

		self.lastmls = get_current_milisecond()

		self.shifted = False
		self.capslock = False

		self.pressedtime = 400

		self.entered = False

		self.funktodo = funktodo

	def change_whereuponvars(self, x = 0, y = 0, w = display.Info().current_w, h = display.Info().current_h):
		self.whereuponW = whereuponvars[2]
		self.whereuponH = whereuponvars[3]

		self.whereuponX = whereuponvars[0]
		self.whereuponY = whereuponvars[1]
		
	def collide(self, x, y, w, h):
		if collide(self.x + self.whereuponX - self.offsetx, x, self.y + self.whereuponY - self.offsety, y, self.width, w, self.height, h):
			return True
		return False

	def onmove(self):
		if self.collide(mouse.get_pos()[0], mouse.get_pos()[1], 1, 1):
			return True
		return False

	def change_coords(self, x = None, y = None):
		self.x = x if x != None else self.x
		self.y = y if y != None else self.y

	def change_offset(self, offx = None, offy = None):
		self.offsetx = offx if offx != None else self.offsetx
		self.offsety = offy if offy != None else self.offsety
	
	def change_text(self, text):
		self.text = text
		self.updated = False
	
	def update(self):
		key = pygame.key.get_pressed()

		if self.onmove():
			if mouse.get_pressed()[0]:
				self.entered = True
		else:
			if mouse.get_pressed()[0]:
				self.entered = False

		if self.entered:
			if self.mode == 'INPUT' or self.mode == 'NUM ONLY' or self.mode == 'CHR ONLY':			  
				event = pygame.event.poll()
				
				if event.type == KEYDOWN:
					if event.key == K_BACKSPACE:
						self.text = self.text[:-1]

					elif event.key == K_RETURN or event.key == K_KP_ENTER:
						self.entered = False
						self.updated = False
					
					elif self.mode == 'INPUT':
						self.text += event.unicode

					elif self.mode == 'NUM ONLY':
						self.text = self.text + event.unicode if event.unicode.isdigit() else self.text

					elif self.mode == 'CHR ONLY':
						self.text = self.text + event.unicode if event.unicode.isalpha() else self.text
					
					self.key = (event.key, event.unicode)
					self.lastmls = get_current_milisecond()

				else:
					pygame.event.post(event)
				

				if get_current_milisecond() - self.lastmls > self.pressedtime:
					if self.text != '':
						try:
							if key[self.key[0]]:
								if self.key[0] == K_BACKSPACE:
									self.text = self.text[:-1]
								
								elif self.mode == 'INPUT':
									self.text += self.key[1]

								elif self.mode == 'NUM ONLY':
									self.text = self.text + self.key[1] if self.key[1].isdigit() else self.text

								elif self.mode == 'CHR ONLY':
									self.text = self.text + self.key[1] if self.key[1].isalpha() else self.text
								
								self.pressedtime = 100
							
							else:
								self.pressedtime = 400
						except:
							pass

					self.lastmls = get_current_milisecond()

				if self.maxchars != None:
					if len(self.text) > self.maxchars:
						self.text = self.text[:-1]
				
				if self.lasttext != self.text:
					self.updated = False
					
					self.lasttext = self.text
			
			if self.mode == 'KEY':
				event = pygame.event.poll()

				if event.type == KEYDOWN:
					self.key = event.key
					self.entered = False
				
				else:
					pygame.event.post(event) 
				
				if self.lastkey != self.key:
					self.updated = False
					
					self.lastkey = self.key
		if not self.updated and self.entered == False:
			runfunction(self.funktodo)


	def draw(self):
		if not self.updated:
			if self.image == None:
				self.surface.fill((0, 0, 0))
			else:
				self.surface.blit(self.image, (0, 0))

			self.border.fill((0, 0, 0, 0))
			
			if self.mode == 'INPUT' or self.mode == 'NUM ONLY' or self.mode == 'CHR ONLY':
				self.fontsize = self.textbH
				
				if self.textbW < len(self.text)*self.textbH:
					self.fontsize = self.textbW/len(self.text)
				
				self.font = font.Font('../data/fonts/pixelfont.ttf', self.fontsize)
				
				if self.textposition == 'CENTER':
					x = self.textbW/2-(len(self.text)*self.fontsize)/2 - self.textoffset

				elif self.textposition == 'LEFT':
					x = 0 - self.textoffset

				elif self.textposition == 'RIGHT':
					x = self.textbW - (len(self.text)*self.fontsize) - self.textoffset
				
				self.border.blit(self.font.render(self.text, 1, self.textcolor), (x, self.textbH/2-self.fontsize/2))
		
			if self.mode == 'KEY':
				if self.key != None:
					name = pygame.key.name(self.key)
					self.fontsize = self.textbH
					
					if self.textbW < len(name)*self.textbH:
						self.fontsize = self.textbW/len(name)
					
					self.font = font.Font('../data/fonts/pixelfont.ttf', self.fontsize)

					if self.textposition == 'CENTER':
						x = self.textbW/2-(len(name)*self.fontsize)/2 - self.textoffset

					elif self.textposition == 'LEFT':
						x = 0 - self.textoffset

					elif self.textposition == 'RIGHT':
						x = self.textbW - (len(name)*self.fontsize)/2 - self.textoffset
					
					self.border.blit(self.font.render(name, 1, self.textcolor), (x, self.textbH/2-self.fontsize/2))

			self.surface.blit(self.border, (self.textbX, self.textbY))
			
			self.updated = True

		self.whereupon.blit(self.surface, (self.x - self.offsetx, self.y - self.offsety))

		if self.backlight != None:
			if self.entered:
				self.whereupon.blit(self.backlightsurf, (self.x - self.offsetx, self.y - self.offsety))
