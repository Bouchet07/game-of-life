import numpy as np
import pygame
from sys import exit

# Constants
WIDTH, HEIGHT = 1200, 800
RECTSIZE = (10, 10) 
FPS = 10

# Colors
WHITE = (220, 220, 220)
BLACK = (0, 0, 0)
GREY = (70, 70, 70)

ALIVE = WHITE
DEAD = BLACK

# Initialize
pygame.init()
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Game of life")
grid = np.zeros([HEIGHT//RECTSIZE[1], WIDTH//RECTSIZE[0]])
run=True
glider = False
orientation = 0 # br, ur, ul, bl 
show = True

def asign_rect(grid, row, col):
    grid[row, col]=1
    return grid

def asign_glider(grid, row, col, orientation=0):

    if orientation == 0:
        grid[row-1:row+2, col+1] = 1
        grid[row+1,col] = 1
        grid[row, col-1] = 1

    if orientation == 1:
        grid[row-1:row+2, col+1] = 1
        grid[row-1,col] = 1
        grid[row, col-1] = 1
    
    if orientation == 2:
        grid[row-1:row+2, col-1] = 1
        grid[row-1,col] = 1
        grid[row, col+1] = 1
    
    if orientation == 3:
        grid[row-1:row+2, col-1] = 1
        grid[row+1,col] = 1
        grid[row, col+1] = 1
    return grid

def draw_glider(row, col, color, orientation=0):
    if orientation == 0:
        for i in range(-1,2):
            draw_rect(1, row+i, col+1, color)
        draw_rect(1, row+1, col, color)
        draw_rect(1, row, col-1, color)

    if orientation == 1:
        for i in range(-1,2):
            draw_rect(1, row+i, col+1, color)
        draw_rect(1, row-1, col, color)
        draw_rect(1, row, col-1, color)
    
    if orientation == 2:
        for i in range(-1,2):
            draw_rect(1, row+i, col-1, color)
        draw_rect(1, row-1, col, color)
        draw_rect(1, row, col+1, color)
    
    if orientation == 3:
        for i in range(-1,2):
            draw_rect(1, row+i, col-1, color)
        draw_rect(1, row+1, col, color)
        draw_rect(1, row, col+1, color)

def draw_rect(live, row, col, color=None):
    if color is None: color = ALIVE if live else DEAD
    pygame.draw.rect(DISPLAY, color, ((col*RECTSIZE[1], row*RECTSIZE[0]), RECTSIZE))

def update_grid(grid, run=True):
    if not run: 
        for row, col in np.ndindex(grid.shape): draw_rect(grid[row, col], row, col)
        return grid

    updated_grid = np.zeros_like(grid)
    for row, col in np.ndindex(grid.shape):
        # Rules
        neighbour_alive = np.sum(grid[row-1:row+2,col-1:col+2]) - grid[row,col]
        if grid[row,col]: # Alive
            if 2 <= neighbour_alive <= 3: updated_grid[row, col] = 1
        else: # Dead
            if neighbour_alive == 3: updated_grid[row, col] = 1
        draw_rect(updated_grid[row, col], row, col)
    return updated_grid
        

while True:
    
    grid = update_grid(grid, run)
    pos = pygame.mouse.get_pos()
    row, col = pos[1]//RECTSIZE[0], pos[0]//RECTSIZE[1]
    if show:
        if glider:
            draw_glider(row, col, GREY, orientation)
        else:
            draw_rect(1, row, col, GREY) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run = not run

            if event.key == pygame.K_g:
                glider = not glider

            if event.key == pygame.K_r:
                orientation = (orientation + 1)%4

            if event.key == pygame.K_d:
                grid = np.zeros_like(grid)
            
            if event.key == pygame.K_s:
                show = not show

            if event.key == pygame.K_KP1:
                FPS = 10
            if event.key == pygame.K_KP2:
                FPS = 20
            if event.key == pygame.K_KP3:
                FPS = 30
            if event.key == pygame.K_KP4:
                FPS = 40
            if event.key == pygame.K_KP5:
                FPS = 50
            if event.key == pygame.K_KP6:
                FPS = 60

    if pygame.mouse.get_pressed()[0]:
        if glider: asign_glider(grid, row, col, orientation)
        else: asign_rect(grid, row, col)

    pygame.display.update()
    if run: CLOCK.tick(FPS)
