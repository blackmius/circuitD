#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

from circuitImage import circuitImage

from pixelCollide import pixelCollide, getMask

import logic

mpx = lambda: mouse.get_pos()[0]
mpy = lambda: mouse.get_pos()[1]

collide = lambda x1, x2, y1, y2, w1, w2, h1, h2: x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2

def outline(image, color=(0,0,0), threshold=127):
	imgmask = mask.from_surface(image, threshold)
	
	outline_image = Surface(image.get_size()).convert_alpha()
	outline_image.fill((0,0,0,0))
	
	for point in imgmask.outline():
		outline_image.set_at(point, color)
	
	return transform.scale(outline_image, (image.get_size()[0] + 2, image.get_size()[1] + 2))

class camera:
	w1 = -1440
	h1 = -900
	w2 = 1440
	h2 = 900

	w = 1440 - 10
	h = 900 - 72
	
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

	def resize(self, window):
		self.w = window.width
		self.h = window.height

	def drawPerms(self, ox, oy, ow, oh):
		if collide(self.x, ox, self.y, oy, self.w, ow*self.zoom, self.h, oh*self.zoom):
			return True
		return False

camera = camera()

class workspace:
	def __init__(self, window):
		self.window = window
		
		self.surface = Surface((camera.w, camera.h))
		
		self.gates = []

		self.bgcolor = (219, 219, 219)
	
		self.mousepressed = False

		self.gateselected = False
		
		self.offset = 200
		
		self.gridW = 15
		
		self.gridH = 15
		
		self.grid = Surface((camera.w + self.gridW, camera.h + self.gridH)).convert_alpha()
		
		self.grid.fill((0, 0, 0, 0))
		
		for x in range(camera.w/self.gridW):
			draw.line(self.grid, (203, 203, 203), (x*self.gridW, 0), (x*self.gridW, camera.h + self.gridH))
			for y in range(camera.h/self.gridH):
				draw.line(self.grid, (203, 203, 203), (0, y*self.gridH), (camera.w + self.gridW, y*self.gridH))
				
	def resizeGrid(self, w, h):
		self.gridW = w
		
		self.gridH = h
		
		self.grid = Surface((camera.w + self.gridW, camera.h + self.gridH)).convert_alpha()
		
		self.grid.fill((0, 0, 0, 0))
		
		for x in range(camera.w/self.gridW):
			draw.line(self.grid, (203, 203, 203), (x*self.gridW, 0), (x*self.gridW, camera.h + self.gridH))
			for y in range(camera.h/self.gridH):
				draw.line(self.grid, (203, 203, 203), (0, y*self.gridH), (camera.w + self.gridW, y*self.gridH))

	def resize(self):
		self.surface = Surface((camera.w, camera.h))

	def change_offset(self, offset):
		self.offset = offset + 200

	def create_gate(self, type):
		self.gates.append(gate(type, self))

	def update(self):
		if mouse.get_pressed()[1] and not self.mousepressed:
			self.create_gate(['&', 2, 1, ['a', 'b'], ['c']])
			self.mousepressed = True
		
		for gate in range(len(self.gates)):
			
			if self.gates[gate].selected:
				if gate < len(self.gates) - 1:
					a = self.gates[len(self.gates) - 1]
					b = self.gates[gate]
					self.gates[gate] = a
					self.gates[len(self.gates) - 1] = b


			self.gates[len(self.gates)-1-gate].update()

		if mouse.get_pressed()[1] == False and self.mousepressed:
			self.mousepressed = False

	def draw(self):
		self.surface.fill(self.bgcolor)
		
		self.surface.blit(self.grid, (0 - camera.x%self.gridW, 0 - camera.y%self.gridH))
		
		for gate in self.gates:
			gate.draw()

		self.window.screen.blit(self.surface, (self.offset + 10, 36))

class gate:
	def __init__(self, type, workspace, x = None, y = None):
		self.type = type
		
		self.workspace = workspace
		
		self.x = mpx() + camera.x - self.workspace.offset if x == None else x
		self.y = mpy() + camera.y - 36 if y == None else y
		
		self.image = circuitImage(self.type[0], 32, self.type[1], self.type[2], self.type[3], self.type[4])

		self.w, self.h = self.image.get_size()
		self.outline = outline(self.image, color = (0, 121, 219))
		
		self.mouseoffset = [0, 0]
		self.pressed = False
		
		self.mousepressed = False
		
		self.selected = False
		
		self.mask = getMask(self.image)
		self.rect = Rect(self.x, self.y, self.w, self.h)

	def update(self):
		self.rect = Rect(self.x + self.workspace.offset + 10, self.y + 36, self.w, self.h)
		
		rect2 = Rect(mouse.get_pos()[0] + camera.x, mouse.get_pos()[1] + camera.y, 1, 1)
		
		if pixelCollide(self.rect, rect2, self.mask, [[True]]):
			if self.mousepressed == False:
				if self.pressed == False and mouse.get_pressed()[0] and self.workspace.gateselected == False:
					self.mouseoffset = [mouse.get_pos()[0] + camera.x - self.x, mouse.get_pos()[1] + camera.y - self.y]
					
					self.mousepressed = True
					self.pressed = True

					self.workspace.gateselected = True

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

				self.workspace.gateselected = False

		
		if mouse.get_pressed()[0]:
			self.mousepressed = True
		
		if mouse.get_pressed()[0] == False and self.mousepressed == True:
			self.mousepressed = False
				
	
	def draw(self):
		if camera.drawPerms(self.x, self.y, self.w, self.h):
			if self.selected:
				self.workspace.surface.blit(self.outline, ((self.x - camera.x - 1, self.y - camera.y - 1)))
			
			self.workspace.surface.blit(self.image, (self.x - camera.x, self.y - camera.y))
