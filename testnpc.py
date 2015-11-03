#!/usr/bin/env python
"""
testnpc.py : Basic Npc

testnpc - the npc itself
companion - follows player
"""
__author__ = "Sam Tubb (sam0s)"
__copyright__ = "None"
__credits__ = []


import pygame
from math import hypot,sqrt
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



def MovePoint(target0,target1,selfx,selfy,movespeed):

    distance = [target0 - selfx, target1 - selfy]
    norm = sqrt(distance[0] ** 2 + distance[1] ** 2)
    direction = [distance[0] / norm, distance[1 ] / norm]
    
    pos_change = [direction[0] * movespeed, direction[1] * movespeed]
    return pos_change

class testcompanion(Entity):

    def __init__(self, pos, anim_set):
        Entity.__init__(self, pos)
        self.cond=0
        self.animator = Animator(anim_set, Animator.MODE_STOPPED, 15)
        self.animator.setAnim("idle")
    def update(self, dt,target):   
            self.animator.update(dt)
            dist=int(hypot(target.pos[0] - self.pos[0], target.pos[1] - self.pos[1]))
            if dist > 75:
                moveto=MovePoint(target.pos[0],target.pos[1],self.pos[0],self.pos[1],3)
                self.pos[0]+=moveto[0]
                self.pos[1]+=moveto[1]
            if dist < 73:
                moveto=MovePoint(target.pos[0],target.pos[1],self.pos[0],self.pos[1],3)
                self.pos[0]-=moveto[0]
                self.pos[1]-=moveto[1]
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

