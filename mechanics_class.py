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
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self,x,y,width,height):
        '''Function that gets a specific sprite from the loaded spritesheet'''
        sprite = pygame.Surface([width,height])
        sprite.set_colorkey((255,255,255))
        sprite.blit(self.sheet,(0,0),(x,y,width,height))
        return sprite

class Renderer:
    '''render engine class that renders sprites based on list data'''
    def __init__(self,game):
        self.game = game
##        self.map_val = self._smooth_noise(self.map_value_generator(1234))
##        self.save_map_vals(self.map_val)
        self.world_map = {}
        noise_map = self.load_map_vals("base_tile_values.json")
        self.world_map.update(noise_map)
        self.update_map()

    def _converter(self,a):
        b= {}
        if type(a) == list:
            for y,row in enumerate(a):
                for x,col in enumerate(row):
                    b[x,y] = col
        return b

    def save_map_vals(self,n):
        d = {}
        for y,row in enumerate(n):
            for x,col in enumerate(row):
                d[str((x,y))] = col
        with open("base_tile_values.json","w",encoding='UTF8') as file:
            json.dump(d,file,indent=2)

    def load_map_vals(self,file):

        def jsonKeys2int(x):
            if isinstance(x, dict):
                    return {eval(k):v for k,v in x.items()}
            return x
        
        map_vals = {}
        with open(file,'r',encoding='UTF8') as file:
            map_vals = json.load(file,object_hook=jsonKeys2int)
        return map_vals

    def update_map(self):
        '''placeholder function'''
        
        self.tilemap(self.world_map)
    
    def map_value_generator(self,seed):
        '''random map value generator using opensimplex module, returns a 2d list of floats'''
##        r = random.randint(0,1280)
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

    def _smooth_noise(self,l):
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
















        
