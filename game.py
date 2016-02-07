import pygame
from pygame.locals import *

from gamelib.game import GameClass, GameState
from gamelib.primitives import Point
from gamelib.asset import *
from testnpc import testnpc
from level import *


class Player(Entity):

    WALK_SPEED = 3

    def __init__(self, pos, anim_set):
        Entity.__init__(self, pos)
        self.money = 0
        self.hp = 25
        self.maxhp = 25
        self.invpos = -665
        self.animator = Animator(anim_set, Animator.MODE_LOOP, 15.0)
        self.animator.setAnim("idle")
    def inventory(self):
        #*Slide* into the DMs
        if self.invpos < 20:
            self.invpos+=35

    def update(self, dt):

        k = pygame.key.get_pressed()
        
        #Inventory Key
        if k[K_i]:
            self.inventory()
        elif self.invpos>-665:
            self.invpos-=50
        
        # Only update player anim with actual movement
        if k[K_w]:
            self.pos.y -= Player.WALK_SPEED
            self.animator.update(dt)
        elif k[K_s]:
            self.pos.y += Player.WALK_SPEED
            self.animator.update(dt)
        if k[K_a]:
            self.pos.x -= Player.WALK_SPEED
            self.animator.update(dt)
        elif k[K_d]:
            self.pos.x += Player.WALK_SPEED
            self.animator.update(dt)

    def render(self, surf, offset = None):
        screen_pos = self.pos + offset if offset else self.pos
        #inventory box:
        pygame.draw.rect(surf, (200,150,150), (30,self.invpos, 600, 400), 0)
        pygame.draw.rect(surf, (  0,  0,  0), (180,self.invpos + 50, 100, 100), 0)
        pygame.draw.rect(surf, (  0,  0,  0), (330,self.invpos + 50, 100, 100), 0)
        pygame.draw.rect(surf, (  0,  0,  0), (480,self.invpos + 50, 100, 100), 0)
        self.animator.render(surf, screen_pos.intArgs())
    def lookAt(self, pos):
        # Determine direction
        d =pos - self.pos
        frame = 0
        if d.x >= d.y:
            frame = 1 if d.x >= -d.y else 3
        else:
            frame = 0 if d.x >= -d.y else 2
       #Determine which anim set to use.
        if frame == 3:
            self.animator.setAnim("walk_up")
        if frame == 2:
            self.animator.setAnim("walk_left")
        if frame == 1:
            self.animator.setAnim("walk_right")
        if frame == 0:
            self.animator.setAnim("walk_down")

class RpgGame(GameClass):

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


class TestState(GameState):

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
        self.test = testnpc(Point(120, 120), self.player_anim)

        self.world = None


    def enter(self, level_file):
        """Called every time the game is switched to this state."""
        # Load level if it is different from our current one.
        if not self.world or self.world.lvlFile != level_file:
            self.world = Level(self.gc.SCREEN_SIZE, level_file)

    def processInput(self):
        """Called during normal update/render period for this state
           to process it's input."""
        # Just handle quit message for now.
        for e in pygame.event.get():
            if e.type == QUIT:
                self.gc.quit()
            elif e.type == KEYUP:
                if e.key == K_TAB:
                    from editor import EditorState
                    self.gc.changeState(EditorState, self.world)

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

# Keep game initialization code out of __main__ so
# that it can be started from the EditorState.
def startGame(initial_state, *args, **kargs):
    # Initialize Game
    game = RpgGame()
    game.initialize()

    # Start first state
    game.changeState(initial_state, *args, **kargs)

    # Main Game Loop
    while game.running:
        game.update()

    # Cleanup
    game.shutdown()


if __name__ == "__main__":
    startGame(TestState, "r00.lvl")

# end main

