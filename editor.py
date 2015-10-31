#!/usr/bin/env python
"""
editor.py : Tools for editing the current Level.
"""
__author__ = "Andrew Peterson (DJKool14)"
__copyright__ = "Copyright 2015, sam0sRpgGame"
__credits__ = []


import sys
import pygame as pg
from pygame.locals import *

from gamelib.game import GameState
from gamelib.asset import TileSet
from gamelib.primitives import Rect, Point

from level import Level


class EditorState(GameState):

    GRID_COLOR = pg.Color(128, 128, 128, 128)
    SELECT_COLOR = pg.Color(0, 255, 0, 128)

    TS_COLOR = pg.Color(255, 0, 255)
    TS_SEL_COLOR = pg.Color(0, 0, 255)
    TS_SRATIO = 0.4

    def __init__(self):
        GameState.__init__(self)

        # For reference, actually set during initialize()
        self.level = None
        self.tileset = None
        self.tsRect = None

        # User Interaction
        self.selected = None
        self.currTile = 0

    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""

    def enter(self, level):
        """Called every time the game is switched to this state."""
        self.level = level
        if not self.tileset or level.tileset.filename != self.tileset.filename:
            # Make a copy of the tileset so we can upscale it and use it
            # as part of the Editor GUI.
            ts = TileSet(level.tileset.filename, level.tileset.srcTileSize)
            scale = (self.gc.SCREEN_SIZE[0]*EditorState.TS_SRATIO)/ts.image.get_width()
            ts.resize((int(ts.tileSize[0]*scale), int(ts.tileSize[1]*scale)))
            print ts.getScale()
            self.tileset = ts

            # Position tileset UI at top left of screen
            self.tsRect = Rect.fromSides(self.gc.SCREEN_SIZE[0]-ts.image.get_width(), 0,
                                         self.gc.SCREEN_SIZE[0], ts.image.get_height())
            self.currTile = 0

        # Select upper left tile by default
        self.selected = self.level.getTileAt(self.level.areaPos)

    def processInput(self):
        pg.display.set_caption(str(self.level.areaPos[0]/660) + "," + str(self.level.areaPos[1]/450) + "   |    lvl name: " + self.level.name)
        """Called during normal update/render period for this state
           to process it's input."""
        for e in pg.event.get():
            if e.type == QUIT:
                self.gc.quit()
            elif e.type == KEYDOWN:
                self._handleKeydown(e.key)
            elif e.type == KEYUP:
                if e.key == K_TAB:
                    from game import TestState
                    self.gc.changeState(TestState, self.level.lvlFile)
            elif e.type == MOUSEBUTTONDOWN:
                self._handleClick(e.button, e.pos)

        # WASD Controls allows for faster movement.
        # They are handled the same as arrow keys,
        # but will be processed on every from instead of just once
        # per keydown event.
        sel_x, sel_y = self.selected
        k = pg.key.get_pressed()
        if k[K_w]:
            self._handleKeydown(K_UP)
        elif k[K_s]:
            self._handleKeydown(K_DOWN)
        if k[K_a]:
            self._handleKeydown(K_LEFT)
        elif k[K_d]:
            self._handleKeydown(K_RIGHT)


    def update(self):
        """Called during normal update/render period for this state
           to update it's local or game data."""
        # Not much to update in Editor State as almost everything
        # is driven by user input.

    def render(self):
        """Called during normal update/render period for this state
           to render it's data in a specific way."""
        surf = self.gc.screen
        view_offset = self.level.getTilePos(self.level.getTileAt(self.level.areaPos))

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

        # Draw tileset UI
        tsrect = pg.Rect(*self.tsRect.intArgs())
        tsrect.inflate_ip(4, 4)
        pg.draw.rect(surf, EditorState.TS_COLOR, tsrect)
        surf.blit(self.tileset.image, self.tsRect.pos.intArgs())

        x, y = self.tsRect.pos.intArgs()
        while x <= self.tsRect.right:
            pg.draw.line(surf, EditorState.GRID_COLOR, (x, self.tsRect.top), (x, self.tsRect.bottom))
            x += self.tileset.tileSize[0]
        while y <= self.tsRect.bottom:
            pg.draw.line(surf, EditorState.GRID_COLOR, (self.tsRect.left, y), (self.tsRect.right, y))
            y += self.tileset.tileSize[1]
        tselrect = self.tileset.getTileRect(self.currTile)
        tselrect.move_ip(*self.tsRect.pos.intArgs())
        pg.draw.rect(surf, EditorState.TS_SEL_COLOR, tselrect, 1)

        pg.display.flip()

    def leave(self):
        """Called whenever we switch from this state to another."""
        self.level.save()

    def shutdown(self):
        """Called during application shutdown."""

    def _handleClick(self, button, mpos):
        mpos = Point(*mpos)

        # Check for UI interaction first
        if self.tsRect.contains(mpos):
            # Determine tile index
            # We could technically iterate through
            # every tile in the tileset and use getTileRect,
            # but it is so much simple to use based math, assuming 2d grid.
            rpos = mpos - self.tsRect.pos
            self.currTile = (int(rpos.y/self.tileset.tileSize[1]) * self.tileset.tileCounts[0]) + int(rpos.x/self.tileset.tileSize[0])
            assert( self.tileset.getTileRect(self.currTile).collidepoint(rpos.intArgs()))
        else:
            # Always handle world clicking last
            wpos = mpos + Point(*self.level.areaPos)
            self.selected = self.level.getTileAt(wpos.args())

    def _handleKeydown(self, key):

        if key == K_SPACE:
            self.level.setTile(self.selected, self.currTile)
            print str(self.level.getTilePos(self.selected))

        # Handle selection movement
        if key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
            sel_x, sel_y = self.selected
            if key == K_UP:
                sel_y -= 1
            elif key == K_DOWN:
                sel_y += 1
            elif key == K_LEFT:
                sel_x -= 1
            elif key == K_RIGHT:
                sel_x += 1

            pos = self.level.getTilePos((sel_x, sel_y))
            if pos:
                self.selected = (sel_x, sel_y)
                self.level.move(pos)

#end EditorState


# Main Entry Point
if __name__ == "__main__":
    # After the Level become more self contained, we can use this area to launch
    # the game directly into editor mode and bypass the Menu and Game States.
    # Right now, too many resources that the Editor relies on is being loaded
    # manually in TestState.

    # Load level specified in arguments passed to editor
    if len(sys.argv) < 2:
        print "You must specify a Level to edit!"
        print "Usage: editor.py <level>"
        sys.exit(-1)

    world = Level((660, 450), sys.argv[1])

    from game import startGame
    startGame(EditorState, world)

# end main
