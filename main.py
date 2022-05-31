import numpy as np
import pygame
from time import sleep

# Constants
WIDTH, HEIGHT = 800, 600
SIZE = (WIDTH, HEIGHT)
RECTSIZE = (10, 10)


ALIVE = (220, 220, 220)
DEAD = (0, 0, 0)
BORDER = (30, 30, 30)


# Initialize
pygame.init()
DISPLAY = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Game of life")
grid = np.zeros([HEIGHT//10, WIDTH//10])
grid[10:12,12:14] = 1
grid[30:33,:] = 1



def update_grid(grid, draw=True):
    updated_grid = np.zeros_like(grid)
    for row, col in np.ndindex(grid.shape):
        # Rules
        neighbour_alive = np.sum(grid[row-1:row+2,col-1:col+2]) - grid[row,col]
        if grid[row,col]: # Alive
            if 2 <= neighbour_alive <= 3: updated_grid[row, col] = 1
        else: # Dead
            if neighbour_alive == 3: updated_grid[row, col] = 1
        if draw:
            color = ALIVE if grid[row,col] else DEAD
            pygame.draw.rect(DISPLAY, color, ((col*RECTSIZE[1], row*RECTSIZE[0]), RECTSIZE))
    return updated_grid
        

game = True
while game:
    updated_grid = update_grid(grid)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game=False
    sleep(0.01)
    grid = updated_grid
pygame.quit()