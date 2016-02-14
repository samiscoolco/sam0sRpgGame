import pygame
from pygame.locals import *

from gamelib.game import GameClass, GameState
from gamelib import ui


class TestUI(GameClass):

    def __init__(self):
        GameClass.__init__(self)

        # Global Constants
        self.SCREEN_SIZE = (660, 450)
        self.DESIRED_FPS = 32

        # Itemize Global GameClass variables for reference
        # Anything here can be accessed in a GameState by self.gc.****
        self.screen = None
        self.clock = None
        self.time = 0
        self.time_step = 0.0

    def initialize(self):
        GameClass.initialize(self)

        # Init pygame
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.clock = pygame.time.Clock()

    def update(self):
        # Must be done before GameClass.update() so it can
        # be used by GameState this frame
        self.clock.tick(self.DESIRED_FPS)
        self.time = pygame.time.get_ticks()
        self.time_step = self.clock.get_rawtime()/1000.0

        GameClass.update(self)

    def shutdown(self):
        GameClass.shutdown(self)
        pygame.quit()

    def quit(self):
        # tell systems to shut down
        self.running = False

# end RpgGame


class MenuState(GameState):

    def __init__(self):
        GameState.__init__(self)

        self.testFrame = None


    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""
        self.testFrame = ui.Frame(pygame.Rect(180, 125, 300, 200))
        self.testFrame.addChild(ui.Text(pygame.Rect(0, 0, 300, 25), "Test Frame", True))
        self.testFrame.addChild(ui.Button(pygame.Rect(25, 150, 100, 25), "OK", self.buttonNotify))
        self.testFrame.addChild(ui.Button(pygame.Rect(175, 150, 100, 25), "Cancel", self.buttonNotify))

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
            elif e.type == USEREVENT:
                if e.usercode == ui.Events.BUTTON_CLICKED:
                    print "%s button clicked!" % (e.button.label)
            else:
                self.testFrame.processEvent(e)


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

        self.testFrame.render(self.gc.screen)

        pygame.display.flip()

    def buttonNotify(self, button):
        print "Callback %s button clicked!" % (button.label)

# end TestState


if __name__ == "__main__":

    # Initialize Game
    game = TestUI()
    game.initialize()

    # Start first state
    game.changeState(MenuState)

    # Main Game Loop
    while game.running:
        game.update()

    # Cleanup
    game.shutdown()

# end main

