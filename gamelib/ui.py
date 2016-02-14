#!/usr/bin/env python
"""
ui.py : Basic UI framework.

"""
__author__ = "Andrew Peterson (DJKool14)"
__copyright__ = "Copyright 2015"
__credits__ = []


import pygame as pg
from pygame.locals import *

from primitives import Rectangle as Rect


# Custom Event IDs used when pushing custom USEREVENTS through
# the pygame events queue instead of direct callback notifications.
class Events:
    BASE = 1234,
    BUTTON_CLICKED = 1235
#end Event


class ColorTheme(object):

    # Frame Colors
    BG_COLOR = pg.Color(255, 0, 0)
    FG_COLOR = pg.Color(255, 255, 0)

    # Button Colors (UP, HOVER, DOWN)
    BUT_COLORS = ( FG_COLOR, pg.Color(192, 192, 0), pg.Color(128, 128, 0) )
    BEV_SIZES  = ( 1, 2, 4)
    BEV_COLOR = pg.Color(0, 255, 255)

    FONT = None # Delay font creation until first text
    FONT_COLOR = pg.Color(255, 255, 255)

    def drawFrame(self, surf, rect):
        pg.draw.rect(surf, self.BG_COLOR, rect, 0)

    def drawButton(self, surf, rect, state):
        pg.draw.rect(surf, self.BUT_COLORS[state], rect, 0)
        pg.draw.rect(surf, self.BEV_COLOR, rect, self.BEV_SIZES[state])

    def drawText(self, surf, rect, text, centered=False):
        if not self.FONT:
            self.FONT = pg.font.Font(pg.font.get_default_font(), 12)

        text_surf = self.FONT.render(text, False, self.FONT_COLOR)
        pos = rect.topleft
        if centered:
            pos = rect.center
            pos = (pos[0]-text_surf.get_width()/2, pos[1]-text_surf.get_height()/2)
        surf.blit(text_surf, pos)

#end ColorTheme
_THEME = ColorTheme()



class Frame(object):

    def __init__(self, bounds):
        self.parent = None
        self.visible = True
        self.bounds = bounds
        self.children = []

    def render(self, surf):
        if not self.visible:
            return

        _THEME.drawFrame(surf, self.getRect())
        if self.children:
            for c in self.children:
                if c.visible:
                    c.render(surf)

    def processEvent(self, event):
        # Only mouse events 
        if hasattr(event, 'pos') and not self.getRect().collidepoint(event.pos):
            return False
        return self._delegate('processEvent', event)

    def getRect(self):
        return self.bounds.move(*self.parent.bounds.topleft) if self.parent else self.bounds

    def addChild(self, child):
        assert(isinstance(child, Frame))
        self.children.append(child)
        child.parent = self

    def _delegate(self, call, *args, **kargs):
        if not self.children:
            return False
        for c in self.children:
            if getattr(c, call)(*args, **kargs):
                return True
        return False

#end Frame



class Text(Frame):

    def __init__(self, bounds, text="", centered = False):
        Frame.__init__(self, bounds)
        self.text = text
        self.centered = centered

    def render(self, surf):
        _THEME.drawText(surf, self.getRect(), self.text, self.centered)

    def processEvent(self, event):
        return False

#end Text



class Button(Frame):

    UP = 0
    HOVER = 1
    DOWN = 2

    def __init__(self, bounds, label, callback = None):
        Frame.__init__(self, bounds)
        self.label = label
        self.callback = callback
        self.state = Button.UP

    def render(self, surf):
        _THEME.drawButton(surf, self.getRect(), self.state)
        _THEME.drawText(surf, self.getRect(), self.label, True)

    def processEvent(self, event):
        # Moving into or out of button
        if event.type == MOUSEMOTION:
            if self.getRect().collidepoint(event.pos):
                if not self.state == Button.DOWN:
                    self._changeState(Button.HOVER)
            elif not self.state == Button.UP:
                self._changeState(Button.UP)
        elif self.state == Button.HOVER:
            # If state is already HOVER, always assume mouse is in Rect
            if event.type == MOUSEBUTTONDOWN:
                self._changeState(Button.DOWN)
        elif self.state == Button.DOWN:
            if event.type == MOUSEBUTTONUP:
                self._changeState(Button.HOVER)

    def _changeState(self, new_state):
        if self.state == new_state:
            return

        if self.state == Button.HOVER:
            if new_state == Button.DOWN:
                self._notify()

        self.state = new_state

    def _notify(self):
        if self.callback:
            self.callback(self)
        else:
            pg.event.post(pg.event.Event(USEREVENT, usercode=Events.BUTTON_CLICKED, button=self))

#end Button
