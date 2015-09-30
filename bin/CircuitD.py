#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

pygame.init()

import gui

import time
import os
import sys

import math
import logic

get_current_second = lambda: int(time.time())
get_current_milisecond = lambda: int(round(time.time() * 1000))

collide = lambda x1, x2, y1, y2, w1, w2, h1, h2: x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2 

distance = lambda x1, y1, x2, y2: int(math.sqrt(abs(x1-x2)**2 + abs(y1-y2)**2))

percent = lambda max, percent: int(float(max)/100*percent)

mpx = lambda: mouse.get_pos()[0]
mpy = lambda: mouse.get_pos()[1]

def outline(image, color=(0,0,0), threshold=127):
    imgmask = mask.from_surface(image, threshold)
    
    outline_image = Surface(image.get_size()).convert_alpha()
    outline_image.fill((0,0,0,0))
    
    for point in imgmask.outline():
        outline_image.set_at(point, color)
    
    return transform.scale(outline_image, (image.get_size()[0] + 2, image.get_size()[1] + 2))

def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    if vertical: h = y2-y1
    else:        h = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
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

def DrawRoundRect(surface, color, rect, width, r, TL = True, TR = True, BL = True, BR = True):
	xr = yr = r
	
	clip = surface.get_clip()
	
	surface.set_clip(clip.clip(rect.inflate(0, -yr*2)))
	draw.rect(surface, color, rect.inflate(1-width,0), width)

	surface.set_clip(clip.clip(rect.inflate(-xr*2, 0)))
	draw.rect(surface, color, rect.inflate(0,1-width), width)
	
	surface.set_clip(clip.clip(rect.left, rect.top, xr, yr))
	if TL:
		draw.ellipse(surface, color, Rect(rect.left, rect.top, 2*xr, 2*yr))
	else:
		draw.rect(surface, color, Rect(rect.left, rect.top, 2*xr, 2*yr))
	
	surface.set_clip(clip.clip(rect.right-xr, rect.top, xr, yr))
	if TR:	
		draw.ellipse(surface, color, Rect(rect.right-2*xr, rect.top, 2*xr, 2*yr), width)
	else:
		draw.rect(surface, color, Rect(rect.right-2*xr, rect.top, 2*xr, 2*yr), width)
	
	surface.set_clip(clip.clip(rect.left, rect.bottom-yr, xr, yr))
	if BL:	
		draw.ellipse(surface, color, Rect(rect.left, rect.bottom-2*yr, 2*xr, 2*yr))
	else:
		draw.rect(surface, color, Rect(rect.left, rect.bottom-2*yr, 2*xr, 2*yr))
	
	surface.set_clip(clip.clip(rect.right-xr, rect.bottom-yr, xr, yr))
	if BR:
		draw.ellipse(surface, color, Rect(rect.right-2*xr, rect.bottom-2*yr, 2*xr, 2*yr), width)
	else:
		draw.rect(surface, color, Rect(rect.right-2*xr, rect.bottom-2*yr, 2*xr, 2*yr), width)

	surface.set_clip(clip)

def colorize(image, newColor):
	image = image.copy()

	image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

	return image  

def circuitImage(name, size):
	if name != '':
		fontsize = (size-4)/2/2
		font = pygame.font.Font('../data/fonts/pixelfont.ttf', fontsize)
	
	w = size
	h = size

	if w < len(name)*fontsize:
		w = len(name)*fontsize + 4

	circuit = Surface((w, h)).convert_alpha()

	circuit.fill((255, 255, 255), (2, 2, w-4, h-4))

	if name != '':
		print 
		circuit.blit(font.render(name, 0, (0, 0, 0)), (2 + (w-4)/2 - len(name)*fontsize/2, 2 + (h-4)/2 - fontsize/2))
	
	return circuit

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

