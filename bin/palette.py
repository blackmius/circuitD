#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

from button import button
from slider import slider

percent = lambda max, percent: int(float(max)/100*percent)

class palette:
    def __init__(self, window):
        self.window = window
        
        self.width = 200
        self.height = self.window.height - 72
    
        self.offset = 0
        self.offsetTo = self.offset

        self.moveSpeed = 10

        self.surface = Surface((self.width, self.height)).convert_alpha()
        self.surface.fill((208, 214, 219, 255))

        self.arrowsWidth = 10
        self.arrowsHeight = 124
    
        self.arrowsBg = Surface((self.arrowsWidth+2, self.height))

        self.arrowsImg2 = transform.scale(image.load('../data/imgs/arrowbutton.png'), (self.arrowsWidth, self.arrowsHeight))
        self.arrowsImg1 = transform.flip(self.arrowsImg2, True, False)

        self.arrows = button(self.width+1, self.height/2 - self.arrowsHeight/2, window.screen, [self.arrowsImg1, self.arrowsImg2], imgnum = 0 if self.offset == 0 - self.width else 1, backlight = (255, 255, 255, 30))

        self.circuitSurface = Surface((self.width - 15, self.height)).convert_alpha()
        self.circuitSurface.fill((0, 0, 0, 0))

        self.circuits = 0

        self.sliderWidth = 15
        self.sliderHeight = self.height
        self.sliderX = self.offset + self.width - self.sliderWidth
        self.sliderY = 36
        self.sliderMaxoffset = 100

        self.slider = slider(window.screen, self.sliderX, self.sliderY, self.sliderWidth, self.sliderHeight, self.sliderMaxoffset)

        self.offsetY = 0

        self.mousepressed = False

        self.pannelWidth = 640
        self.pannelHeight = 36
        
        self.offsetreturn = self.offset
        self.pastoffsetreturn = self.offset

    def resize(self):
        self.width = 200

        self.height = self.window.height - 72

        self.surface = Surface((self.width, self.height)).convert_alpha()
        self.surface.fill((208, 214, 219, 255))

        self.arrowsBg = Surface((self.arrowsWidth+2, self.height))

        self.arrows = button(self.width+1, self.height/2 - self.arrowsHeight/2, self.window.screen, [self.arrowsImg1, self.arrowsImg2], imgnum = 0 if self.offset == 0 - self.width else 1, backlight = (255, 255, 255, 30))

        self.circuitSurface = Surface((self.width - 15, self.height)).convert_alpha()
        self.circuitSurface.fill((0, 0, 0, 0))

        self.sliderHeight = self.height

        self.slider = slider(self.window.screen, self.sliderX, self.sliderY, self.sliderWidth, self.sliderHeight, self.sliderMaxoffset)

        self.arrows.change_coords(x = self.offset + self.width + 1)
        self.slider.change_coords(x = self.offset + self.width - percent(self.width - self.width/4, 10))

    def changeOffset(self):
        self.offsetTo = self.offset - self.width if not self.offset - self.width < 0 - 360 else 0
    
    def changeOffsetY(self):
        self.offsetY = self.slider.absoffset

    def update(self):
        if self.offset != self.offsetTo:
            if self.offset < self.offsetTo:
                self.offset += self.width/self.moveSpeed
                
                if self.offset > self.offsetTo:
                    self.offset = self.offsetTo
            
            else:
                self.offset -= self.width/self.moveSpeed
                if self.offset < self.offsetTo:
                    self.offset = self.offsetTo
            
            self.offsetreturn = self.offset
            self.arrows.change_coords(x = self.offset + self.width + 1)
            self.slider.change_coords(x = self.offset + self.width - percent(self.width - self.width/4, 10))
        
        else:
            if self.arrows.update():
                self.changeOffset()
            
            if self.slider.update():
                self.changeOffsetY()
        
        if self.pastoffsetreturn != self.offsetreturn:
            self.pastoffsetreturn = self.offsetreturn
            
            return self.offsetreturn

    
    def draw(self, whereupon):
        self.window.screen.blit(self.surface, (self.offset, self.pannelHeight))
        self.window.screen.blit(self.arrowsBg, (self.offset + self.width, self.pannelHeight))

        self.arrows.draw()
        self.slider.draw()
        
        self.window.screen.blit(self.circuitSurface, (self.offset, self.pannelHeight))