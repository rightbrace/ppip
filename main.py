# Import the needed libraries
import pygame
from pygame import * 
from random import randint

# Start pygame
pygame.init() 

# Non-adjustable constants
WINDOW_WIDTH = 1100 
WINDOW_HEIGHT = 600 
TILE_SIZE = 100

# Adjustable constants
WHITE = (255, 255, 255) 

SPAWN_RATE = 360 

REG_SPEED = 2 
SLOW_SPEED = 1 

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

# VampireSprite is the main opponent. This class sets up a vampire, updates its logic, and draw it
class VampireSprite(sprite.Sprite): 
    def __init__(self): 
        super().__init__() 
        self.speed = REG_SPEED 
        self.image = VAMPIRE_PIZZA.copy() 
        y = 50 + randint(0, 4) * 100 
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH, y)) 

    def update(self, game_window): 
        # Draw it
        game_window.blit(self.image, (self.rect.x, self.rect.y)) 

# Here, we set up all of the game elements, and store them in varibles
all_vampires = sprite.Group() 

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
    
    # Every frame, paint over the whole screen with the background
    GAME_WINDOW.blit(BACKGROUND, (0, 0)) 

    # Very rarely, spawn a new vampire
    if randint(1, SPAWN_RATE) == 1: 
        all_vampires.add(VampireSprite())

    # Update every vampire
    for vampire in all_vampires: 
        vampire.update(GAME_WINDOW)

    # Make the changes visible onscreen
    display.update() 

# Tell pygame we're done
pygame.quit() 