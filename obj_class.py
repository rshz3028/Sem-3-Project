# script for game object classes


import pygame
from config import *
import math
import random

from pygame.locals import *

from mechanics_class import *
from config import *

class Player(pygame.sprite.Sprite):
    ''' defining player character details and functions'''
    def __init__(self,game,spritesheet,x,y,sp_x,sp_y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
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
##        self.scroll()
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collision("x")
        self.rect.y += self.y_change
        self.collision("y")

        self.x_change = 0
        self.y_change = 0
        self.move_center()

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            if self.SCROLLLEFT:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[K_RIGHT]:
            if self.SCROLLRIGHT:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[K_UP]:
            if self.SCROLLUP:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[K_DOWN]:
            if self.SCROLLDOWN:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

##    def scroll(self):
##        if self.rect.x >= WIN_W*0.75:
##            self.SCROLLRIGHT = True
##        else:
##            self.SCROLLRIGHT = False
##        if self.rect.x <= WIN_W*0.25:
##            self.SCROLLLEFT = True
##        else:
##            self.SCROLLLEFT = False
##        if self.rect.y >= WIN_H*0.75:
##            self.SCROLLDOWN = True
##        else:
##            self.SCROLLDOWN = False
##        if self.rect.y <= WIN_H*0.25:
##            self.SCROLLUP = True
##        else:
##            self.SCROLLUP = False

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
                self.ani_loop += 0.1
                if self.ani_loop>=3:
                    self.ani_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = up_ani[0]
            else:
                self.image = up_ani[math.floor(self.ani_loop)]
                self.ani_loop += 0.1
                if self.ani_loop>=3:
                    self.ani_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = left_ani[0]
            else:
                self.image = left_ani[math.floor(self.ani_loop)]
                self.ani_loop += 0.1
                if self.ani_loop>=3:
                    self.ani_loop = 1
                    
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = right_ani[0]
            else:
                self.image = right_ani[math.floor(self.ani_loop)]
                self.ani_loop += 0.1
                if self.ani_loop>=3:
                    self.ani_loop = 1

    def move_center(self):
        self.x,self.y = 0,0
        self.x = (640 - self.rect.x)
        self.y = (400 - self.rect.y)
        for sprite in self.game.all_sprites:
            sprite.rect.x += self.x
            sprite.rect.y += self.y   
        
class Block(pygame.sprite.Sprite):
    ''' a ground tile bloack class for different base tiles in the gae'''
    def __init__(self,game,spritesheet,x,y,sp_x,sp_y,collide=False):
        self.game = game
        self._layer = BLOCK_LAYER
        if collide:
            self.groups = self.game.all_sprites,self.game.blocks,self.game.collide_blocks
        else:
            self.groups = self.game.all_sprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = spritesheet.get_sprite(sp_x,sp_y,self.width,self.height)
        self.image.set_colorkey((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Tree(pygame.sprite.Sprite):
    def __init__(self,game,spritesheet,x,y,sp_x,sp_y,collide=False):
        self.game = game
        self._layer = BLOCK_LAYER
        if collide:
            self.groups = self.game.all_sprites,self.game.blocks,self.game.collide_blocks
        else:
            self.groups = self.game.all_sprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = spritesheet.get_sprite(sp_x,sp_y,self.width,self.height)
        self.image.set_colorkey((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


















            
