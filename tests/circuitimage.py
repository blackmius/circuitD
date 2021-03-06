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

def circuitImage(name, size, inputs, outputs, inputsname, outputsname):
	if name != '':
		fontsize = (size-4)/2/2
		font = pygame.font.Font('../data/fonts/pixelfont.ttf', fontsize)
	
	cfontsize = int(fontsize/1.5)
	cfont = pygame.font.Font('../data/fonts/pixelfont.ttf', cfontsize)
	
	maxchrlength = 0
	
	for i in inputsname+outputsname:
		if len(i) > maxchrlength:
			maxchrlength = len(i)
	
	connectIndent = size*2/inputs if inputs > outputs else size*2/outputs
	sideIndent = connectIndent/2
	
	if size < len(name)*fontsize:
		w = len(name)*fontsize + 4 + (len(name)*fontsize)/2/2 + maxchrlength*cfontsize*2 - fontsize
	
	else:
		w = size + maxchrlength*cfontsize*2 - fontsize
	
	if inputs > outputs:
		h = inputs*connectIndent
	
	else: 
		h = outputs*connectIndent
	
	connect = Surface((fontsize, 2))
	
	surface = Surface((w + fontsize*2, h)).convert_alpha()
	surface.fill((0, 0, 0, 0))
	
	circuit = Surface((w, h)).convert_alpha()

	circuit.fill((255, 255, 255), (2, 2, w-4, h-4))

	if name != '': 
		circuit.blit(font.render(name, 0, (0, 0, 0)), (2 + (w-4)/2 - len(name)*fontsize/2, h/8/2))
	
	surface.blit(circuit, (fontsize, 0))
	
	for i in range(inputs):
		surface.blit(connect, (0, i*connectIndent + sideIndent))
		surface.blit(cfont.render(inputsname[i], 0, (0, 0, 0)), (fontsize + 3, i*connectIndent + sideIndent - cfont.size(inputsname[i])[1]/2))
	
	for o in range(outputs):
		surface.blit(connect, (w + fontsize, o*connectIndent + sideIndent))
		surface.blit(cfont.render(outputsname[o], 0, (0, 0, 0)), (fontsize + w - 3 - cfont.size(outputsname[o])[0], o*connectIndent + sideIndent - cfont.size(outputsname[o])[1]/2))
	
	return surface

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

def events():
	key = pygame.key.get_pressed()
	
	for e in event.get():
		if e.type == pygame.QUIT:
			raise SystemExit
		if e.type == KEYDOWN:
			if e.key == K_ESCAPE:
				raise SystemExit

def mainloop():
	c = circuitImage('&', 128, 3, 1, ['dasfasf', 'b', 'q'], ['dasfasf'])

	window.screen.fill((205, 205, 205))

	window.screen.blit(c, (100, 100))

	display.update()

	while True:
		events()

if __name__ == "__main__":
	mainloop()
