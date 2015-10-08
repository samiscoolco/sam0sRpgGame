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
from gamelib.primitives import Circle
from level import *

class testnpc(Entity):

    VIEW_DIST = 100

    def __init__(self, pos, anim_set):
        Entity.__init__(self, pos)
        self.cond=0
        self.animator = Animator(anim_set, Animator.MODE_STOPPED, 15)
        self.animator.setAnim("idle")
        self.vision = Circle(pos, testnpc.VIEW_DIST)

    def update(self, dt):   
            self.animator.update(dt)

    def render(self, surf, offset = None):
        screen_pos = self.pos + offset if offset else self.pos
        self.animator.render(surf, screen_pos.intArgs())

    def lookAt(self, pos):
        # Idle frame index based on direction to target:
        # <--X-->
        #|  \3/
        #Y 2 X 1
        #|  /0\
        #V
        d = pos - self.pos
        frame = 0
        if d.x >= d.y:
            frame = 1 if d.x >= -d.y else 3
        else:
            frame = 0 if d.x >= -d.y else 2
        self.animator.setFrame(frame)

