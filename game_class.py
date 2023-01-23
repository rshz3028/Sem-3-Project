import pygame,sys,json,time
from pygame.locals import *

from mechanics_class import *
from obj_class import *
from config import *
from profiling import *

class Game:
    ''' main game class that stitches functions from other scripts to run the game'''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W,WIN_H))
        self.screen_rect = pygame.Rect(0,0,WIN_W,WIN_H)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None,32)
        self.running = True

        self.player_spritesheet = SpriteLoader("assets/player.png")
        self.base_tiles = SpriteLoader("assets/tile_spritesheet.png")
        self.objs_spritesheet = SpriteLoader("assets/trees.png")

        self.last_time = time.time() 
        self.dt = time.time()-self.last_time

    @profile
    def new(self):
        #new game
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.active_sprites = pygame.sprite.LayeredUpdates()
        self.player_group = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.collide_blocks = pygame.sprite.LayeredUpdates()

        self.player = Player(self,self.player_spritesheet,200,125,11,9)
        self.renderer = Renderer(self)

##        self.all_sprites.update()
 
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def update(self):
        #self.player_group.update()
        
        self.dt = time.time() - self.last_time
        self.dt*=60
        self.last_time = time.time()

        self.screen_rect.center = self.player.rect.center

##        for i in self.all_sprites:
##            if self.screen_rect.contains(i):
        print(self.clock.tick())
        
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass


 
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()


