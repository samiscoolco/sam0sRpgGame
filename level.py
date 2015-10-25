
from os import path
import json

import pygame as pg
from gamelib.primitives import Entity
from gamelib.asset import TileSet


class Tile (Entity):

    def __init__ (self,x,y,color):
        Entity.__init__(self, x, y)
        self.color=color

    def update(self):
        pg.draw.rect(screen, (self.color), (self.x,self.y,16,16), 0)

# end Tile


class Level(object):

    TILE_WIDTH = 50
    TILE_HEIGHT = 50


    def __init__(self, area_size, filename = None, tileset = None):

        self.name = ""
        self._worldImg = None
        self.size = None
        self._currArea = None
        self.areaPos = None
        self.areaSize = area_size
        self.numTiles = (int(area_size[0]/Level.TILE_WIDTH)+1,
                         int(area_size[1]/Level.TILE_HEIGHT)+1)
        self.tileset = tileset

        self.lvlFile = None
        self.imgFile = None

        if tileset:
            # pygame doesn't allow you to arbitrarily scale surfaces on blit,
            # so we must prescale the tileset to the tile size we want.
            if tileset.tileSize[0] != Level.TILE_WIDTH or tileset.tileSize[1] != Level.TILE_HEIGHT:
                tileset.resize((Level.TILE_WIDTH, Level.TILE_HEIGHT))

        if filename:
            self.load(filename)


    def load(self, filename):
        """Load a level from the given file."""

        # Sanity checks
        if not filename or len(filename) == 0:
            return False

        # Allow from loading from PNG as well as 'lvl' files
        base, ext = path.splitext(filename)
        if ext.lower() == ".png":
            self._worldImg = pg.image.load(filename)

            self.name = path.basename(base)
            self.name = path.basename(base)
            self.lvlFile = base + ".lvl"
            self.imgFile = filename
            if not self.tileset:
                raise ValueError("Manual Tileset required when loading Level from image!")

        elif ext.lower() == ".lvl":
            # Load from lvl file
            with open(filename) as level:
                self.lvlFile = filename

                data = json.load(level)
                print "Level Loaded: \n%s" % (data)
                self.name = data['name']
                tsImg = data['tilesetImage']
                self.imgFile = data['worldImage']

                if path.exists(tsImg):
                    self.tileset = TileSet(tsImg, tuple(data['tilesetSize']))

                else:
                    raise ValueError("TileSet Image %s Not Found!" % tsImg)

                if path.exists(self.imgFile):
                    self._worldImg = pg.image.load(self.imgFile)
                else:
                    raise ValueError("World Image %s Not Found!" % self.imgFile)

        else:
            return False

        # pygame doesn't allow you to arbitrarily scale surfaces on blit,
        # so we must prescale the tileset to the tile size we want.
        if self.tileset.tileSize[0] != Level.TILE_WIDTH or self.tileset.tileSize[1] != Level.TILE_HEIGHT:
            self.tileset.resize((Level.TILE_WIDTH, Level.TILE_HEIGHT))
                
        self.size = (self._worldImg.get_width() * Level.TILE_WIDTH,
                     self._worldImg.get_height() * Level.TILE_HEIGHT)

        # Generate first area at origin, just in case
        self._currArea = pg.Surface(self.areaSize)
        self._generateArea((0, 0))

        return True


    def save(self, filename = None):
        """Save current level state to file."""
        if not self.tileset:
            return False

        filename = filename if filename else self.lvlFile
        print "Level saving to %s" % filename
        with open(filename, 'w') as level:
            data = { 'name': self.name, 
                     'tilesetImage': self.tileset.filename,
                     'tilesetSize': self.tileset.srcTileSize,
                     'worldImage': self.imgFile
                    }
            json.dump(data, level, indent=True)

            # Save out world image in case it was edited
            pg.image.save(self._worldImg, self.imgFile)

            return True
        return False


    def render(self, surf):
        """Render the level to the given surface."""
        surf.blit(self._currArea, (0,0))


    def move(self, pos):
        """Move to another area of the map, possibly generating the a new area.

        pos - Absolute world position (not relative to area) to move to.
        Returns True when the move is to a new area.
        """
        # We don't have to do anything if the movement is still in the current area.
        if self.inArea(pos):
            return False

        # Check for world boundaries
        if 0 > pos[0] >= self.size[0] or \
           0 > pos[1] >= self.size[1]:
           return False

        # Calculate new area pos
        print "move%s" % str(pos)
        self._generateArea((int(pos[0]/self.areaSize[0]) * self.areaSize[0],
                            int(pos[1]/self.areaSize[1]) * self.areaSize[1]))
        return True


    def inArea(self, pos):
        if self.areaPos[0] <= pos[0] < (self.areaPos[0] + self.areaSize[0]) and \
           self.areaPos[1] <= pos[1] < (self.areaPos[1] + self.areaSize[1]):
           return True
        return False


    def getTileAt(self, pos):
        # Check for world boundaries
        if pos[0] < 0 or pos[0] >= self.size[0] or \
           pos[1] < 0 or pos[1] >= self.size[1]:
           return None
        return (int(pos[0]/Level.TILE_WIDTH), int(pos[1]/Level.TILE_HEIGHT))


    def getTilePos(self, tile):
        pos = (tile[0] * Level.TILE_WIDTH, tile[1] * Level.TILE_HEIGHT)
        # Check for world boundaries
        if pos[0] < 0 or pos[0] >= self.size[0] or \
           pos[1] < 0 or pos[1] >= self.size[1]:
           return None
        return pos


    def getTileRect(self, tile):
        pos = self.getTilePos(tile)
        if not pos:
            return None
        return pg.Rect(pos[0], pos[1], Level.TILE_WIDTH, Level.TILE_HEIGHT)


    def setTile(self, tile, ts_index):
        # Tile visual is stored in R value
        self._worldImg.set_at(tile, pg.Color(ts_index, 0, 0))

        # redraw area with new tile if it is currently visible
        if self.inArea(self.getTilePos(tile)):
            self._generateArea(self.areaPos)


    def _generateArea(self, pos):
        """Generate a new area."""
        print "_generateArea(%s)" % str(pos)
        # This is seperate from render() to allow caching the render to
        # _currArea to be used later by render().
        # Eventually, we will be rendering static object sprites on top
        # of the background image and shouldn't need to do that on every frame.
        tw, th = (Level.TILE_WIDTH, Level.TILE_HEIGHT)
        world_pos = (pos[0]/tw, pos[1]/th)
        print "World Pos - %s" % str(world_pos)
        self.areaPos = pos
        self._currArea.fill((0,0,255))
        for j in xrange(self.numTiles[1]):
            for i in xrange(self.numTiles[0]):
                #print str(i)+","+str(j)
                px = self._worldImg.get_at((world_pos[0] + i, world_pos[1] + j))
                targetRect = pg.Rect(i*tw,j*th,tw,th)
                if self.tileset:
                    pg.draw.rect(self._currArea, (128, 128, 128), targetRect, 1)
                    if px[2] == 176:
                        self.tileset.render(self._currArea, targetRect, 0)
                    elif px[0] == 0:
                        self.tileset.render(self._currArea, targetRect, 12)
                    else:
                        self.tileset.render(self._currArea, targetRect, px[0])
                else:
                    if px[0]==185:
                        #t = Tile(i*16,j*16,(185,122,87))
                        pg.draw.rect(self._currArea, (128,122,87), targetRect, 0)
                        #tiles.add(t)
                    if px[0]==32:
                        pg.draw.rect(self._currArea, (255,255,87), targetRect, 0)
                        #t = Tile(i*16,j*16,(255,255,0))
                        #tiles.add(t)
                    if px[2]==176:
                        pg.draw.rect(self._currArea, (239,228,176), targetRect, 0)
                        #t = Tile(i*16,j*16,(239,228,176))
                        #tiles.add(t)


# end Level