class button:
	def function_example(self, x, y):
		print 'button at ({0}, {1}) was pressed'.format(x, y)
		
	def __init__(self, x, y, whereupon, obj, color = None, backlight = None, function_to_do = None, mb = 0, name = None, offsetx = 0, offsety = 0, imgnum = 0, whereuponvars = [0, 0, display.Info().current_w, display.Info().current_h]):
		if type(obj) is list:
			self.imgnum = imgnum
			self.images = obj
			self.imgtype = 'list'
			self.image = self.images[self.imgnum]
		else:
			self.image = obj
			self.imgtype = 'img'

		self.mb = mb

		self.name = name
		
		self.whereupon = whereupon

		self.whereuponW = whereuponvars[2]
		self.whereuponH = whereuponvars[3]

		self.whereuponX = whereuponvars[0]
		self.whereuponY = whereuponvars[1]
		
		self.x, self.y = x, y
		
		self.color = color if color != None else (0, 0, 0, 0)
		
		self.function_to_do = function_to_do if function_to_do != None else lambda: self.function_example(self.x, self.y)
		
		self.sizes = [self.image.get_width(), self.image.get_height()]
		
		self.backlight = None
		
		if backlight != None:
			self.backlightcolor = backlight
			self.backlight = pygame.Surface(self.sizes).convert_alpha()		
			self.backlight.fill(self.backlightcolor)
		
		self.surface = pygame.Surface(self.sizes).convert_alpha()
		
		self.surface.fill(self.color)
		
		self.target = self.image
		self.surface.blit(self.target, (0 ,0))
		
		self.pressed = False
		
		self.offsetx = offsetx

		self.offsety = offsety

		self.rect = Rect(self.x + self.whereuponX - self.offsetx, self.y + self.whereuponY - self.offsety, self.sizes[0], self.sizes[1])

	def change_whereuponvars(self, x = 0, y = 0, w = display.Info().current_w, h = display.Info().current_h):
		self.whereuponW = whereuponvars[2]
		self.whereuponH = whereuponvars[3]

		self.whereuponX = whereuponvars[0]
		self.whereuponY = whereuponvars[1]

	def change_coords(self, x = None, y = None):
		self.x = x if x != None else self.x
		self.y = y if y != None else self.y

		self.rect = Rect(self.x + self.whereuponX - self.offsetx, self.y + self.whereuponY - self.offsety, self.sizes[0], self.sizes[1])

	def change_offset(self, offx = None, offy = None):
		self.offsetx = offx if offx != None else self.offsetx
		self.offsety = offy if offy != None else self.offsety

		self.rect = Rect(self.x + self.whereuponX - self.offsetx, self.y + self.whereuponY - self.offsety, self.sizes[0], self.sizes[1])

	def change_obj(self, obj, imgnum = 0, changetype = False):
		if type(obj) is list:
			self.imgnum = imgnum
			self.images = obj
			
			if changetype:
				self.imgtype = 'list'
			
			self.image = self.images[self.imgnum]
		
		else:
			self.image = obj
			if changetype:
				self.imgtype = 'img'

		self.sizes = [self.image.get_width(), self.image.get_height()]
		self.rect = Rect(self.x + self.whereuponX - self.offsetx, self.y + self.whereuponY - self.offsety, self.sizes[0], self.sizes[1])

		self.surface = Surface(self.sizes).convert_alpha()
		self.surface.fill(self.color)
		
		self.target = self.image
		self.surface.blit(self.target, (0 ,0))

		if self.backlight != None:
			self.backlight = pygame.Surface(self.sizes).convert_alpha()		
			self.backlight.fill(self.backlightcolor)
		

	def collide(self, x, y, w, h):
		if collide(self.x + self.whereuponX - self.offsetx, x, self.y + self.whereuponY - self.offsety, y, self.sizes[0], w, self.sizes[1], h):
			return True
		return False

	def update(self):
		if self.collide(self.whereuponX, self.whereuponY, self.whereuponW, self.whereuponH):
			if self.pressed == False: 
				if onclick(self.rect, self.mb, lambda: runfunction(self.function_to_do)):
					self.pressed = True
					if self.imgtype == 'list':
						self.imgnum += 1
						
						if self.imgnum > len(self.images) - 1:
							self.imgnum = 0

						self.change_obj(self.images[self.imgnum])
		
		if pygame.mouse.get_pressed()[self.mb]:
			self.pressed = True	
		if pygame.mouse.get_pressed()[self.mb] == False and self.pressed == True:
			self.pressed = False

	def onmove(self):
		if self.collide(mouse.get_pos()[0], mouse.get_pos()[1], 1, 1):
			return True
		return False
		
	def draw(self):
		self.whereupon.blit(self.surface, (self.x - self.offsetx, self.y - self.offsety))
		if self.backlight != None:
			if self.collide(mouse.get_pos()[0], mouse.get_pos()[1], 1, 1):
				self.whereupon.blit(self.backlight, (self.x - self.offsetx, self.y - self.offsety))

