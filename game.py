import pygame
from pygame.locals import *

from gamelib.game import GameClass, GameState
from gamelib.primitives import Point,Rectangle
from gamelib.asset import *
from testnpc import Companion
from level import *
from gamestates import *
import items

class Hud(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.invpos = -665
        self.invlock = False
        self.lockrect=Rectangle.fromPoints(Point(40,self.invpos+10),Point(72,self.invpos+32))
    def update(self):
        mse=Point(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        k = pygame.key.get_pressed()
        self.lockrect=Rectangle.fromPoints(Point(40,self.invpos+10),Point(72,self.invpos+42))
        #Inventory Key
        if k[K_TAB]:
            if self.invpos < 20:
                self.invpos+=35
            self.invlock=False
        elif self.invpos>-665 and self.invlock == False:
            if self.lockrect.contains(mse):
                self.invlock=True
                self.invpos=20
            else:
                self.invpos-=50
        
    def render(self,surf, offset = None):
        pygame.draw.rect(surf, (200,150,150), (30,self.invpos, 600, 400), 0)
        pygame.draw.rect(surf, (  0,  0,  0), (40,self.invpos + 10, 32, 32), 0)
        pygame.draw.rect(surf, (  0,  0,  0), (330,self.invpos + 50, 100, 100), 0)
        pygame.draw.rect(surf, (  0,  0,  0), (480,self.invpos + 50, 100, 100), 0)


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
        self.mouseoffset = 0
        self.invdock = False
        self.inventory = []
    def update(self, dt):

        k = pygame.key.get_pressed()
        
        #Inventory Key
        if k[K_i]:
            print self.inventory
            self.inventory[0].destroy()
            if self.invpos < 20:
                self.invpos+=35
        elif self.invpos>-665 and self.invdock == False:
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
        
if __name__ == "__main__":
    
    # Initialize Game
    game = RpgGame()
    game.initialize()
    # Start first state
    game.changeState(MenuState)

    # Main Game Loop
    while game.running:
        game.update()

    # Cleanup
    game.shutdown()
# end main

