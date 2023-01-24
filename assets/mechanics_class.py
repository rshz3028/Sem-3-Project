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
    world_map = {}
    def __init__(self,game):
        self.game = game
        Renderer.world_map = self.load_map_vals("base_tile_values.json")
        self.update_map()

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
        
        self.tilemap(Renderer.world_map)
    
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















        
