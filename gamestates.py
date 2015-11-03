""" game states.py sam tubb """
from gamelib.game import GameState
from gamelib.primitives import Rectangle,Point
from gamelib.asset import *
import pygame
from pygame.locals import *
from level import *
from testnpc import testnpc
from game import Player

class TestState(GameState):

    def __init__(self):
        GameState.__init__(self)

        # For reference, actually set during initialize()
        self.player_anim = None
        self.world_tiles = None
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

        self.world_tiles = TileSet("sands.png", (25, 25))
        self.world = Level(self.gc.SCREEN_SIZE, "r00.png", self.world_tiles)

        self.player = Player(Point(64, 64), self.player_anim)
        self.test = testnpc(Point(120, 120), self.player_anim)


    def enter(self):
        """Called every time the game is switched to this state."""
        pass

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
        p, w, t = self.player, self.world, self.test
        p.update(self.gc.time_step)
        t.update(self.gc.time_step)
        if p.pos.x < 0:
            p.pos.x = 1
        elif p.pos.x >= w.size[0]:
            p.pos.x = w.size[0] - 1
        if p.pos.y < 0:
            p.pos.y = 1
        elif p.pos.y >= w.size[1]:
            p.pos.y = w.size[1] - 1

        # Have NPC look at player if they get close
        if t.vision.contains(p.pos):
            t.lookAt(p.pos)
        p.lookAt(Point(mse[0],mse[1]))
        w.move(p.pos.intArgs())

    def render(self):
        """Called during normal update/render period for this state
           to render it's data in a specific way."""
        self.gc.screen.fill((0,0,0))
        self.world.render(self.gc.screen)

        offset = -Point(*self.world.areaPos)
        self.player.render(self.gc.screen, offset)
        self.test.render(self.gc.screen, offset)
        pygame.display.flip()

# end TestState

class MenuState(GameState):

    def __init__(self):
        GameState.__init__(self)

        # For reference, actually set during initialize()
        self.player_anim = None
        self.world_tiles = None
        self.world = None

        self.player = None
        self.button1= Rectangle.fromPoints(Point(22,134),Point(104,172))
        self.button2= Rectangle.fromPoints(Point(21,218),Point(156,251))
        self.button3= Rectangle.fromPoints(Point(26,306),Point(146,336))
    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""
        self.menuimg=pygame.image.load("images\\menu.png")


    def enter(self):
        print "welcome to the menu"
        pass

    def processInput(self):
        mse=Point(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        """Called during normal update/render period for this state
           to process it's input."""
        # Just handle quit message for now.
        for e in pygame.event.get():
            if e.type == QUIT:
                self.gc.quit()
            if e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    if self.button1.contains(mse):
                        self.gc.changeState(TestState)
                    if self.button2.contains(mse):
                        self.gc.changeState(OptionsState)
                    if self.button3.contains(mse):
                        self.gc.changeState(CreditsState)

    def update(self):
        """Called during normal update/render period for this state
           to update it's local or game data."""
        pygame.display.set_caption(str(self.gc.clock.get_fps()))
        #Mouse Position
        mse=pygame.mouse.get_pos()

    def render(self):
        """Called during normal update/render period for this state
           to render it's data in a specific way."""
        self.gc.screen.fill((0,0,0))
        self.gc.screen.blit(self.menuimg,(0,0))
        pygame.display.flip()

#end menu state

class CreditsState(GameState):

    def __init__(self):
        GameState.__init__(self)

        # For reference, actually set during initialize()
        self.player_anim = None
        self.world_tiles = None
        self.world = None

        self.player = None
        self.button1= Rectangle.fromPoints(Point(520,320),Point(640,345))
    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""
        self.menuimg=pygame.image.load("images\\creds.png")


    def enter(self):
        print "welcome to the credit page"
        pass

    def processInput(self):
        mse=Point(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        """Called during normal update/render period for this state
           to process it's input."""
        # Just handle quit message for now.
        for e in pygame.event.get():
            if e.type == QUIT:
                self.gc.quit()
            if e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    if self.button1.contains(mse):
                        self.gc.changeState(MenuState)

    def update(self):
        """Called during normal update/render period for this state
           to update it's local or game data."""
        pygame.display.set_caption(str(self.gc.clock.get_fps()))
        #Mouse Position
        mse=pygame.mouse.get_pos()

    def render(self):
        """Called during normal update/render period for this state
           to render it's data in a specific way."""
        self.gc.screen.fill((0,0,0))
        self.gc.screen.blit(self.menuimg,(0,0))
        pygame.display.flip()

#end credits

class OptionsState(GameState):

    def __init__(self):
        GameState.__init__(self)

        # For reference, actually set during initialize()
        self.player_anim = None
        self.world_tiles = None
        self.world = None

        self.player = None
        self.button1= Rectangle.fromPoints(Point(520,320),Point(640,345))
    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""
        self.menuimg=pygame.image.load("images\\opts.png")


    def enter(self):
        print "welcome to the options page"
        pass

    def processInput(self):
        mse=Point(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        """Called during normal update/render period for this state
           to process it's input."""
        # Just handle quit message for now.
        for e in pygame.event.get():
            if e.type == QUIT:
                self.gc.quit()
            if e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    if self.button1.contains(mse):
                        self.gc.changeState(MenuState)

    def update(self):
        """Called during normal update/render period for this state
           to update it's local or game data."""
        pygame.display.set_caption(str(self.gc.clock.get_fps()))
        #Mouse Position
        mse=pygame.mouse.get_pos()

    def render(self):
        """Called during normal update/render period for this state
           to render it's data in a specific way."""
        self.gc.screen.fill((0,0,0))
        self.gc.screen.blit(self.menuimg,(0,0))
        pygame.display.flip()

#end options
