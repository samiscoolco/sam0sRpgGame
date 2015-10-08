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

class testnpc(Entity):
    def __init__(self, pos, anim_set):
        Entity.__init__(self, pos)
        self.cond=0
        self.animator = Animator(anim_set, Animator.MODE_LOOP, 15)
        self.animator.setAnim("idle")

    def update(self, dt):   
            self.animator.update(dt)

    def render(self, surf, offset = None):
        screen_pos = self.pos + offset if offset else self.pos
        self.animator.render(surf, screen_pos.intArgs())
