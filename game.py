import pygame,os
from pygame.locals import *
from gamelib.game import GameClass, GameState
from gamelib.primitives import Point,Rectangle
from gamelib.asset import *
from testnpc import Companion
from level import *
from gamestates import *
import items
pygame.font.init()
FontInv=pygame.font.Font(None,15)

class Hud(Entity):
    def __init__(self,t):
        self.imagerepo=[pygame.image.load(os.path.join('data','images','apple.png'))]
        Entity.__init__(self)
        self.target = t
        self.targinv=t.inventory
        self.invpos = -665
        self.invlock = 0
    def update(self):
        mse=Point(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        k = pygame.key.get_pressed()

        #Inventory Key Press/Release
        if not k[K_TAB]:
            if self.invlock==4:self.invlock=0
            if self.invlock==1:self.invlock=3
        if k[K_TAB] and self.invlock==0:
            self.invpos=30
            self.invlock=1
        if k[K_TAB] and self.invlock==3:
            self.invlock=4
            self.invpos=-600


    def render(self,surf, offset = None):
        if self.invpos >-300:
            #Inv Background
            pygame.draw.rect(surf, (200,150,150), (30,self.invpos, 600, 400), 0)
            #Slot 1
            pygame.draw.rect(surf, (  0,  0,  0), (330,self.invpos + 50, 45, 45), 0)
            surf.blit(self.imagerepo[self.targinv[0].imgnum],(339,self.invpos+57))
            surf.blit(FontInv.render(str(self.targinv[0].stack),0,(255,255,255)),(360,self.invpos+72))
            #Slot 2
            #pygame.draw.rect(surf, (  0,  0,  0), (480,self.invpos + 50, 100, 100), 0)
            #surf.blit(self.imagerepo[self.targinv[1].imgnum],(350,self.invpos+50))


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

        #Greater food = More hungry; 100 = Starving; 50 = Indifferent; 0 = Very Full; (0-25 Could possibly give a buff)
        self.food = 50
    def give(self,item,quant):
        #give items
        for x in range(quant):
            self.inventory.append(item)
        #auto stack
        stack = self.inventory.count(item)
        self.inventory=list(set(self.inventory))
        self.inventory[self.inventory.index(item)].stack = stack
    def take(self,item,quant):
        #take items
        for x in self.inventory:
            if x.name == item:
                x.stack-=quant
                print x.stack
    def update(self, dt):

        k = pygame.key.get_pressed()

        # Only update player anim with actual movement
        if k[K_e]:
            for x in self.inventory:
                print "FOOD B4:" + str(self.food)
                x.Use()
                self.take("apple",1)
                print "FOOD AFRTER:" + str(self.food)

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
