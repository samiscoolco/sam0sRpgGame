
import pygame as pg


class Entity(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

# end Entity


class Tile (Entity):

    def __init__ (self,x,y,color):
        Entity.__init__(self, x, y)
        self.color=color

    def update(self):
        pg.draw.rect(screen, (self.color), (self.x,self.y,16,16), 0)

# end Tile


class Level(object):

    TILE_WIDTH = 25
    TILE_HEIGHT = 25


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

        if tileset:
            # This feels wrong, but it is the only way to make sure the tiles are the right size
            if tileset.tileSize[0] != Level.TILE_WIDTH or tileset.tileSize[1] != Level.TILE_HEIGHT:
                newsize = (tileset.tileCounts[0] * Level.TILE_WIDTH, tileset.tileCounts[1] * Level.TILE_HEIGHT)
                print "resizing tileset from %s to %s" %  (tileset.image.get_size(), newsize)
                tileset.image = pg.transform.scale(tileset.image, newsize)
                tileset.tileSize = (Level.TILE_WIDTH, Level.TILE_HEIGHT)

        if filename:
            self.load(filename)

    def load(self, filename):
        """Load a level from the given file."""

        # Sanity checks
        if not filename or len(filename) == 0:
            return False

        # For now, all we are doing is loading the world image associated with
        # this level. Eventually, we should be loading from a level file that
        # has all of the enemy and item locations as well.
        self._worldImg = pg.image.load(filename)
        self.size = (self._worldImg.get_width() * Level.TILE_WIDTH,
                     self._worldImg.get_height() * Level.TILE_HEIGHT)
        self.name = filename

        # Generate first area at origin, just in case
        self._currArea = pg.Surface(self.areaSize)
        self._generateArea((0, 0))

        return True


    def save(self, filename):
        """Save current level state to file."""
        pass


    def render(self, surf):
        """Render the level to the given surface."""
        surf.blit(self._currArea, (0,0))


    def move(self, pos):
        """Move to another area of the map, possibly generating the a new area.

        pos - Absolute world position (not relative to area) to move to.
        Returns True when the move is to a new area.
        """
        # We don't have to do anything if the movement is still in the current area.
        if pos[0] >= self.areaPos[0] and pos[0] < (self.areaPos[0] + self.areaSize[0]) and \
           pos[1] >= self.areaPos[1] and pos[1] < (self.areaPos[1] + self.areaSize[1]):
           return False

        # Check for world boundaries
        if pos[0] < 0 or pos[0] >= self.size[0] or \
           pos[1] < 0 or pos[1] >= self.size[1]:
           return False

        # Calculate new area pos
        print "move%s" % str(pos)
        self._generateArea((int(pos[0]/self.areaSize[0]) * self.areaSize[0],
                            int(pos[1]/self.areaSize[1]) * self.areaSize[1]))
        return True


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