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
from gamelib.primitives import Point, Rectangle as Rect

from level import Level, AdvancedTileSet


class EditorState(GameState):

    GRID_COLOR = pg.Color(128, 128, 128, 128)
    SELECT_COLOR = pg.Color(0, 255, 0, 128)

    TS_COLOR = pg.Color(255, 0, 255)
    TS_SEL_COLOR = pg.Color(0, 0, 255)
    TS_SRATIO = 0.4

    TS_ICON_SIZE = (64, 64)

    DIR_N = 0
    DIR_W = 1
    DIR_E = 2
    DIR_S = 3
    DIR_NW = 4
    DIR_NE = 5
    DIR_SE = 6
    DIR_SW = 7
    DIR_OFFSETS = (
        (0, -1),
        (-1, 0),
        ( 1, 0),
        ( 0, +1),
        (-1, -1),
        ( 1, -1),
        ( 1, 1),
        (-1, 1)
    )

    def __init__(self):
        GameState.__init__(self)

        # For reference, actually set during initialize()
        self.level = None
        self.tileset = None
        self.tsRect = None
        self.terrains = None
        self.terrRect = None

        # User Interaction
        self.selected = None
        self.currTile = None
        self.currTerr = None


    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""

    def enter(self, level):
        """Called every time the game is switched to this state."""
        self.level = level
        if not self.tileset or level.tileset.filename != self.tileset.filename:
            # Make a copy of the tileset so we can upscale it and use it
            # as part of the Editor GUI.
            ts = AdvancedTileSet(level.tileset.filename)
            scale = (self.gc.SCREEN_SIZE[0]*self.TS_SRATIO)/ts.image.get_width()
            ts.resize((int(ts.tileSize[0]*scale), int(ts.tileSize[1]*scale)))
            print ts.getScale()
            self.tileset = ts

            # Position tileset UI at top right of screen
            self.tsRect = Rect.fromSides(self.gc.SCREEN_SIZE[0]-ts.image.get_width(), 0,
                                         self.gc.SCREEN_SIZE[0], ts.image.get_height())
            self.currTile = 0

            # Generate Terrain Icons
            self.terrains = [(t, self.tileset.genTerrainIcon(t, self.TS_ICON_SIZE)) for t in self.tileset.terrain]
            print "Generated %i terrain tiles." % (len(self.terrains))

            # Position terrain UI at right of screen just under tileset UI
            self.terrRect = Rect.fromSides(self.gc.SCREEN_SIZE[0] - self.TS_ICON_SIZE[0],
                                           ts.image.get_height(),
                                           self.gc.SCREEN_SIZE[0],
                                           ts.image.get_height() + len(self.terrains) * self.TS_ICON_SIZE[1])

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
                    from gamestates import TestState
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
            pg.draw.line(surf, self.GRID_COLOR, (x, 0), (x, self.level.areaSize[1]))
            x += self.level.TILE_WIDTH
        while y <= self.level.areaSize[1]:
            pg.draw.line(surf, self.GRID_COLOR, (0, y), (self.level.areaSize[0], y))
            y += self.level.TILE_HEIGHT

        # Draw selected tile
        selrect = self.level.getTileRect(self.selected)
        selrect.move_ip(-view_offset[0], -view_offset[1])
        pg.draw.rect(surf, self.SELECT_COLOR, selrect, 1)

        # Draw tileset UI
        tsrect = pg.Rect(*self.tsRect.intArgs())
        tsrect.inflate_ip(4, 4)
        pg.draw.rect(surf, self.TS_COLOR, tsrect)
        surf.blit(self.tileset.image, self.tsRect.pos.intArgs())

        # Tileset Grid
        x, y = self.tsRect.pos.intArgs()
        while x <= self.tsRect.right:
            pg.draw.line(surf, self.GRID_COLOR, (x, self.tsRect.top), (x, self.tsRect.bottom))
            x += self.tileset.tileSize[0]
        while y <= self.tsRect.bottom:
            pg.draw.line(surf, self.GRID_COLOR, (self.tsRect.left, y), (self.tsRect.right, y))
            y += self.tileset.tileSize[1]
        if self.currTile != None:
            tselrect = self.tileset.getTileRect(self.currTile)
            tselrect.move_ip(*self.tsRect.pos.intArgs())
            pg.draw.rect(surf, self.TS_SEL_COLOR, tselrect, 1)

        # Draw Terrain Tiles
        if self.terrains:
            terr_rect = pg.Rect(self.terrRect.pos.intArgs(), self.TS_ICON_SIZE)
            for t in self.terrains:
                surf.blit(t[1], terr_rect.topleft)

                # Draw selected Terrain Tile
                if self.currTerr != None and self.terrains[self.currTerr] is t:
                    pg.draw.rect(surf, self.TS_SEL_COLOR, terr_rect, 2)

                terr_rect.move_ip(0, self.TS_ICON_SIZE[1])

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
            self.currTerr = None
        elif self.terrRect.contains(mpos):
            rpos = mpos - self.terrRect.pos
            self.currTerr = rpos.y // self.TS_ICON_SIZE[1]
            self.currTile = None
            print "Selected terrain type %i (%s)" % (self.currTerr, self.terrains[self.currTerr][0])
        else:
            # Always handle world clicking last
            wpos = mpos + Point(*self.level.areaPos)
            self.selected = self.level.getTileAt(wpos.args())

    def _handleKeydown(self, key):

        if key == K_SPACE:
            # Use active terrain to determine next tileset selection
            terrain = self.terrains[self.currTerr][0] if self.currTerr != None else None
            if self.currTerr != None:
                offset = self._calcBorderOffset(self.selected, terrain)
                self.currTile = self.tileset.getTerrainTile(terrain, offset)
                #print "Border offset: %i" % (offset)

            self.level.setTile(self.selected, self.currTile)
            print "Set Tile%s to %i" % (str(self.selected), self.currTile)
            #print str(self.level.getTilePos(self.selected))

            if self.currTerr != None:
                # Propogate terrain changes to neighbors
                for d in self.DIR_OFFSETS:
                    tile = (self.selected[0]+d[0], self.selected[1]+d[1])
                    if self.tileset.matchTerrain(terrain, self.level.getTile(tile)):
                        offset = self._calcBorderOffset(tile, terrain)
                        self.level.setTile(tile, self.tileset.getTerrainTile(terrain, offset))
                        #print "Neighbor%s Set to %i" % (str(tile), offset)

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


    def _calcBorderOffset(self, tile, terr, check_diags = True):
        # Cardinal Directions
        # N = 1, W = 2, E = 4, S = 8
        offset = 1 if self.tileset.matchTerrain(terr, self.level.getTile((tile[0], tile[1]-1))) else 0
        offset += 2 if self.tileset.matchTerrain(terr, self.level.getTile((tile[0]-1, tile[1]))) else 0
        offset += 4 if self.tileset.matchTerrain(terr, self.level.getTile((tile[0]+1, tile[1]))) else 0
        offset += 8 if self.tileset.matchTerrain(terr, self.level.getTile((tile[0], tile[1]+1))) else 0

        # Diagnals, only care about diagnals when we have a full 15 (all sides the same)
        if check_diags and offset == 15:
            diag = 1 if self.tileset.matchTerrain(terr, self.level.getTile((tile[0]-1, tile[1]-1))) else 0
            diag += 2 if self.tileset.matchTerrain(terr, self.level.getTile((tile[0]+1, tile[1]-1))) else 0
            diag += 4 if self.tileset.matchTerrain(terr, self.level.getTile((tile[0]+1, tile[1]+1))) else 0
            diag += 8 if self.tileset.matchTerrain(terr, self.level.getTile((tile[0]-1, tile[1]+1))) else 0

            # Only one diagnal is valid, check using quick power of 2 check
            diag = ~diag & 15
            #print "Diag %i, %i" % (diag, diag & (diag-1))
            if diag & (diag-1) == 0:
                # Is this faster than log?
                while diag > 0:
                    offset += 1
                    diag >>= 1

        return offset

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
