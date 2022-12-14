import pygame,sys
from pygame.locals import *

from gameobjects import GameObject

class Canvas:
    rect = pygame.Rect(0,0,1200,800)
    surface = pygame.Surface((1200,800))
    surface.fill((255,255,255))

    def __init__(self,screen):
        self.screen = screen

    def draw(self):
        pygame.Surface.blit(self.screen,self.surface,self.rect)
    

class Button(GameObject):

    def __init__(self):
        self.rect = pygame.Rect(0,0,300,75)
        self.surface = pygame.Surface((300,75))
        self.surface.fill((255,0,0))

    def draw(self):
        pygame.Surface.blit(Canvas.surface,self.surface,self.rect)

class NewGame(Button):
    def __init__(self):
        self.rect = pygame.Rect(50,200,300,75)
        self.surface = pygame.Surface((300,75))
        self.surface.fill((255,0,0))
    def active_state(self):
        self.surface.fill((0,200,25))

class LoadGame(Button):
    def __init__(self):
        self.rect = pygame.Rect(50,280,300,75)
        self.surface = pygame.Surface((300,75))
        self.surface.fill((255,0,0))
    def active_state(self):
        self.surface.fill((0,200,25))

class Settings(Button):
    def __init__(self):
        self.rect = pygame.Rect(50,360,300,75)
        self.surface = pygame.Surface((300,75))
        self.surface.fill((255,0,0))
    def active_state(self):
        self.surface.fill((0,200,25))

class ExitGame(Button):
    def __init__(self):
        self.rect = pygame.Rect(50,440,300,75)
        self.surface = pygame.Surface((300,75))
        self.surface.fill((255,0,0))
    def active_state(self):
        pygame.quit()
        sys.exit()
    

















    

    
