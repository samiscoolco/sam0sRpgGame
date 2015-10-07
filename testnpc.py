#!/usr/bin/env python
"""
testnpc.py : Basic Npc

testnpc - the npc itself
"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []


import pygame
from pygame.locals import *
from gamelib.asset import *
from level import *

SCREEN_SIZE = (660, 450)
class testnpc(Entity):
    def __init__(self,x,y, anim_set):
        Entity.__init__(self, x, y)
        self.cond=0
        self.animator = Animator(anim_set, Animator.MODE_LOOP, 15)
        self.animator.setAnim("idle")
    def update(self, dt):   
            self.animator.update(dt)

    def render(self, surf):
        screen_pos = (self.x % SCREEN_SIZE[0], self.y % SCREEN_SIZE[1])
        self.animator.render(surf, screen_pos)
