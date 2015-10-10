#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

pygame.init()

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

def colorize(image, newColor):
    image = image.copy()

    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    return image  

class window:
    info = display.Info()
    
    width = 640
    height = 480

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

from palette import palette
from panels import panels
from workspace import workspace, camera

palette = palette(window)
panels = panels(window)
workspace = workspace(window)

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
            palette.resize()
            panels.resize()
            camera.resize(window)
            workspace.resize()

    camera.update()

def mainloop():    
    while True:
        window.screen.fill((255, 255, 255))       
        
        workspace.draw()
        workspace.update()
        
        offset = palette.update()
        if type(offset) is int:
            workspace.change_offset(offset)
        palette.draw(window.screen) 
        
        panels.draw()
        
        info.draw()

        cursor.update()
        cursor.draw()

        events()
        
        display.update()

if __name__ == "__main__":
    mainloop()
