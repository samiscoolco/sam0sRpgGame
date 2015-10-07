import pygame
from pygame.locals import *

from gamelib.game import GameClass, GameState
from gamelib.asset import *
from testnpc import testnpc
from level import *


class Player(Entity):

    WALK_SPEED = 3

    def __init__(self,x,y, anim_set):
        Entity.__init__(self, x, y)
        self.money = 0
        self.hp = 25
        self.maxhp = 25
        self.invpos=1

        self.animator = Animator(anim_set, Animator.MODE_LOOP, 15.0)

    def inventory(self):
        if self.invpos < 300:
            self.invpos+=4

    def update(self, dt):

        k=pygame.key.get_pressed()
        
        #Inventory Key
        if k[K_i]:
            self.inventory()
        elif self.invpos>-90:
            self.invpos-=5
        
        # Only update player anim with actual movement
        if k[K_w]:
            self.y -= Player.WALK_SPEED
            self.animator.setAnim("walk_up")
            self.animator.update(dt)
        elif k[K_s]:
            self.y += Player.WALK_SPEED
            self.animator.setAnim("walk_down")
            self.animator.update(dt)
        if k[K_a]:
            self.x -= Player.WALK_SPEED
            self.animator.setAnim("walk_left")
            self.animator.update(dt)
        elif k[K_d]:
            self.x += Player.WALK_SPEED
            self.animator.setAnim("walk_right")
            self.animator.update(dt)

    def render(self, surf):
        screen_pos = (self.x % SCREEN_SIZE[0], self.y % SCREEN_SIZE[1])
        pygame.draw.circle(surf, (200,5,50), (self.invpos,32), 32, 0)
        self.animator.render(surf, screen_pos)


# This should be removed and placed as an RpgGame Constant eventually
# We only need it now to have access to it in the Player class.
SCREEN_SIZE = (660, 450)

class RpgGame(GameClass):

    def __init__(self):
        GameClass.__init__(self)

        # Global Constants
        self.SCREEN_SIZE = SCREEN_SIZE
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

        self.player = Player(64, 64, self.player_anim)
        self.test = testnpc(120,120, self.player_anim)


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

        # Keep player from leaving game world
        # This should eventually be moved into Player
        p, w, t = self.player, self.world, self.test
        p.update(self.gc.time_step)
        t.update(self.gc.time_step)
        if p.x < 0:
            p.x = 1
        elif p.x >= w.size[0]:
            p.x = w.size[0] - 1
        if p.y < 0:
            p.y = 1
        elif p.y >= w.size[1]:
            p.y = w.size[1] - 1

        w.move((p.x, p.y))

    def render(self):
        """Called during normal update/render period for this state
           to render it's data in a specific way."""
        self.gc.screen.fill((0,0,0))
        self.world.render(self.gc.screen)
        self.player.render(self.gc.screen)
        self.test.render(self.gc.screen)
        pygame.display.flip()

# end TestState


if __name__ == "__main__":
    
    # Initialize Game
    game = RpgGame()
    game.initialize()

    # Start first state
    game.changeState(TestState)

    # Main Game Loop
    while game.running:
        game.update()

    # Cleanup
    game.shutdown()
# end main
