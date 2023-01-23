# script for game object classes


import pygame
from config import *
import math
import random

from pygame.locals import *

from mechanics_class import *
from config import *
from profiling import *

class Player(pygame.sprite.Sprite):
    ''' defining player character details and functions'''
    
    def __init__(self,game,spritesheet,x,y,sp_x,sp_y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites,self.game.active_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.spritesheet = spritesheet

        x = x*TILESIZE
        y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.ani_loop = 1

        self.image = self.spritesheet.get_sprite(sp_x,sp_y,13,19)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.SCROLLLEFT = False
        self.SCROLLRIGHT = False
        self.SCROLLUP = False
        self.SCROLLDOWN = False
        
    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change#*self.game.dt
        self.collision("x")
        self.rect.y += self.y_change#*self.game.dt
        self.collision("y")

        self.x_change = 0
        self.y_change = 0
        self.move_center()

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
            
    def collision(self,direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self,self.game.collide_blocks,False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self,self.game.collide_blocks,False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    
    def animate(self):
        up_ani = [self.spritesheet.get_sprite(10,39,10,17),
                  self.spritesheet.get_sprite(34,39,10,17),
                  self.spritesheet.get_sprite(59,39,10,17),
                  self.spritesheet.get_sprite(82,39,10,17)]
        down_ani = [self.spritesheet.get_sprite(11,9,10,17),
                  self.spritesheet.get_sprite(35,9,10,17),
                  self.spritesheet.get_sprite(59,9,10,17),
                  self.spritesheet.get_sprite(82,9,10,17)]
        left_ani = [self.spritesheet.get_sprite(11,69,8,17),
                  self.spritesheet.get_sprite(34,69,8,17),
                  self.spritesheet.get_sprite(59,70,8,17),
                  self.spritesheet.get_sprite(84,70,8,17)]
        right_ani = [self.spritesheet.get_sprite(11,97,8,17),
                  self.spritesheet.get_sprite(33,97,8,17),
                  self.spritesheet.get_sprite(58,98,8,17),
                  self.spritesheet.get_sprite(83,98,8,17)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = down_ani[0]
            else:
                self.image = down_ani[math.floor(self.ani_loop)]
                self.ani_loop += 0.1*self.game.dt
                if self.ani_loop>=3:
                    self.ani_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = up_ani[0]
            else:
                self.image = up_ani[math.floor(self.ani_loop)]
                self.ani_loop += 0.1*self.game.dt
                if self.ani_loop>=3:
                    self.ani_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = left_ani[0]
            else:
                self.image = left_ani[math.floor(self.ani_loop)]
                self.ani_loop += 0.1*self.game.dt
                if self.ani_loop>=3:
                    self.ani_loop = 1
                    
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = right_ani[0]
            else:
                self.image = right_ani[math.floor(self.ani_loop)]
                self.ani_loop += 0.1*self.game.dt
                if self.ani_loop>=3:
                    self.ani_loop = 1

    def move_center(self):
        self.x,self.y = 0,0
        self.x = (640 - self.rect.x)//20
        self.y = (400 - self.rect.y)//20
        for sprite in self.game.all_sprites:
            sprite.rect.x += self.x
            sprite.rect.y += self.y
        
class Block(pygame.sprite.Sprite):
    ''' a ground tile bloack class for different base tiles in the gae'''
    def __init__(self,game,spritesheet,x,y,sp_x,sp_y,collide=False):
        self.game = game
        self._layer = BLOCK_LAYER
        if collide:
            self.groups = self.game.all_sprites,self.game.blocks,self.game.collide_blocks,self.game.inactive_sprites
        else:
            self.groups = self.game.all_sprites,self.game.blocks,self.game.inactive_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = spritesheet.get_sprite(sp_x,sp_y,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def appear(self):
        pass

class Tree(pygame.sprite.Sprite):
    def __init__(self,game,spritesheet,x,y,collide=True):
        data = [(11,6),(65,4),(112,7)]
        sp_x,sp_y = random.choice(data)

        self.game = game
        self._layer = TREE_LAYER

        if collide:
            self.groups = self.game.all_sprites,self.game.collide_blocks,self.game.inactive_sprites
        else:
            self.groups = self.game.all_sprites,self.game.inactive_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE*2

        self.image = spritesheet.get_sprite(sp_x,sp_y,self.width,self.height)
        self.rect = pygame.Rect(self.x,self.y-32,self.width,self.height)
        





















            
