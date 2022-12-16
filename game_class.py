import pygame,sys
from pygame.locals import *

from game_objs import *
from config import *

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W,WIN_H))
        self.clock = pygame.time.Clock()
        #self.font = pygame.font.Font(None,32)
        self.running = True

    def tilemap(self):
        for y,row in enumerate(MAP_VALUES):
            for x,col in enumerate(row):
                if col == 1:
                    Block(self,x,y)
                if col==2:
                    Player(self,x,y)
    
    def new(self):
        #new game
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.tilemap()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

        
    def update(self):
        self.all_sprites.update()

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


