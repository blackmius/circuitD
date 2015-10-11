#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *
from pygame import *
import pygame

from fillGradient import fill_gradient

class panels:
    def __init__(self, window):
        self.window = window
        
        self.panelWidth = self.window.width
        self.panelHeight = 36
        
        self.panelBg = Surface((self.panelWidth, self.panelHeight))
        
        self.panel1 = Surface((self.panelWidth, self.panelHeight))
        self.panel2 = Surface((self.panelWidth, self.panelHeight))
        
        fill_gradient(self.panelBg, (60, 60, 60), (15, 15, 13))
        
        self.panel1.blit(self.panelBg, (0, 0))
        self.panel2.blit(self.panelBg, (0, 0))
    
    def resize(self):
        self.panelWidth = self.window.width
        
        self.panelBg = Surface((self.panelWidth, self.panelHeight))
        
        self.panel1 = Surface((self.panelWidth, self.panelHeight))
        self.panel2 = Surface((self.panelWidth, self.panelHeight))
        
        fill_gradient(self.panelBg, (60, 60, 60), (15, 15, 13))
        
        self.panel1.blit(self.panelBg, (0, 0))
        self.panel2.blit(self.panelBg, (0, 0))
        
    def draw(self):
        self.window.screen.blit(self.panel1, (0, 0))
        
        self.window.screen.blit(self.panel2, (0, self.window.height - self.panelHeight))
        
