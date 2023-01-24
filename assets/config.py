import pygame

WIN_W = 1280 # window width
WIN_H = 800  # window height
FLAGS =pygame.FULLSCREEN|pygame.RESIZABLE|pygame.HWSURFACE|pygame.DOUBLEBUF
FPS = 0    # frame rate
TILESIZE = 32  # smallest pixel unit
CHUNKSIZE = 8


PLAYER_SPEED = 9  # player movement speed(7 pixels per frame)
PLAYER_LAYER = 3  # Layeredsurface class attribute
BLOCK_LAYER = 1   # Layeredsurface class attribute
TREE_LAYER = 2

# rgb values of colors
RED = (255,0,0)  
GREEN = (0,255,0) 
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
