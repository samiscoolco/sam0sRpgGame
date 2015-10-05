import pygame
from pygame.locals import *

from level import *
from asset import *

class Controller(object):
    def __init__(self):
        self.area=[0,0]
    def update(self,playerobj):
        if playerobj.x>650:
            self.area[0]+=1
            print ("lel")
        tiles.update()


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
        #*Slide* into the DMs
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
        pygame.draw.circle(screen, (200,5,50), (self.invpos,32), 32, 0)
        self.animator.render(surf, screen_pos)


SCREEN_SIZE = (660,450)
DESIRED_FPS = 32

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
tiles = pygame.sprite.Group()
clock = pygame.time.Clock()

# load game assets
player_anim = AnimationSet("player_14.png", (16, 24))
player_anim.addAnim("walk_down", 0, 3)
player_anim.addAnim("walk_right", 4, 7)
player_anim.addAnim("walk_left", 8, 11)
player_anim.addAnim("walk_up", 12, 15)

world_tiles = TileSet("sands.png", (25, 25))
world = Level(SCREEN_SIZE, "r00.png", world_tiles)

go=True
p=Player(64,64, player_anim)
c=Controller()


while go:
    pygame.display.set_caption(str(clock.get_fps()))

    # updates
    clock.tick(DESIRED_FPS)
    dt = clock.get_time()/1000.0
    #c.update(p)
    #screen.blit(limages,(0,0))
    p.update(dt)

    # Keep player from leaving game world
    # This should eventually be moved into Player
    if p.x < 0:
        p.x = 1
    elif p.x >= world.size[0]:
        p.x = world.size[0] - 1
    if p.y < 0:
        p.y = 1
    elif p.y >= world.size[1]:
        p.y = world.size[1] - 1

    world.move((p.x, p.y))
   
    for e in pygame.event.get():
        if e.type == QUIT:
            go = False

    # render
    screen.fill((0,0,0))
    world.render(screen)
    p.render(screen)
    pygame.display.flip()

#print tiles.sprites()

pygame.display.quit()
quit()
    
