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