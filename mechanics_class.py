# script that define classes and function that run the game

import pygame
from pygame.locals import *

import opensimplex as sp
import json
import random

from obj_class import *
from config import *

class SpriteLoader:
    ''' class to load a spritesheet into memory '''
    def __init__(self,file,color=(255,255,255),alpha=False):
        if alpha:
            self.sheet = pygame.image.load(file).convert_alpha()
        self.sheet = pygame.image.load(file).convert()
        self.color = color

    def get_sprite(self,x,y,width,height):
        '''Function that gets a specific sprite from the loaded spritesheet'''
        sprite = pygame.Surface([width,height])
        sprite.set_colorkey(self.color)
        sprite.blit(self.sheet,(0,0),(x,y,width,height))
        return sprite

class Renderer:
    '''render engine class that renders sprites based on list data'''
    world_map = {}
    def __init__(self,game,new = True):
        self.game = game
        if new:
            self.new_game()
        else:
            self.load_game()

##    def loading(self,n):
##        task = threading.Thread(target=n)
##        task.start()
##        Load
##        while True:
##            if task.is_alive():
##                Loading()
##            else:
##                break
        

    def new_game(self):
        loading_screen = Loading()
        map_val =_smooth_noise(map_value_generator(1234))
        save_map_vals(map_val)
        Renderer.world_map = self.load_map_vals("base_tile_values.json")
        self.tilemap(Renderer.world_map)
        loading_screen.terminate()

    def load_game(self):
        loading_screen = Loading()
        Renderer.world_map = self.load_map_vals("base_tile_values.json")
        self.tilemap(Renderer.world_map)
        loading_screen.terminate()
    
    def load_map_vals(self,file):
        
        def jsonKeys2int(x):
            if isinstance(x, dict):
                    return {eval(k):v for k,v in x.items()}
            return x
        
        map_vals = {}
        with open(file,'r',encoding='UTF8') as file:
            map_vals = json.load(file,object_hook=jsonKeys2int)
        return map_vals
    
    def save_map_vals(n):
        d = {}
        for y,row in enumerate(n):
            for x,col in enumerate(row):
                d[str((x,y))] = col
        with open("base_tile_values.json","w") as file:
            json.dump(d,file,indent=2)

    def map_value_generator(seed):
        '''random map value generator using opensimplex module, returns a 2d list of floats'''
        r = seed
        print(f"seed: {r}")
        sp.seed(r)
        n = []
        for y in range(250):
            o = []
            for x in range(400):
                o.append(sp.noise2(x*0.2,y*0.2))
            n.append(o)
        return n

    def _smooth_noise(l):
        '''function used to smooth out noise values of a list l by checking
            with the values of the tiles around it. If a type of tile is in greater count make the current tile into that tile.
            This function returns a list of float values'''
        for y,row in enumerate(l):
            for x,col in enumerate(row):
                high_ground = 0
                grass = 0
                sand = 0
                water = 0
                deep_water = 0
                if x == len(row)-1 and y == len(l)-1:
                    neighb = [l[y][x-1],l[y-1][x],l[y-1][x-1]]
                elif x == len(row)-1:
                    neighb = [l[y][x-1],l[y+1][x],l[y-1][x],l[y-1][x-1],l[y+1][x-1]]
                elif y == len(l)-1:
                    neighb = [l[y][x+1],l[y][x-1],l[y-1][x],l[y-1][x-1],l[y-1][x+1]]
                else:
                    neighb = [l[y][x+1],l[y][x-1],l[y+1][x],l[y-1][x],l[y+1][x+1],l[y-1][x-1],l[y-1][x+1],l[y+1][x-1]]
                for i in neighb:
                    if i >= 0.5: high_ground += 1
                    elif i>=0.1 and i<=0.5: grass += 1
                    elif i>=-0.1 and i<=0.1: sand += 1
                    elif i>=-0.3 and i<=-0.1: water += 1
                    elif i<=-0.3: deep_water += 1
                if high_ground == max(high_ground,grass,sand,water,deep_water): l[y][x] = 0.51
                elif grass == max(high_ground,grass,sand,water,deep_water): l[y][x] = 0.2
                elif sand == max(high_ground,grass,sand,water,deep_water): l[y][x] = 0.0
                elif water == max(high_ground,grass,sand,water,deep_water): l[y][x] = -0.2
                elif deep_water == max(high_ground,grass,sand,water,deep_water): l[y][x] = -0.31
        return l
    
    def tilemap(self,n):
        for i in n:
            x,y = i
            a,b = random.choice([(0,0),(32,0)]) #ground tiles
            c,d = random.choice([(66,0),(101,0)]) #foilage
            e,f = random.choice([(0,64),(32,64)])
    
            if n[x,y] >= 0.5 :           #high ground
                Block(self.game,self.game.base_tiles,x,y,a,b)
                if random.randint(1,5)==2:
                    if random.randint(1,10) == 1:
                        Block(self.game,self.game.base_tiles,x,y,e,f)
                    else:
                        Block(self.game,self.game.base_tiles,x,y,c,d)
                    
            elif n[x,y] >=0.1 and n[x,y] <=0.5:        #grass plains
                Block(self.game,self.game.base_tiles,x,y,a,b)
                if random.randint(1,5)==2:
                    if random.randint(1,10) == 1:
                        Block(self.game,self.game.base_tiles,x,y,e,f)
                    else:
                        Block(self.game,self.game.base_tiles,x,y,c,d)
                    
            elif n[x,y] >= -0.1 and n[x,y] <= 0.1:      # sand
                Block(self.game,self.game.base_tiles,x,y,a,b)
                if random.randint(1,6) == 2:
                    Block(self.game,self.game.base_tiles,x,y,67,66,collide=True)
                    
            elif n[x,y] <= -0.1 and n[x,y] >= -0.3:     #trees
                Block(self.game,self.game.base_tiles,x,y,a,b)
                Block(self.game,self.game.base_tiles,x,y,c,d)
                Tree(self.game,self.game.objs_spritesheet,x,y)
                
            elif n[x,y] <= -0.3:     #trees
                Block(self.game,self.game.base_tiles,x,y,a,b)
                Block(self.game,self.game.base_tiles,x,y,c,d)
                Tree(self.game,self.game.objs_spritesheet,x,y)

