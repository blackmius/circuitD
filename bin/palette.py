#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

from button import button
from slider import slider

from circuitImage import circuitImage
from fillGradient import fill_gradient

percent = lambda max, percent: int(float(max)/100*percent)

strdiv = lambda line, n: [line[i:i+n] for i in range(0, len(line), n)]

class tab:
    def __init__(self, name, elements, palette):
        self.name = name

        self.palette = palette

        self.open = False
        
        self.w = 190
        self.h = 26

        self.x = 0 - self.palette.offset
        self.y = 0

        self.image = Surface((self.w, self.h))

        fill_gradient(self.image, (60, 60, 60), (15, 15, 13))

        self.fontsize = 18

        self.font = font.Font('../data/fonts/gost.ttf', self.fontsize)

        self.image.blit(self.font.render(self.name, 0, (255, 255, 255)), (4, self.h/2-self.font.size(self.name)[1]/2))

        self.surfaceH = self.h
        
        self.surface = Surface((self.w, self.surfaceH))
        
        self.elements =  []

        self.num = len(self.palette.tabs)

        self.circuitSize = 50        
        self.circuitIntend = 25

        for i in elements:
            self.addElement(i)

        self.buttonImgs = [image.load('../data/imgs/arrowbutton2.png'), transform.flip(image.load('../data/imgs/arrowbutton2.png'), False, True)]
        self.button = button(160, self.h/2 - 7, self.image, self.buttonImgs, imgnum = 1 if self.open else 0, whereuponvars = [self.x, self.y + 36, self.w, self.h], backlight = (255, 255, 255, 30))
        
        self.elementImg = Surface((50, 50))
        self.elementImg.fill((255, 255, 255), (2, 2, 46, 46))

        self.font = font.Font('../data/fonts/gost.ttf', self.fontsize)

    def resize(self):
        d = 0
        
        for i in self.elements:
            d += len(i[0].split('\n'))*(self.fontsize+4)

        if self.open and self.elements != []:
            self.surfaceH = (len(self.elements)/2 + len(self.elements)%2)*self.circuitSize + (len(self.elements)/2 + (len(self.elements)%2) + 1)*self.circuitIntend + self.h + d

            self.surface = Surface((self.w, self.surfaceH))

            self.surface.fill((208, 214, 219, 255))

            y = 0
            d = 0

            if len(self.elements) > 1:
                for y in range(len(self.elements)/2):
                    b = 0
                    k = 0

                    self.surface.blit(self.elements[y][1], (20, y*self.circuitSize + (y+1)*self.circuitIntend + self.h + d))
                    
                    for i in range(len(self.elements[y][0].split('\n'))):
                        self.surface.blit(self.font.render(self.elements[y][0].split('\n')[i], 0, (0, 0, 0)), ((45 - self.font.size(self.elements[y][0].split('\n')[i])[0]/2, (y+1)*self.circuitSize + (y+1)*self.circuitIntend + self.h + d + i*self.fontsize + i*4)))
                        
                        b += self.fontsize+4

                    self.surface.blit(self.elements[y+1][1], (120, y*self.circuitSize + (y+1)*self.circuitIntend + self.h + d))
                    
                    for i in range(len(self.elements[y+1][0].split('\n'))):
                        self.surface.blit(self.font.render(self.elements[y+1][0].split('\n')[i], 0, (0, 0, 0)), ((145 - self.font.size(self.elements[y+1][0].split('\n')[i])[0]/2, (y+1)*self.circuitSize + (y+1)*self.circuitIntend + self.h + d + i*self.fontsize + i*4)))
                        
                        b += self.fontsize+4

                    d += b if b > k else k

                if len(self.elements)%2 == 1:
                    self.surface.blit(self.elements[-1:][0][1], (20, (y+1)*self.circuitSize + (y+1)*self.circuitIntend + self.h + d))
                    
                    for i in range(len(self.elements[-1:][0][0].split('\n'))):
                        self.surface.blit(self.font.render(self.elements[-1:][0][0].split('\n')[i], 0, (0, 0, 0)), ((45 - self.font.size(self.elements[-1:][0][0].split('\n')[i])[0]/2, (y+2)*self.circuitSize + (y+1)*self.circuitIntend + self.h + d + i*self.fontsize + i*4)))
            
            if len(self.elements) == 1:
                self.surface.blit(self.elements[-1:][0][1], (20, self.circuitIntend + self.h + d))
                
                for i in range(len(self.elements[-1:][0][0].split('\n'))):
                    self.surface.blit(self.font.render(self.elements[-1:][0][0].split('\n')[i], 0, (0, 0, 0)), ((45 - self.font.size(self.elements[-1:][0][0].split('\n')[i])[0]/2, self.circuitSize + self.circuitIntend + self.h + d + i*self.fontsize + i*4)))
        
        else:
            self.surfaceH = self.h
            self.surface = Surface((self.w, self.surfaceH))
   
    def addElement(self, name, image = None):     
        name = name.split()

        for i in range(len(name)):
            if len(name[i]) > 10:
                name[i] = strdiv(name[i], 10)

            else:
                name[i] = [name[i]]

        name = '\n'.join(str(item) for innerlist in name for item in innerlist)

        if image == None:
            image = self.elementImg
        
        else:
            if image.get_size() != (50, 50):
                transform.scale(image, (50, 50))
        
        self.elements.append([name, image])

        self.resize()

    def update(self):
        self.x = 0 - self.palette.offset

        if self.palette.tabupdated:
            self.y = 0
            
            for i in range(self.num):
                if self.palette.tabs[i].open:
                    self.y += self.palette.tabs[i].surfaceH

                else:
                    self.y += self.h

            self.button.change_whereuponvars(y = self.y + 36 - int(self.palette.slider.absoffset))
    
        if self.button.update():
            self.open = not self.open

            self.resize()

            return True

    def draw(self):
        self.button.draw()
        self.surface.blit(self.image, (0, 0))

        self.palette.surface.blit(self.surface, (self.x, self.y - int(self.palette.slider.absoffset)))
        
