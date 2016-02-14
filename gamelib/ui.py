#!/usr/bin/env python
"""
ui.py : Basic UI framework

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

    # Various Flags
    F_NONE = 0
    F_CENTER_HORZ = 1
    F_CENTER_VERT = 2
    F_CENTER_FULL = 3

    def drawFrame(self, surf, rect):
        pg.draw.rect(surf, self.BG_COLOR, rect, 0)

    def drawButton(self, surf, rect, state):
        pg.draw.rect(surf, self.BUT_COLORS[state], rect, 0)
        pg.draw.rect(surf, self.BEV_COLOR, rect, self.BEV_SIZES[state])

    def drawText(self, surf, rect, text, flags=0):
        if not self.FONT:
            self.FONT = pg.font.Font(pg.font.get_default_font(), 12)

        text_surf = self.FONT.render(text, False, self.FONT_COLOR)
        pos = rect.topleft
        if flags:
            pos = (pos[0] + ((rect.width-text_surf.get_width())/2 if flags & self.F_CENTER_HORZ else 0),
                   pos[1] + ((rect.height-text_surf.get_height())/2 if flags & self.F_CENTER_VERT else 0))
        surf.blit(text_surf, pos)
        return text_surf.get_width()

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
        self.flags = ColorTheme.F_CENTER_FULL if centered else 0

    def render(self, surf):
        _THEME.drawText(surf, self.getRect(), self.text, self.flags)

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
        _THEME.drawText(surf, self.getRect(), self.label, ColorTheme.F_CENTER_FULL)

    def processEvent(self, event):
        # Moving into or out of button
        if event.type == MOUSEMOTION:
            if self.getRect().collidepoint(event.pos):
                if not self.state == Button.DOWN:
                    self._changeState(Button.HOVER)
                    return True
            elif not self.state == Button.UP:
                self._changeState(Button.UP)
        elif self.state == Button.HOVER:
            # If state is already HOVER, always assume mouse is in Rect
            if event.type == MOUSEBUTTONDOWN:
                self._changeState(Button.DOWN)
                return True
        elif self.state == Button.DOWN:
            if event.type == MOUSEBUTTONUP:
                self._changeState(Button.HOVER)
                return True
        return False

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



class EditBox(Frame):

    def __init__(self, bounds, text=""):
        Frame.__init__(self, bounds)
        self.text = text
        self.focused = False
        self.selPos = 0

    def render(self, surf):
        text = self.text
        if self.focused:
            text = self.text[:self.selPos]+"|"+self.text[self.selPos:]
        _THEME.drawButton(surf, self.getRect(), Button.DOWN)
        _THEME.drawText(surf, self.getRect(), text, ColorTheme.F_CENTER_VERT)

    def processEvent(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.getRect().collidepoint(event.pos):
                self.focused = True
                self.selPos = len(self.text)
            else:
                self.focused = False

        elif event.type == KEYDOWN:
            if not self.focused:
                return False

            if event.key == K_LEFT:
                self.selPos -= 1 if self.selPos > 0 else 0
            elif event.key == K_RIGHT:
                self.selPos += 1 if self.selPos < len(self.text) else 0
            elif event.key == K_BACKSPACE and self.selPos > 0:
                self.selPos -= 1
                self.text = self.text[:self.selPos]+self.text[self.selPos+1:]
            elif event.unicode:
                self.text = self.text[:self.selPos]+event.unicode+self.text[self.selPos:]
                self.selPos += 1
            return True

    def setFocus(self, focus):
        self.focused = focus

#end EditBox