class slider:
	def __init__(self, whereupon, x, y, width, height, maxoffset, sliderimg1 = None, sliderimg2 = None, offsetx = 0, offsety = 0, mp = 0, whereuponvars = [0, 0, display.Info().current_w, display.Info().current_h], state = 0, drawoffset = False, funktodo = None, startoffset = 0):
		self.x = x
		self.y = y
		
		self.state = state

		self.width = width
		self.height = height

		self.maxoffset = maxoffset

		self.offsetx = offsetx
		self.offsety = offsety

		self.drawoffset = drawoffset

		self.mp = mp

		self.funktodo = funktodo
		self.lastabsoffset = None

		if sliderimg1 != None:
			self.sliderimg1 = pygame.transform.scale(sliderimg1, (self.width, self.height))
		else:
			self.sliderimg1 = Surface((self.width, self.height))
			self.sliderimg1.fill((0, 0, 0))

		if self.state == 0:
			if sliderimg2 != None:
				self.sliderimg2 = pygame.transform.scale(sliderimg2, (self.width, self.width))
			else:
				self.sliderimg2 = Surface((self.width, self.width))
				self.sliderimg2.fill((255, 0, 0))

		else:
			if sliderimg2 != None:
				self.sliderimg2 = pygame.transform.scale(sliderimg2, (self.height, self.height))
			else:
				self.sliderimg2 = Surface((self.height, self.height))
				self.sliderimg2.fill((255, 0, 0))

		if self.drawoffset:
			if self.state == 0:
				self.font = pygame.font.Font('../data/fonts/pixelfont.ttf', self.width/2)
			else:
				self.font = pygame.font.Font('../data/fonts/pixelfont.ttf', self.height/2)


		self.surface = Surface((self.width, self.height)).convert_alpha()
		self.surface.fill((0, 0, 0, 0))

		if self.state == 0:
			self.pxperoffset = float(self.maxoffset) / (self.height - self.width)
		
		else:
			self.pxperoffset = float(self.maxoffset) / (self.width - self.height)

		self.lastmousex = None
		self.lastmousey = None

		self.whereupon = whereupon

		self.whereuponW = whereuponvars[2]
		self.whereuponH = whereuponvars[3]

		self.whereuponX = whereuponvars[0]
		self.whereuponY = whereuponvars[1]

		self.updated = False

		if startoffset != 0:
			self.absoffset = startoffset
			self.offset = self.absoffset/self.pxperoffset
		
		else:
			self.absoffset = 0
			self.offset = 0

		self.pressed = False

		self.moved = False

	def change_whereuponvars(self, x = 0, y = 0, w = display.Info().current_w, h = display.Info().current_h):
		self.whereuponW = whereuponvars[2]
		self.whereuponH = whereuponvars[3]

		self.whereuponX = whereuponvars[0]
		self.whereuponY = whereuponvars[1]

	def change_coords(self, x = None, y = None):
		self.x = x if x != None else self.x
		self.y = y if y != None else self.y

	def change_offset(self, offx = None, offy = None, absoffset = None, maxoffset = None):
		self.offsetx = offx if offx != None else self.offsetx
		self.offsety = offy if offy != None else self.offsety
		if absoffset != None:
			self.absoffset = absoffset
			self.updated = False
			self.offset = absoffset/self.pxperoffset
		
		if maxoffset != None:
			self.maxoffset = maxoffset

			if self.state == 0:
				self.pxperoffset = float(self.maxoffset) / (self.height - self.width)
			
			else:
				self.pxperoffset = float(self.maxoffset) / (self.width - self.height)

	def collide(self, x, y, w, h, slider):
		if slider:
			if collide(self.x - self.offsetx + self.whereuponX, x, self.y - self.offsety + self.whereuponY, y, self.width, w, self.height, h):
				return True
			return False
		else:
			if self.state == 0:
				if collide(self.x - self.offsetx + self.whereuponX, x, self.y - self.offsety + self.whereuponY + int(self.offset), y, self.width, w, self.width, h):
					return True
				return False
			else:
				if collide(self.x - self.offsetx + self.whereuponX + int(self.offset), x, self.y - self.offsety + self.whereuponY, y, self.height, w, self.height, h):
					return True
				return False


	def onmove(self, slider):
		if self.collide(mouse.get_pos()[0], mouse.get_pos()[1], 1, 1, slider):
			return True
		return False

	def update(self):
		if self.collide(self.whereuponX, self.whereuponY, self.whereuponW, self.whereuponH, True):
			mousepos = mouse.get_pos()

			if mouse.get_pressed()[self.mp]:
				if self.moved or not self.pressed:
					if self.onmove(False) or self.moved:
						if self.lastmousey != None and self.lastmousex != None:
							if self.state == 0:
								if self.lastmousey < mousepos[1]:
									self.offset += mousepos[1] - self.lastmousey

								if self.lastmousey > mousepos[1]:
									self.offset -= self.lastmousey - mousepos[1]

								if self.offset > self.height - self.width + 1:
									self.offset = self.height - self.width

							else:
								if self.lastmousex < mousepos[0]:
									self.offset += mousepos[0] - self.lastmousex

								if self.lastmousex > mousepos[0]:
									self.offset -= self.lastmousex - mousepos[0]

								if self.offset > self.width - self.height + 1:
									self.offset = self.width - self.height

							self.updated = False
							
							if self.offset < 0:
								self.offset = 0

							self.absoffset = self.offset * self.pxperoffset

							if self.absoffset > self.maxoffset:
								self.absoffset = self.maxoffset

						self.moved = True
						
						self.lastmousey = mousepos[1]
						self.lastmousex = mousepos[0]

				self.pressed = True
			
			else:
				self.lastmousey = None
				self.lastmousex = None

				self.pressed = False

				self.moved = False
		
		else:
			self.lastmousey = None
			self.lastmousex = None

			self.pressed = False

			self.moved = False

		if self.funktodo != None:
			if self.lastabsoffset != int(self.absoffset):
				runfunction(self.funktodo)
				self.lastabsoffset = int(self.absoffset)

	def draw(self):
		if not self.updated:
			self.surface.blit(self.sliderimg1, (0, 0))
			
			if self.state == 0:
				self.surface.blit(self.sliderimg2, (0, int(self.offset)))

			else:
				self.surface.blit(self.sliderimg2, (int(self.offset), 0))
			
			if self.drawoffset:
				offset = self.font.render(str(int(self.absoffset)), 1, (0, 0, 0))
				offsetsizes = self.font.size(str(int(self.absoffset)))
				
				if self.state == 0:
					offset = pygame.transform.rotate(offset, -90)
					coords = (self.width/2 - offsetsizes[1]/2, self.height/2 - offsetsizes[0]/2)
				
				else:
					coords = ((self.width/2 - offsetsizes[0]/2, self.height/2 - offsetsizes[1]/2))
				
				self.surface.blit(offset, coords)
			
			self.updated = True

		self.whereupon.blit(self.surface, (self.x - self.offsetx, self.y - self.offsety))

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

