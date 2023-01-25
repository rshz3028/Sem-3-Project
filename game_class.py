import pygame,sys,json,time
from pygame.locals import *

from mechanics_class import *
from obj_class import *
from config import *
from profiling import *



class Menu:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((MENU_W,MENU_H),pygame.NOFRAME)
        self.rect = self.screen.get_rect()
        self.font = pygame.font.SysFont(FONT,FONT_SIZE)

        pygame.display.set_caption("The Lost")
        icon = pygame.image.load("assets/icon.png").convert()
        pygame.display.set_icon(icon)

        self.click = False
        self.clock = pygame.time.Clock()

        self.chara = SpriteLoader("assets/Run.png")
        self.ani_cycle = [self.chara.get_sprite(10,29,48,61),
                     self.chara.get_sprite(77,31,54,59),
                     self.chara.get_sprite(150,28,49,62),
                     self.chara.get_sprite(218,27,51,63),
                     self.chara.get_sprite(288,30,48,60),
                     self.chara.get_sprite(366,31,54,59),
                     self.chara.get_sprite(428,28,48,62),
                     self.chara.get_sprite(482,27,45,63)]

        self.ani_var = 0

        self.last_time = time.time()
        self.dt = time.time()-self.last_time

    def chara_ani(self,num):

        image = self.ani_cycle[round(self.ani_var)]
        image_rect = image.get_rect(midbottom=self.rect.midbottom)
        image_rect.x = 450
        
        self.screen.blit(image,image_rect)
        self.ani_var +=0.1*self.dt
        if self.ani_var>num: self.ani_var = 0

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
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

    def main(self):
        
        while True:

            self.dt = time.time() - self.last_time
            self.dt*=60/0.8
            self.last_time = time.time()
            
            self.screen.fill((13,14,46))
            mx,my = pygame.mouse.get_pos()

            self.draw_text("New Game",self.font,WHITE,self.screen,50,50)
            if self.text_rect.collidepoint((mx,my)):
                if self.click:
                    Game()
                    self.screen = pygame.display.set_mode((600,600))

            self.draw_text("Options",self.font,WHITE,self.screen,50,80)
            if self.text_rect.collidepoint((mx,my)):
                if self.click:
                    Options()

            self.draw_text("Quit Game",self.font,WHITE,self.screen,50,120)
            if self.text_rect.collidepoint((mx,my)):
                if self.click:
                    pygame.quit()
                    sys.exit()

            self.chara_ani(7)
            
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
        self.renderer = Renderer(self,new=False)
 
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

class Options(Menu):

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((MENU_W,MENU_H),pygame.NOFRAME)
        self.font = pygame.font.SysFont(FONT,FONT_SIZE)

        pygame.display.set_caption("The Lost")
        icon = pygame.image.load("assets/icon.png").convert()
        pygame.display.set_icon(icon)

        self.click = False
        self.clock = pygame.time.Clock()

        self.last_time = time.time()
        self.dt = time.time()-self.last_time
        
        self.main()

    def main(self):

        while True:

            self.dt = time.time() - self.last_time
            self.dt*=60/0.8
            self.last_time = time.time()
            
            self.screen.fill((13,14,46))
            mx,my = pygame.mouse.get_pos()

            self.draw_text("l",self.font,WHITE,self.screen,50,50)
            if self.text_rect.collidepoint((mx,my)):
                if self.click:
                    pass

            self.draw_text("Previous",self.font,WHITE,self.screen,50,120)
            if self.text_rect.collidepoint((mx,my)):
                if self.click:
                    break
            
            self.click = False
            self.event()
            pygame.display.update()
            self.clock.tick(80)


if __name__ == '__main__':
    main_menu = Menu()
    while True:
        main_menu.update()






        


