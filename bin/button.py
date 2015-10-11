#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

import time 

get_current_second = lambda: int(time.time())
get_current_milisecond = lambda: int(round(time.time() * 1000))

collide = lambda x1, x2, y1, y2, w1, w2, h1, h2: x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2 


def onclick(rect, button):
    if collide(rect[0], mouse.get_pos()[0], rect[1], mouse.get_pos()[1], rect[2], 1, rect[3], 1) and mouse.get_pressed()[button]:
        return True
    return False

class button:    
    def __init__(self, x, y, whereupon, obj, color = None, backlight = None, mb = 0, name = None, offsetx = 0, offsety = 0, imgnum = 0, whereuponvars = [0, 0, display.Info().current_w, display.Info().current_h]):
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
        self.whereuponW = w
        self.whereuponH = h

        self.whereuponX = x
        self.whereuponY = y

        self.rect = Rect(self.x + self.whereuponX - self.offsetx, self.y + self.whereuponY - self.offsety, self.sizes[0], self.sizes[1])
    

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
                if onclick(self.rect, self.mb):
                    
                    self.pressed = True
                    
                    if self.imgtype == 'list':
                        self.imgnum += 1
                        
                        if self.imgnum > len(self.images) - 1:
                            self.imgnum = 0

                        self.change_obj(self.images[self.imgnum])
                    
                    return True
            
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