import threading
class Loading:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_W, WIN_H),pygame.FULLSCREEN)
        self.font = pygame.font.SysFont(FONT,FONT_SIZE)

        self.font = pygame.font.SysFont(FONT, 100)
        self.clock = pygame.time.Clock()

        self.chara = SpriteLoader("assets/attack.png")
        self.ani_cycle = [
                     self.chara.get_sprite(11,0,68,86),
                     self.chara.get_sprite(79,0,68,86),
                     self.chara.get_sprite(151,0,68,86),
                     self.chara.get_sprite(220,0,68,86),
                     self.chara.get_sprite(297,0,68,86),
                     self.chara.get_sprite(373,0,68,86),
                     ]
        self.ani_var = 0
        self.running = True

        self.main()

    def draw_text(self,text,font,color,surface,x,y):
        text_obj = self.font.render(text,True,color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x,y)
        surface.blit(text_obj,text_rect)

    def animation(self):
        image = self.ani_cycle[round(self.ani_var)]
        rect = image.get_rect(center = (640,400))
        self.screen.blit(image,rect)
        self.ani_var +=0.1
        if self.ani_var>5: self.ani_var = 0

    def terminate(self):
        self.running = False

    def main(self):

        while self.running:
            
            self.screen.fill((13,14,46))

            self.animation()
            self.draw_text("Loading",FONT,WHITE,self.screen,640,300)
            
            pygame.display.update()
            self.clock.tick(FPS)
        









        
