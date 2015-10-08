#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

import time

get_current_second = lambda: int(time.time())
get_current_milisecond = lambda: int(round(time.time() * 1000))

collide = lambda x1, x2, y1, y2, w1, w2, h1, h2: x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2 

class slider:
    def __init__(self, whereupon, x, y, width, height, maxoffset, sliderimg1 = None, sliderimg2 = None, offsetx = 0, offsety = 0, mp = 0, whereuponvars = [0, 0, display.Info().current_w, display.Info().current_h], state = 0, drawoffset = False, startoffset = 0):
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
        
        if not self.updated:
            return True

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