class palette:
    def __init__(self, window):
        self.window = window
        
        self.width = 200
        self.height = self.window.height - 72
    
        self.offset = 0
        self.offsetTo = self.offset

        self.moveSpeed = 10

        self.surface = Surface((self.width, self.height)).convert_alpha()

        self.arrowsWidth = 10
        self.arrowsHeight = 124
    
        self.arrowsBg = Surface((self.arrowsWidth+2, self.height))

        self.arrowsImg2 = transform.scale(image.load('../data/imgs/arrowbutton.png'), (self.arrowsWidth, self.arrowsHeight))
        self.arrowsImg1 = transform.flip(self.arrowsImg2, True, False)

        self.arrows = button(self.width+1, self.height/2 - self.arrowsHeight/2, window.screen, [self.arrowsImg1, self.arrowsImg2], imgnum = 0 if self.offset == 0 - self.width else 1, backlight = (255, 255, 255, 30))

        self.sliderWidth = 15
        self.sliderHeight = self.height
        self.sliderX = self.offset + self.width - self.sliderWidth
        self.sliderY = 36
        self.sliderMaxoffset = 0

        self.slider = slider(window.screen, self.sliderX, self.sliderY, self.sliderWidth, self.sliderHeight, self.sliderMaxoffset)

        self.lastslideroffset = 0

        self.offsetY = 0

        self.mousepressed = False

        self.pannelWidth = 640
        self.pannelHeight = 36
        
        self.offsetreturn = self.offset
        self.pastoffsetreturn = self.offset

        self.tabs = []
        
        for i in ['Inputs', 'Outputs', 'Prim elements', 'Elements']:
            self.tabs.append(tab(i, [], self))

        self.tabs[0].addElement('a')
        self.tabs[0].addElement('test test2')
        self.tabs[0].addElement('test test3')
        self.tabs[0].addElement('test test4')
        self.tabs[0].addElement('test test5')


        self.tabupdated = True
        
    def resize(self):
        self.width = 200

        self.height = self.window.height - 72

        self.surface = Surface((self.width, self.height)).convert_alpha()

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

    def updateTabs(self):
        for i in self.tabs:
            if i.update():
                self.tabupdated = True

                self.updateTabs()

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

            if self.lastslideroffset != self.slider.absoffset:
                self.tabupdated = True

                self.lastslideroffset = self.slider.absoffset

            self.updateTabs()

            off = 0

            for i in self.tabs:
                off += i.surfaceH

            if off - self.height > 0:
                self.slider.change_offset(maxoffset = off - self.height)
            
            else:
                self.slider.change_offset(maxoffset = 0)

            self.tabupdated = False
        
        if self.pastoffsetreturn != self.offsetreturn:
            self.pastoffsetreturn = self.offsetreturn
            
            return self.offsetreturn

    
    def draw(self, whereupon):
        self.surface.fill((208, 214, 219, 255))

        for i in self.tabs:
            i.draw()

        self.window.screen.blit(self.surface, (self.offset, self.pannelHeight))
        self.window.screen.blit(self.arrowsBg, (self.offset + self.width, self.pannelHeight))

        self.arrows.draw()
        self.slider.draw()
