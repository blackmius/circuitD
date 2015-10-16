#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

def circuitImage(name, size, inputs, outputs, inputsname, outputsname): 
	if len(inputsname) < inputs:
		inputsname += ['' for i in range(inputs - len(inputsname))]
	
	if len(outputsname) < outputs:
		outputsname += ['' for o in range(outputs - len(outputsname))]
	
	if name != '':
		fontsize = (size-4)/2
		font = pygame.font.Font('../data/fonts/gost.ttf', fontsize)
	
	cfontsize = int(fontsize/1.5)
	cfont = pygame.font.Font('../data/fonts/gost.ttf', cfontsize)
	
	maxchrlength = 0
	
	for i in inputsname+outputsname:
		if len(i) > maxchrlength:
			maxchrlength = len(i)
	
	if inputs > outputs:
		connectIndent = size*2/inputs
 	
 	else:
 		connectIndent = size*2/outputs

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
		circuit.blit(font.render(name, 0, (0, 0, 0)), (w/2 - font.size(name)[0]/2, h/8/2))
	
	surface.blit(circuit, (fontsize, 0))
	
	for i in range(inputs):
		surface.blit(connect, (0, i*connectIndent + sideIndent))
		surface.blit(cfont.render(inputsname[i], 0, (0, 0, 0)), (fontsize + 3, i*connectIndent + sideIndent - cfont.size(inputsname[i])[1]/2))
	
	for o in range(outputs):
		surface.blit(connect, (w + fontsize, o*connectIndent + sideIndent))
		surface.blit(cfont.render(outputsname[o], 0, (0, 0, 0)), (fontsize + w - 3 - cfont.size(outputsname[o])[0], o*connectIndent + sideIndent - cfont.size(outputsname[o])[1]/2))
	
	return surface