class window:
	info = display.Info()
	
	width = info.current_w
	height = info.current_h

	minWidth = 640
	minHeight = 480
	
	screen = display.set_mode((width, height), HWSURFACE|DOUBLEBUF|RESIZABLE)
	
	fullscreen = False

	icon = transform.scale(pygame.image.load('../data/imgs/icon.png'), (32, 32))
	display.set_icon(icon)

	display.set_caption('circuitD')
	
	def toggle_fullscreen(self):
		self.fullscreen = not self.fullscreen
		self.screen = display.set_mode((self.width, self.height), FULLSCREEN|HWSURFACE|DOUBLEBUF|RESIZABLE) if self.fullscreen else display.set_mode((self.width, self.height), HWSURFACE|DOUBLEBUF|RESIZABLE)
	
	def resize(self, size):
		self.width = size[0]
		self.height = size[1]
        
		if self.width < self.minWidth:
		    self.width = self.minWidth

		if self.height < self.minHeight:
		    self.height = self.minHeight

		self.screen = pygame.display.set_mode((self.width, self.height), HWSURFACE|DOUBLEBUF|RESIZABLE)

window = window()

class camera:
	w1 = -window.width
	h1 = -window.height
	w2 = window.width
	h2 = window.height

	w = window.width - 10
	h = window.height - 72
	
	x = 0
	y = 0
	
	zoom = 1

	speed = 2
	
	offsetbarrierwidth = 5

	lastmousex = 0
	lastmousey = 0

	def controls(self):
		key = pygame.key.get_pressed()
		mousepos = mouse.get_pos()

		mouseoffsetx = abs(mousepos[0] - self.lastmousex)
		mouseoffsety = abs(mousepos[1] - self.lastmousey)

		if mouse.get_pressed()[2]:
			if mousepos[0] > self.lastmousex:
				self.x -= mouseoffsetx 

			elif mousepos[0] < self.lastmousex:
				self.x += mouseoffsetx 

			if mousepos[1] > self.lastmousey:
				self.y -= mouseoffsety

			elif mousepos[1] < self.lastmousey:
				self.y += mouseoffsety 

		
		self.lastmousex, self.lastmousey = mousepos

		UP = False
		DOWN = False
		LEFT = False
		RIGHT = False

		if key[K_UP]:
			UP = True
	 	elif key[K_DOWN]:
	 		DOWN = True

 		if key[K_LEFT]:
 			LEFT = True
		elif key[K_RIGHT]:
			RIGHT = True

		if UP:
			if self.y - self.speed > self.h1:
				self.y -= self.speed
			else:
				self.y = self.h1
		elif DOWN:
			if self.y + self.speed < self.h2:
				self.y += self.speed
			else:
				self.y = self.h2

		if LEFT:
			if self.x - self.speed > self.w1:
				self.x -= self.speed
			else:
				self.x = self.w1
		elif RIGHT:
			if self.x + self.speed < self.w2:
				self.x += self.speed
			else:
				self.x = self.w2

	def update(self):
		self.controls()

	def resize(self):
		self.w = window.width - gui.chooseCircuitArrowsWidth
		self.h = window.height - gui.pannelHeight*2

	def drawPerms(self, ox, oy, ow, oh):
		if collide(self.x, ox, self.y, oy, self.w, ow*self.zoom, self.h, oh*self.zoom):
			return True
		return False

