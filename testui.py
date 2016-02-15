import pygame
from pygame.locals import *

from gamelib.game import GameClass, GameState
from gamelib import ui
from gamelib.asset import TileSet
import paths


class TiledTheme(ui.Theme):

    TILE_SIZE = 25
    MIN_SIZE = TILE_SIZE * 2

    _TILE_FRAME = (
        24, 25, 26,
        32, 33, 34,
        40, 41, 42
    )

    _TILE_BUTTON = (
        0, 1, 2,
        8, 9, 10,
        16, 17, 18
    )

    _TILE_DOWN = (
        3, 4, 5,
        11, 12, 13,
        19, 20, 21
    )

    PADDING = MIN_SIZE

    DEBUG_COLOR = pygame.Color(128, 128, 128)

    def __init__(self, tileset):
        self.tileset = tileset
        self.tileset.resize((self.TILE_SIZE, self.TILE_SIZE))

    def drawFrame(self, surf, rect):
        self._fillRect(surf, rect, self._TILE_FRAME)

    def drawButton(self, surf, rect, state):
        self._fillRect(surf, rect, self._TILE_DOWN if state == ui.Button.DOWN else self._TILE_BUTTON)

    def _toTileSpace(self, src_rect):
        halfTile = self.TILE_SIZE/2
        return pygame.Rect(src_rect.left/self.TILE_SIZE, src_rect.top/self.TILE_SIZE,
                           (src_rect.width+halfTile)/self.TILE_SIZE, (src_rect.height+halfTile)/self.TILE_SIZE)

    def _drawTile(self, surf, tile_pos, idx):
        pos = (tile_pos[0]*self.TILE_SIZE, tile_pos[1]*self.TILE_SIZE)
        self.tileset.render(surf, pos, idx)

    def _fillRect(self, surf, rect, tilemap):
        trect = self._toTileSpace(rect)
        irect = trect.inflate(-2, -2)

        # Draw Corners
        self._drawTile(surf, trect.topleft, tilemap[0])
        self._drawTile(surf, (irect.right, trect.top), tilemap[2])
        self._drawTile(surf, irect.bottomright, tilemap[8])
        self._drawTile(surf, (trect.left, irect.bottom), tilemap[6])

        # Draw Sides
        if irect.width > 0:
            for x in xrange(irect.left, irect.right):
                self._drawTile(surf, (x, trect.top), tilemap[1])
                self._drawTile(surf, (x, irect.bottom), tilemap[7])
        if irect.height > 0:
            for y in xrange(irect.top, irect.bottom):
                self._drawTile(surf, (trect.left, y), tilemap[3])
                self._drawTile(surf, (irect.right, y), tilemap[5])

                # Fill middle
                for x in xrange(irect.left, irect.right):
                    self._drawTile(surf, (x, y), tilemap[4])

        # DEBUG GRID
        #pygame.draw.rect(surf, self.DEBUG_COLOR, rect, 1)

#end TiledTheme


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

        ui_tiles = TileSet(paths.getImagePath("rpggame-ui.png"), (16, 16))
        ui.setTheme(TiledTheme(ui_tiles))

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
        self.testFrame = ui.Frame(pygame.Rect(175, 125, 300, 200))
        self.testFrame.addChild(ui.Text(pygame.Rect(0, 0, 300, 25), "Test Frame", True))
        self.testFrame.addChild(ui.EditBox(pygame.Rect(25, 25, 250, TiledTheme.MIN_SIZE), "insert text"))
        self.testFrame.addChild(ui.CheckBox(pygame.Rect(25, 75, 100, TiledTheme.MIN_SIZE), "Unchecked", self.checked))
        self.testFrame.addChild(ui.Button(pygame.Rect(25, 125, 100, TiledTheme.MIN_SIZE), "OK", self.buttonNotify))
        self.testFrame.addChild(ui.Button(pygame.Rect(175, 125, 100, TiledTheme.MIN_SIZE), "Cancel", self.buttonNotify))


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

    def checked(self, checkbox):
        checkbox.checked = not checkbox.checked
        if checkbox.checked:
            checkbox.label = "Checked"
        else:
            checkbox.label = "Unchecked"

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

