
import pygame as pg



class TileSet(object):

    def __init__(self, filename, tile_size):

        self.tileSize = tile_size
        self.numTiles = 0
        self.tileCounts = (0,0)
        self.image = pg.image.load(filename)

        if self.image:
            self.tileCounts = (self.image.get_width()/tile_size[0],
                               self.image.get_height()/tile_size[1])
            self.numTiles = self.tileCounts[0] * self.tileCounts[1]


    def render(self, surf, pos, tile_idx):
        
        tileRect = self.getTileRect(tile_idx)
        surf.blit(self.image, pos, tileRect)


    def getTileRect(self, tile_idx):

        if tile_idx < 0 or tile_idx >= self.numTiles:
            raise IndexError()

        tx = tile_idx % self.tileCounts[0]
        ty = tile_idx / self.tileCounts[0]

        return pg.Rect((tx*self.tileSize[0], ty*self.tileSize[1]), self.tileSize)
        
#end TileSet



class AnimationSet(TileSet):

    def __init__(self, filename, tile_size):
        TileSet.__init__(self, filename, tile_size)

        self.anims = {}

    def addAnim(self, name, start_frame, end_frame):

        if name in self.anims or start_frame > end_frame:
            return False

        self.anims[name] = (start_frame, end_frame)
        return True

    def getAnim(self, name):
        return self.anims.get(name)

#end Animation



class Animator(object):

    MODE_STOPPED = 0
    MODE_PLAYONCE = 1
    MODE_LOOP = 2
    MODE_PINGPONG = 3
    MODE_PING = 3
    MODE_PONG = 4

    def __init__(self, animation_set, mode = 2, fps = 1.0):

        self.animset = animation_set
        self.mode = mode
        self.period = 1.0/fps
        self.frame = 0
        self.time = 0.0
        self.anim = (0, self.animset.numTiles-1)

    def update(self, dt):
        if self.mode == Animator.MODE_STOPPED:
            return

        self.time += dt
        if self.time > self.period:
            self.time -= self.period
            self.next()


    def next(self):
        anim = self.anim if self.anim else (0, self.animset.numTiles-1)
        if self.mode == Animator.MODE_PONG:
            self.frame -= 1
            if self.frame == anim[0]:
                self.mode = Animator.MODE_PING
        else:
            self.frame += 1
            if self.frame == anim[1]:
                if self.mode == Animator.MODE_PLAYONCE:
                    self.mode = Animator.MODE_STOPPED
                elif self.mode == Animator.MODE_PING:
                    self.mode = Animator.MODE_PONG
                else: #MODE_LOOP || MODE_STOPPED
                    self.frame = anim[0]


    def setAnim(self, name, mode = -1):
        anim = self.animset.getAnim(name)

        if anim != self.anim:
            self.anim = anim
            self.frame = self.anim[0]
            if mode >= 0:
                self.mode = mode
            print "anim set %s" % str(anim)


    def render(self, surf, pos):
        self.animset.render(surf, pos, self.frame)


    def finished(self):
        return self.mode == Animator.MODE_STOPPED

#end Animator