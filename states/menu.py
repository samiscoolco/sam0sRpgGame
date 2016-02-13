""" game states.py sam tubb """
from gamelib.game import GameState
from gamelib.primitives import Rectangle,Point
import pygame
from pygame.locals import *
import paths


class MenuState(GameState):

    def __init__(self):
        GameState.__init__(self)

        self.resume = False
        self.button1= Rectangle.fromPoints(Point(22,134),Point(104,172))
        self.button2= Rectangle.fromPoints(Point(21,218),Point(156,251))
        self.button3= Rectangle.fromPoints(Point(26,306),Point(146,336))

    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""
        self.menuimg=pygame.image.load(paths.getImagePath('menu.png'))

    def enter(self, resume = False):
        print "welcome to the menu"
        self.resume = resume

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
                        from states.world import WorldState
                        self.gc.changeState(WorldState, "r01.lvl" if not self.resume else None)
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

        self.button1= Rectangle.fromPoints(Point(520,320),Point(640,345))

    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""
        self.menuimg=pygame.image.load(paths.getImagePath('creds.png'))

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

        self.button1= Rectangle.fromPoints(Point(520,320),Point(640,345))

    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""
        self.menuimg=pygame.image.load(paths.getImagePath('opts.png'))

    def enter(self):
        print "welcome to the options page"

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
