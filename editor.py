#!/usr/bin/env python
"""
editor.py : Tools for editing the current Level.
"""
__author__ = "Andrew Peterson (DJKool14)"
__copyright__ = "Copyright 2015, sam0sRpgGame"
__credits__ = []


import pygame as pg
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_TAB, K_LSHIFT, K_w, K_a, K_s, K_d

from gamelib.game import GameState


class EditorState(GameState):

    GRID_COLOR = pg.Color(128, 128, 128, 128)
    SELECT_COLOR = pg.Color(0, 255, 0, 128)

    def __init__(self):
        GameState.__init__(self)

        # For reference, actually set during initialize()
        self.level = None
        self.tileset = None
        self.selected = None

    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""

    def enter(self, level):
        """Called every time the game is switched to this state."""
        self.level = level
        self.tileset = level.tileset

        # Select upper left tile by default
        self.selected = self.level.getTileAt(self.level.areaPos)

    def processInput(self):
        """Called during normal update/render period for this state
           to process it's input."""
        for e in pg.event.get():
            if e.type == QUIT:
                self.gc.quit()
            elif e.type == KEYUP:
                if e.key == K_TAB:
                    from game import TestState
                    self.gc.changeState(TestState)

        sel_x, sel_y = self.selected
        k = pg.key.get_pressed()
        if k[K_w]:
            sel_y -= 1
        elif k[K_s]:
            sel_y += 1
        if k[K_a]:
            sel_x -= 1
        elif k[K_d]:
            sel_x += 1

        pos = self.level.getTilePos((sel_x, sel_y))
        if pos:
            self.selected = (sel_x, sel_y)
            self.level.move(pos)


    def update(self):
        """Called during normal update/render period for this state
           to update it's local or game data."""

    def render(self):
        """Called during normal update/render period for this state
           to render it's data in a specific way."""
        surf = self.gc.screen
        view_offset = self.level.areaPos

        surf.fill((0,0,0))
        self.level.render(surf)

        # Draw a grid to highlight each tile.
        x, y = 0, 0
        while x <= self.level.areaSize[0]:
            pg.draw.line(surf, EditorState.GRID_COLOR, (x, 0), (x, self.level.areaSize[1]))
            x += self.level.TILE_WIDTH
        while y <= self.level.areaSize[1]:
            pg.draw.line(surf, EditorState.GRID_COLOR, (0, y), (self.level.areaSize[0], y))
            y += self.level.TILE_HEIGHT

        # Draw selected tile
        selrect = self.level.getTileRect(self.selected)
        selrect.move_ip(-view_offset[0], -view_offset[1])
        pg.draw.rect(surf, EditorState.SELECT_COLOR, selrect, 1)

        pg.display.flip()

    def leave(self):
        """Called whenever we switch from this state to another."""

    def shutdown(self):
        """Called during application shutdown."""

#end EditorState


# Main Entry Point
if __name__ == "__main__":
    # After the Level become more self contained, we can use this area to launch
    # the game directly into editor mode and bypass the Menu and Game States.
    # Right now, too many resources that the Editor relies on is being loaded
    # manually in TestState.
    pass

# end main
