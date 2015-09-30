#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

import time
import os
import sys

import math

if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

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

class window:
	info = display.Info()
	
	width = 640
	height = 480
	
	screen = display.set_mode((width, height))
	
	fullscreen = False

	icon = transform.scale(pygame.image.load('../data/imgs/icon.png'), (32, 32))
	display.set_icon(icon)

	display.set_caption('circuitD')
	
	def toggle_fullscreen(self):
		self.fullscreen = not self.fullscreen
		self.screen = display.set_mode((self.width, self.height), FULLSCREEN) if self.fullscreen else display.set_mode((self.width, self.height))

window = window()

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

	color = (0, 0, 0)

	info = {
		'Fps': lambda: 'FPS: ' + str(fps.get())

	}

	def toggle(self):
		self.isdraw = not self.isdraw

	def draw(self):
		if self.isdraw:
			yoffset = 0
			for i in self.info: 
				window.screen.blit(self.text.render(self.info[i](), 1, self.color), (0, yoffset*self.size))
				yoffset += 1


info = info()

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

def mainloop():
	c = circuitImage('&', 128)
	while True:
		window.screen.fill((205, 205, 205))

		window.screen.blit(c, (100, 100))
		window.screen.blit(nand, (300, 300))

		info.draw()

		events()
		
		display.update()

if __name__ == "__main__":
	mainloop()