import numpy as np
import pygame
from sys import exit

# Constants
WIDTH, HEIGHT = 1200, 800
SIZE = (WIDTH, HEIGHT)
RECTSIZE = (10, 10)
FPS = 10

# Colors
WHITE = (220, 220, 220)
BLACK = (0, 0, 0)
BORDER = (30, 30, 30)

ALIVE = WHITE
DEAD = BLACK

# Initialize
pygame.init()
DISPLAY = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Game of life")
grid = np.zeros([HEIGHT//10, WIDTH//10])
run=True
glider = False
orientation = 0 # br, ur, ul, bl 

def asign_rect(grid, pos):
    grid[pos[1]//RECTSIZE[0], pos[0]//RECTSIZE[1]]=1
    return grid

def asign_glider(grid, pos, orientation=0):
    row, col = pos[1]//RECTSIZE[0], pos[0]//RECTSIZE[1]
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

def draw_rect(grid, row, col):
    color = ALIVE if grid[row,col] else DEAD
    pygame.draw.rect(DISPLAY, color, ((col*RECTSIZE[1], row*RECTSIZE[0]), RECTSIZE))

def update_grid(grid, run=True):
    if not run: 
        for row, col in np.ndindex(grid.shape): draw_rect(grid, row, col)
        return grid

    updated_grid = np.zeros_like(grid)
    for row, col in np.ndindex(grid.shape):
        # Rules
        neighbour_alive = np.sum(grid[row-1:row+2,col-1:col+2]) - grid[row,col]
        if grid[row,col]: # Alive
            if 2 <= neighbour_alive <= 3: updated_grid[row, col] = 1
        else: # Dead
            if neighbour_alive == 3: updated_grid[row, col] = 1
        draw_rect(updated_grid, row, col)
    return updated_grid
        

while True:
    
    grid = update_grid(grid, run)

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
        pos = pygame.mouse.get_pos()
        if glider: asign_glider(grid, pos, orientation)
        else: asign_rect(grid, pos)

    pygame.display.update()
    if run: CLOCK.tick(FPS)
