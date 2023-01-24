import pygame,sys,json,time
from pygame.locals import *

from mechanics_class import *
from obj_class import *
from config import *
from profiling import *

class Menu:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((600,600))
        self.font = pygame.font.SysFont('Bodoni MT',20)

        self.click = False
        self.clock = pygame.time.Clock()

    def draw_text(self,text,font,color,surface,x,y):
        text_obj = font.render(text,True,color)
        self.text_rect = text_obj.get_rect()
        self.text_rect.topleft = (x,y)
        surface.blit(text_obj,self.text_rect)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

    def main(self):
        
        while True:
            
            self.screen.fill((255,255,255))
            mx,my = pygame.mouse.get_pos()

            self.draw_text("New Game",self.font,(255,0,0),self.screen,150,150)
            if self.text_rect.collidepoint((mx,my)):
                if self.click:
                    self.screen.fill((255,0,0))
                    Game()
                self.screen = pygame.display.set_mode((800,600))
            
            self.click = False
            self.event()
            pygame.display.update()
            self.clock.tick(FPS)

    def update(self):
        self.main()

class Game:
    ''' main game class that stitches functions from other scripts to run the game'''
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((WIN_W,WIN_H),FLAGS)
        pygame.display.set_caption("The Lost")
        icon = pygame.image.load("assets/icon.png").convert()
        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None,32)
        self.running = True

        self.player_spritesheet = SpriteLoader("assets/player.png")
        self.base_tiles = SpriteLoader("assets/tile_spritesheet.png")
        self.objs_spritesheet = SpriteLoader("assets/trees.png")

        self.last_time = time.time() 
        self.dt = time.time()-self.last_time

        self.main()
        
    def new(self):
        #new game
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.active_sprites = pygame.sprite.LayeredUpdates()
        self.inactive_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.collide_blocks = pygame.sprite.LayeredUpdates()

        self.player = Player(self,self.player_spritesheet,200,125,14,12)
        self.renderer = Renderer(self)
 
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.playing = False
                    self.running = False

    def update(self):
        
        self.dt = time.time() - self.last_time
        self.dt*=60
        self.last_time = time.time()
        
    def draw(self):
        self.screen.fill(BLACK)
        
        for sprite in self.all_sprites:
            if (abs(sprite.rect.x - self.player.rect.x) < (WIN_W ) and \
       (abs(sprite.rect.y - self.player.rect.y)) < WIN_H):
                sprite.update() 
                self.screen.blit(sprite.image,sprite.rect)
            
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        self.new()
        while self.running:
            while self.playing:
                self.events()
                self.update()
                self.draw()
            self.running = False
        self.playing = False
        self.running = False



if __name__ == '__main__':
    main_menu = Menu()
    while True:
        main_menu.update()






        