camera = camera()

class fps:
	clock = pygame.time.Clock()
	
	maxfps = 140
	
	def get(self):
		self.clock.tick(self.maxfps)
		
		return round(self.clock.get_fps(), 2)

fps = fps()

class info:
	isdraw = True

	size = 18

	text = pygame.font.Font('../data/fonts/pixelfont.ttf', size)

	color = (255, 255, 255)

	info = {
		'Fps': lambda: 'FPS: ' + str(fps.get()),
		'CameraPos': lambda: 'CameraPos: ' + str((camera.x, camera.y))

	}

	def toggle(self):
		self.isdraw = not self.isdraw

	def draw(self):
		if self.isdraw:
			xoffset = 0
			for i in self.info: 
				window.screen.blit(self.text.render(self.info[i](), 1, self.color), (xoffset, window.height - self.size - 9))
				xoffset += self.text.size(self.info[i]())[0]


info = info()

class space:
	surface = Surface((camera.w, camera.h))
	gates = []

	bgcolor = (219, 219, 219)
	
	mousepressed = False

	gateselected = False

	def resize(self):
		surface = Surface((camera.w, camera.h))

	def create_gate(self, type):
		self.gates.append(gate(type))

	def update(self):
		if mouse.get_pressed()[1] and not self.mousepressed:
			self.create_gate('&')
			self.mousepressed = True
		
		for gate in range(len(self.gates)):
			'''
			#выборка элементов
			if self.gates[gate].selected:
				if gate < len(self.gates) - 1:
					a = self.gates[len(self.gates) - 1]
					b = self.gates[gate]
					self.gates[gate] = a
					self.gates[len(self.gates) - 1] = b
			'''

			self.gates[len(self.gates)-1-gate].update()

		if mouse.get_pressed()[1] == False and self.mousepressed:
			self.mousepressed = False

	def draw(self):
		self.surface.fill(self.bgcolor)

		for gate in self.gates:
			gate.draw()

		window.screen.blit(self.surface, (gui.chooseCircuitOffset + gui.chooseCircuitWidth + gui.chooseCircuitArrowsWidth, gui.pannelHeight))

