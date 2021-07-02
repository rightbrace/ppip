# Import the needed libraries
import pygame
from pygame import * 

# Start pygame
pygame.init() 

# Non-adjustable constants
WINDOW_WIDTH = 1100 
WINDOW_HEIGHT = 600 

# Set up the window with a size and name
GAME_WINDOW = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
display.set_caption('Attack of the Vampire Pizzas!') 

# Track the game state with a boolean. game_running means we are playing
game_running = True 
while game_running: 
    # Handle clicking in the game, and trying to close the window
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            # If we're trying to close the window, both the game and program stop
            game_running = False
    
    # Make the changes visible onscreen
    display.update() 

# Tell pygame we're done
pygame.quit() 