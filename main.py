import pygame,sys
from pygame.locals import *

pygame.init()

from menu import *
from mouse import *

# variables
sc_w = 1200
sc_h = 800

#Rects
SCREENRECT = pygame.Rect(0,0,sc_w,sc_h)

#Constants
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

#the Display
screen = pygame.display.set_mode((sc_w,sc_h))

#Cursor
cursor = Mouse()
CLICK = False

#Menu
menu = Canvas(screen)
newgame = NewGame()
loadgame = LoadGame()
settings = Settings()
exitgame = ExitGame()

#FPS
fps = 60
clock = pygame.time.Clock()

while True:

    screen.fill(BLACK)

    menu.draw()
    newgame.draw()
    loadgame.draw()
    settings.draw()
    exitgame.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
           (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
            
        if event.type == MOUSEBUTTONDOWN:
            if not CLICK: CLICK = True
            mouse_x,mouse_y = pygame.mouse.get_pos()
            cursor.rect.x,cursor.rect.y = mouse_x,mouse_y
            if newgame.rect.colliderect(cursor.rect):
                newgame.active_state()
            if loadgame.rect.colliderect(cursor.rect):
                loadgame.active_state()
            if settings.rect.colliderect(cursor.rect):
                settings.active_state()
            if exitgame.rect.colliderect(cursor.rect):
                exitgame.active_state()
        if event.type == MOUSEBUTTONUP:
            if CLICK: CLICK = False
                

    pygame.display.update()
    clock.tick(fps)

