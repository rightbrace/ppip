# Import the needed libraries
import pygame
from pygame import * 

# Start pygame
pygame.init() 

# Non-adjustable constants
WINDOW_WIDTH = 1100 
WINDOW_HEIGHT = 600 
TILE_SIZE = 100

# Adjustable constants
WHITE = (255, 255, 255) 

DRAW_GRID = True

# Set up the window with a size and name
GAME_WINDOW = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
display.set_caption('Attack of the Vampire Pizzas!') 

# load an image, if only a name is provided, assume that it is a square tile (because most objects in this game are)
def load_img(filename, width=TILE_SIZE, height=TILE_SIZE):
    img = image.load(filename)
    surf = Surface.convert_alpha(img)
    return transform.scale(surf, (width, height))

# Get the Rect() object corresponding to a given row and column
def rect_from_position(row, col):
    return Rect(TILE_SIZE * col, TILE_SIZE * row, TILE_SIZE, TILE_SIZE)

# Load all of the assets
BACKGROUND = load_img('restaurant.jpg', WINDOW_WIDTH, WINDOW_HEIGHT)
VAMPIRE_PIZZA = load_img('vampire.png')

# Set up the game tiles
for row in range(6):
    for column in range(11):
        # IF we want the grid overlay (as decided by the DRAW_GRID constant), draw a box around some of the tiles
        if DRAW_GRID: 
                draw.rect(BACKGROUND, WHITE, rect_from_position(row, column), 1)  

# Track the game state with a boolean. game_running means we are playing
game_running = True 
while game_running: 
    # Handle clicking in the game, and trying to close the window
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            # If we're trying to close the window, both the game and program stop
            game_running = False
    
    # Draw some stuff
    GAME_WINDOW.blit(BACKGROUND, (0, 0)) 
    GAME_WINDOW.blit(VAMPIRE_PIZZA, (900, 400)) 

    # Make the changes visible onscreen
    display.update() 

# Tell pygame we're done
pygame.quit() 