space = space()

class gate:
	def __init__(self, type):
		self.type = type
		
		self.x = mpx() + camera.x - (gui.chooseCircuitOffset + gui.chooseCircuitWidth + gui.chooseCircuitArrowsWidth)
		self.y = mpy() + camera.y - gui.pannelHeight
		
		self.image = circuitImage(self.type, 64)

		self.w, self.h = self.image.get_size()
		self.outline = outline(self.image, color = (0, 121, 219))
		
		self.mouseoffset = [0, 0]
		self.pressed = False
		
		self.mousepressed = False
		
		self.selected = False

	def update(self):
		if collide(self.x + gui.chooseCircuitOffset + gui.chooseCircuitWidth + gui.chooseCircuitArrowsWidth, mouse.get_pos()[0] + camera.x, self.y + gui.pannelHeight, mouse.get_pos()[1] + camera.y, self.w, 1, self.h, 1):
			if self.mousepressed == False:
				if self.pressed == False and mouse.get_pressed()[0] and space.gateselected == False:
					self.mouseoffset = [mouse.get_pos()[0] + camera.x - self.x, mouse.get_pos()[1] + camera.y - self.y]
					
					self.mousepressed = True
					self.pressed = True

					space.gateselected = True

					self.selected = True
		else:
			if mouse.get_pressed()[0]:
				self.selected = False


		if self.pressed == True:			
			if mouse.get_pressed()[0]:
				self.mousepressed = True
				self.pressed = True
				self.selected = True

				self.x = mouse.get_pos()[0] + camera.x - self.mouseoffset[0]
				self.y = mouse.get_pos()[1] + camera.y - self.mouseoffset[1]
			else:
				self.pressed = False

				space.gateselected = False

		
		if mouse.get_pressed()[0]:
			self.mousepressed = True
		
		if mouse.get_pressed()[0] == False and self.mousepressed == True:
			self.mousepressed = False
				
	
	def draw(self):
		if camera.drawPerms(self.x, self.y, self.w, self.h):
			if self.selected:
				space.surface.blit(self.outline, ((self.x - camera.x - 1, self.y - camera.y - 1)))
			
			space.surface.blit(self.image, (self.x - camera.x, self.y - camera.y))

