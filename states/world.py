
import pygame
from pygame.locals import *

from gamelib.game import GameState
from gamelib.asset import AnimationSet
from gamelib.primitives import Point

from game import Player,Hud
from level import Level
import items
from testnpc import Companion

class WorldState(GameState):

    def __init__(self):
        GameState.__init__(self)

        # For reference, actually set during initialize()
        self.player_anim = None
        self.world = None

        self.player = None

    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""

        # Load State Assets
        self.player_anim = AnimationSet("player_14.png", (16, 24))
        self.player_anim.addAnim("walk_down", 0, 3)
        self.player_anim.addAnim("walk_right", 4, 7)
        self.player_anim.addAnim("walk_left", 8, 11)
        self.player_anim.addAnim("walk_up", 12, 15)
        self.player_anim.addAnim("idle", 16, 19)#for npc right now

        self.player = Player(Point(64, 64), self.player_anim)
        self.player.give(items.Food(self.player,"apple",self.player.inventory),22)
        self.player.take("apple",3)
        self.test = Companion(Point(120, 120), self.player_anim)
        self.hud = Hud(self.player)


    def enter(self, level_file):
        """Called every time the game is switched to this state."""
        if not self.world or self.world.lvlFile != level_file:
            self.world = Level(self.gc.SCREEN_SIZE, level_file)

    def processInput(self):
        """Called during normal update/render period for this state
           to process it's input."""
        # Just handle quit message for now.
        for e in pygame.event.get():
            if e.type == QUIT:
                self.gc.quit()

    def update(self):
        """Called during normal update/render period for this state
           to update it's local or game data."""
        pygame.display.set_caption(str(self.gc.clock.get_fps()))
        #Mouse Position
        mse=pygame.mouse.get_pos()
        # Keep player from leaving game world
        # This should eventually be moved into Player
        p, w, t, h = self.player, self.world, self.test, self.hud

        p.update(self.gc.time_step)
        t.update(self.gc.time_step,p)
        h.update()
        if p.pos.x < 0:
            p.pos.x = 1
        elif p.pos.x >= w.size[0]:
            p.pos.x = w.size[0] - 1
        if p.pos.y < 0:
            p.pos.y = 1
        elif p.pos.y >= w.size[1]:
            p.pos.y = w.size[1] - 1

        # Have NPC look at player if they get close
        #if t.vision.contains(p.pos):
            #t.lookAt(p.pos)
        p.lookAt(Point(mse[0]+self.world.areaPos[0],mse[1]+self.world.areaPos[1]))
        w.move(p.pos.intArgs())

    def render(self):
        """Called during normal update/render period for this state
           to render it's data in a specific way."""
        self.gc.screen.fill((0,0,0))
        self.world.render(self.gc.screen)

        offset = -Point(*self.world.areaPos)
        self.player.render(self.gc.screen, offset)
        self.test.render(self.gc.screen, offset)
        self.hud.render(self.gc.screen, offset)
        pygame.display.flip()

# end WorldState
