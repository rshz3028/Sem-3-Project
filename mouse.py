import pygame,sys
from pygame.locals import *

class Mouse:

    def __init__(self):
        self.rect = pygame.Rect(0,0,8,8)
        self.surface = pygame.Surface((8,8))
        self.surface.fill((0,0,0))

        