class gui:
	chooseCircuitWidth = 200
	chooseCircuitHeight = window.height - 72
	
	chooseCircuitOffset = 0
	chooseCircuitOffsetTo = chooseCircuitOffset

	chooseCircuitMoveSpeed = 10

	chooseCircuitSurface = Surface((chooseCircuitWidth, chooseCircuitHeight)).convert_alpha()
	chooseCircuitSurface.fill((208, 214, 219, 255))

	chooseCircuitArrowsWidth = 10
	chooseCircuitArrowsHeight = 124
	
	chooseCircuitArrowsBg = Surface((chooseCircuitArrowsWidth+2, chooseCircuitHeight))

	chooseCircuitArrowsImg2 = transform.scale(image.load('../data/imgs/arrowbutton.png'), (chooseCircuitArrowsWidth, chooseCircuitArrowsHeight))
	chooseCircuitArrowsImg1 = transform.flip(chooseCircuitArrowsImg2, True, False)

	chooseCircuitArrows = button(chooseCircuitWidth+1, chooseCircuitHeight/2 - chooseCircuitArrowsHeight/2, window.screen, [chooseCircuitArrowsImg1, chooseCircuitArrowsImg2], imgnum = 0 if chooseCircuitOffset == 0 - chooseCircuitWidth else 1, function_to_do = 'gui.changeChooseCircuitOffset()', backlight = (255, 255, 255, 30))

	circuitSurface = Surface((chooseCircuitWidth - 15, chooseCircuitHeight)).convert_alpha()
	circuitSurface.fill((0, 0, 0, 0))

	circuits = 0

	chooseCircuitSliderWidth = 15
	chooseCircuitSliderHeight = chooseCircuitHeight
	chooseCircuitSliderX = chooseCircuitOffset + chooseCircuitWidth - chooseCircuitSliderWidth
	chooseCircuitSliderY = 36
	chooseCircuitSliderMaxoffset = 100

	chooseCircuitSlider = slider(window.screen, chooseCircuitSliderX, chooseCircuitSliderY, chooseCircuitSliderWidth, chooseCircuitSliderHeight, chooseCircuitSliderMaxoffset, funktodo = 'gui.changeChooseCircuitOffsetY()')

	chooseCircuitOffsetY = 0

	mousepressed = False

	pannelWidth = window.width
	pannelHeight = 36

	topPannel = Surface((pannelWidth, pannelHeight))
	bottomPannel = Surface((pannelWidth, pannelHeight))

	pannelBg = Surface((pannelWidth, pannelHeight))
	fill_gradient(pannelBg, (60, 60, 60), (15, 15, 13), Rect(0, 1, pannelWidth, pannelHeight-2))

	topPannel.blit(pannelBg, (0, 0))
	bottomPannel.blit(pannelBg, (0, 0))

	def resize(self):
		self.chooseCircuitHeight = window.height - 72

		self.chooseCircuitSurface = Surface((self.chooseCircuitWidth, self.chooseCircuitHeight)).convert_alpha()
		self.chooseCircuitSurface.fill((208, 214, 219, 255))
		
		self.chooseCircuitArrowsBg = Surface((self.chooseCircuitArrowsWidth+2, self.chooseCircuitHeight))

		self.chooseCircuitArrows = button(self.chooseCircuitWidth+1, self.chooseCircuitHeight/2 - self.chooseCircuitArrowsHeight/2, window.screen, [self.chooseCircuitArrowsImg1, self.chooseCircuitArrowsImg2], imgnum = 0 if self.chooseCircuitOffset == 0 - self.chooseCircuitWidth else 1, function_to_do = 'gui.changeChooseCircuitOffset()', backlight = (255, 255, 255, 30))

		self.circuitSurface = Surface((self.chooseCircuitWidth - 15, self.chooseCircuitHeight)).convert_alpha()
		self.circuitSurface.fill((0, 0, 0, 0))

		self.chooseCircuitSliderHeight = self.chooseCircuitHeight

		self.chooseCircuitSlider = slider(window.screen, self.chooseCircuitSliderX, self.chooseCircuitSliderY, self.chooseCircuitSliderWidth, self.chooseCircuitSliderHeight, self.chooseCircuitSliderMaxoffset, funktodo = 'gui.changeChooseCircuitOffsetY()')

		self.pannelWidth = window.width

		self.topPannel = Surface((self.pannelWidth, self.pannelHeight))
		self.bottomPannel = Surface((self.pannelWidth, self.pannelHeight))

		self.pannelBg = Surface((self.pannelWidth, self.pannelHeight))
		fill_gradient(self.pannelBg, (60, 60, 60), (15, 15, 13), Rect(0, 1, self.pannelWidth, self.pannelHeight-2))

		self.topPannel.blit(self.pannelBg, (0, 0))
		self.bottomPannel.blit(self.pannelBg, (0, 0))

		self.chooseCircuitArrows.change_coords(x = self.chooseCircuitOffset + self.chooseCircuitWidth + 1)
		self.chooseCircuitSlider.change_coords(x = self.chooseCircuitOffset + self.chooseCircuitWidth - percent(self.chooseCircuitWidth - self.chooseCircuitWidth/4, 10))


	def changeChooseCircuitOffset(self):
		self.chooseCircuitOffsetTo = self.chooseCircuitOffset - self.chooseCircuitWidth if not self.chooseCircuitOffset - self.chooseCircuitWidth < 0 - 360 else 0
	
	def changeChooseCircuitOffsetY(self):
		self.chooseCircuitOffsetY = self.chooseCircuitSlider.absoffset

	def update(self):
		if self.chooseCircuitOffset != self.chooseCircuitOffsetTo:
			if self.chooseCircuitOffset < self.chooseCircuitOffsetTo:
				self.chooseCircuitOffset += self.chooseCircuitWidth/self.chooseCircuitMoveSpeed
				
				if self.chooseCircuitOffset > self.chooseCircuitOffsetTo:
					self.chooseCircuitOffset = self.chooseCircuitOffsetTo
			
			else:
				self.chooseCircuitOffset -= self.chooseCircuitWidth/self.chooseCircuitMoveSpeed
				if self.chooseCircuitOffset < self.chooseCircuitOffsetTo:
					self.chooseCircuitOffset = self.chooseCircuitOffsetTo

			self.chooseCircuitArrows.change_coords(x = self.chooseCircuitOffset + self.chooseCircuitWidth + 1)
			self.chooseCircuitSlider.change_coords(x = self.chooseCircuitOffset + self.chooseCircuitWidth - percent(self.chooseCircuitWidth - self.chooseCircuitWidth/4, 10))
		
		else:
			self.chooseCircuitArrows.update()
			self.chooseCircuitSlider.update()

		space.update()

	
	def draw(self):
		space.draw()

		window.screen.blit(self.chooseCircuitSurface, (self.chooseCircuitOffset, self.pannelHeight))
		window.screen.blit(self.chooseCircuitArrowsBg, (self.chooseCircuitOffset + self.chooseCircuitWidth, self.pannelHeight))

		self.chooseCircuitArrows.draw()
		self.chooseCircuitSlider.draw()
		
		window.screen.blit(self.circuitSurface, (self.chooseCircuitOffset, self.pannelHeight))
		window.screen.blit(self.topPannel, (0, 0))
		window.screen.blit(self.bottomPannel, (0, window.height - self.pannelHeight))

