import numpy as np
from scipy.ndimage import convolve
import pygame
from sys import exit

# Constants
# WIDTH, HEIGHT = 1200, 800
WIDTH, HEIGHT = 1600, 1000
# RECTSIZE = (10, 10) 
RECTSIZE = (2, 2) 
FPS = 10
MODES = ['wrap', 'constant']
MODE = 1 #index of MODES

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
# grid = np.zeros([HEIGHT//RECTSIZE[1], WIDTH//RECTSIZE[0]], dtype=np.uint8)
grid = np.zeros([HEIGHT//RECTSIZE[1], WIDTH//RECTSIZE[0]], dtype=bool)
kernel = np.ones((3,3), dtype=bool)
kernel[1,1] = 0
run=True
glider = False
gunglider = False
orientation = 0 # br, ur, ul, bl 
show = True

def asign_rect(grid, row, col):
    '''
    Assigns a rectangle in the grid in the position (row, col)

    Example:
    >>> grid = np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])
    >>> assign_rect(grid, 1, 1)
    >>> grid
    np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ])
    '''
    grid[row, col]=1
    return grid

def asign_glider(grid, row, col, orientation=0):

    '''
    Assigns a glider in the grid with center in the position (row, col)
    with orientation (0-3)

    Example:
    >>> grid = np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])
    >>> assign_glider(grid, 1, 1)
    >>> grid
    np.array([
        [0, 0, 1],
        [1, 0, 1],
        [0, 1, 1]
    ])
    '''

    if row+1 >= grid.shape[0]-1: row=grid.shape[0]-2
    if col+1 >= grid.shape[1]-1: col=grid.shape[1]-2

    if row < 1: row=1
    if col < 1: col=1

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


def asign_gunglider(grid, row, col, orientation=0):
    
    if row+4 >= grid.shape[0]-1: row=grid.shape[0]-5
    if col+18 >= grid.shape[1]-1: col=grid.shape[1]-19
    
    if row < 4: row=4
    if col < 17: col=17
    
    #blocks
    grid[row:row+2,col-17:col-15] = 1
    grid[row-2:row,col+17:col+19] = 1
    
    #right
    grid[row-2:row+1, col+3:col+5] = 1
    grid[row-3, col+5] = 1
    grid[row+1, col+5] = 1
    grid[row-4:row-2, col+7] = 1
    grid[row+1:row+3, col+7] = 1
    
    #left
    grid[row:row+3, col-7] = 1
    grid[row-1, col-6] = 1
    grid[row+3, col-6] = 1
    grid[row-2, col-5:col-3] = 1
    grid[row+4, col-5:col-3] = 1
    grid[row+1, col-3] = 1
    grid[row-1, col-2] = 1
    grid[row+3, col-2] = 1
    grid[row:row+3, col-1] = 1
    grid[row+1, col] = 1
    
    return grid

def draw_rect(grid, row, col, color=None, careful=False):
    '''
    Draws a rectangle in the display in (row, col) with color.
    If careful, will not overwrite a live cell and if not color
    will pick white for live and black for dead cells

    Examples:
    >>> draw_rect(grid, 1, 1)
    '''
    live = grid[row, col]
    if color is None: 
        # print('h')
        color = ALIVE if live else DEAD
        
    if not careful: pygame.draw.rect(DISPLAY, color, ((col*RECTSIZE[1], row*RECTSIZE[0]), RECTSIZE))
    else:
        if not live: pygame.draw.rect(DISPLAY, color, ((col*RECTSIZE[1], row*RECTSIZE[0]), RECTSIZE))

def draw_glider(grid, row, col, color, orientation=0):
    '''
    Draws a glider in the display with center in (row, col) with color
    with orientation (0-3)

    Examples:
    >>> draw_glider(grid, 1, 1, (70,70,70), 1)
    '''
    
    if row+1 >= grid.shape[0]-1: row=grid.shape[0]-2
    if col+1 >= grid.shape[1]-1: col=grid.shape[1]-2

    if row < 1: row=1
    if col < 1: col=1

    if orientation == 0:
        for i in range(-1,2):
            draw_rect(grid, row+i, col+1, color, True)
        draw_rect(grid, row+1, col, color, True)
        draw_rect(grid, row, col-1, color, True)

    if orientation == 1:
        for i in range(-1,2):
            draw_rect(grid, row+i, col+1, color, True)
        draw_rect(grid, row-1, col, color, True)
        draw_rect(grid, row, col-1, color, True)
    
    if orientation == 2:
        for i in range(-1,2):
            draw_rect(grid, row+i, col-1, color, True)
        draw_rect(grid, row-1, col, color, True)
        draw_rect(grid, row, col+1, color, True)
    
    if orientation == 3:
        for i in range(-1,2):
            draw_rect(grid, row+i, col-1, color, True)
        draw_rect(grid, row+1, col, color, True)
        draw_rect(grid, row, col+1, color, True)

def draw_gunglider(grid, row, col, color, orientation=0):
    if row+4 >= grid.shape[0]-1: row=grid.shape[0]-5
    if col+18 >= grid.shape[1]-1: col=grid.shape[1]-19
    
    if row < 4: row=4
    if col < 17: col=17

def update_grid(grid, run=True):
    '''
    Returns the next generation of the grid if run=True, else will return the same grid

    Examples:
    >>> ugrid = update_grid(grid)
    '''
    if run: 
        neighbors = convolve(grid.astype(np.uint8), kernel, mode=MODES[MODE])
        return (
            ((grid == 1) & (neighbors > 1) & (neighbors < 4))
            | ((grid == 0) & (neighbors == 3))
        )#.astype(np.uint8)

    return grid.copy()


def draw_grid(grid, ugrid):
    '''
    Draws the difference between grids

    Examples:
    >>> grid = np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])
    >>> ugrid = np.array([
        [0, 0, 1],
        [1, 0, 1],
        [0, 1, 1]
    ])
    >>> draw_grid(grid, ugrid) # will draw only the cells with 1s
    '''
    dfrows, dfcols = np.where(ugrid != grid)
    for row, col in zip(dfrows, dfcols): draw_rect(ugrid, row, col)

while True:
    
    # Get the next generation
    ugrid = update_grid(grid, run)
    
    # Parameters needed
    pos = pygame.mouse.get_pos()
    row, col = pos[1]//RECTSIZE[0], pos[0]//RECTSIZE[1]

    # Displays the object to place
    remove = False
    remove_glider=False
    if show:
        remove = True
        if glider:
            remove_glider=True
            draw_glider(ugrid, row, col, GREY, orientation)
        else:
            draw_rect(ugrid, row, col, GREY, careful=True) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run = not run

            if event.key == pygame.K_g:
                glider = not glider

            if event.key == pygame.K_p:
                gunglider = not gunglider
            
            if event.key == pygame.K_r:
                orientation = (orientation + 1)%4

            if event.key == pygame.K_d:
                ugrid = np.zeros_like(ugrid)
            
            if event.key == pygame.K_s:
                show = not show

            # if event.key == pygame.K_KP1:
            #     FPS = 10
            # if event.key == pygame.K_KP2:
            #     FPS = 20
            # if event.key == pygame.K_KP3:
            #     FPS = 30
            # if event.key == pygame.K_KP4:
            #     FPS = 40
            # if event.key == pygame.K_KP5:
            #     FPS = 50
            # if event.key == pygame.K_KP6:
            #     FPS = 60

    # Assigns the object to the grid
    if pygame.mouse.get_pressed()[0]:
        if gunglider: asign_gunglider(ugrid, row, col, orientation)
        elif glider: asign_glider(ugrid, row, col, orientation)
        else: asign_rect(ugrid, row, col)
    
    # Ones is everything placed, we draw the grid and update the display
    draw_grid(grid, ugrid)
    pygame.display.update()

    # Get ready for the next generation
    grid = ugrid
    
    # We clean the showed object
    if remove:
        if remove_glider:
            draw_glider(ugrid, row, col, BLACK, orientation)
        else:
            draw_rect(ugrid, row, col, BLACK, careful=True)
    # if run: CLOCK.tick(FPS)

# [convolve part](https://gist.github.com/mikelane/89c580b7764f04cf73b32bf4e94fd3a3) 