gui = gui()

class cursor:
	mouse.set_visible(False)

	width = 16
	height = 20
	
	cursors = [pygame.transform.scale(pygame.image.load('../data/imgs/cursors/' + str(i) + '.png'), (width, height)) for i in range(len(os.listdir('../data/imgs/cursors/')))]
	cursor = 0

	img = Surface((width, height)).convert_alpha()
	img.fill((0, 0, 0, 0))
	img.blit(cursors[cursor], (0, 0))

	x = 0
	y = 0

	lastx = None
	lasty = None

	def changeCursor(self, cursor):
		self.cursor = cursor

		self.img = Surface((self.width, self.height)).convert_alpha()
		self.img.fill((0, 0, 0, 0))
		self.img.blit(self.cursors[self.cursor], (0, 0))
		
	def update(self):
		self.x, self.y = mouse.get_pos()

		if self.lasty != self.y:
			self.lasty = self.y

		if self.lastx != self.x:
			self.lastx = self.x

	def draw(self):
		window.screen.blit(self.img, (self.x, self.y))

cursor = cursor()

def events():
	key = pygame.key.get_pressed()
	
	for e in event.get():
		if e.type == pygame.QUIT:
			raise SystemExit
		
		if e.type == KEYDOWN:
			if e.key == K_F11:
				window.toggle_fullscreen()
			elif e.key == K_F10:
				image.save(window.screen, os.path.join("../"+"screenshots/")+time.strftime("%d_%b_%Y+%H_%M_%S.png", time.localtime()))
			elif e.key == K_F3:
				info.toggle()
			elif e.key == K_ESCAPE:
				raise SystemExit
			else:
				event.post(e)

		elif e.type==VIDEORESIZE:
			window.resize(e.size)
			gui.resize()
			camera.resize()
			space.resize()

	camera.update()

def mainloop():
	b = []
	while True:
		window.screen.fill((255, 255, 255))

		gui.update()
		gui.draw()

		for i in b:
			i.update()
			i.draw()

		info.draw()

		cursor.update()
		cursor.draw()

		events()
		
		display.update()

if __name__ == "__main__":
	mainloop()