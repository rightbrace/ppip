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

# Let's quickly get some stuff on the screen, load the images first:
background_img = image.load('restaurant.jpg') 
background_surf = Surface.convert_alpha(background_img) 
BACKGROUND = transform.scale(background_surf, (WINDOW_WIDTH, WINDOW_HEIGHT)) 

pizza_img = image.load('vampire.png') 
pizza_surf = Surface.convert_alpha(pizza_img) 
VAMPIRE_PIZZA = transform.scale(pizza_surf, (100, 100)) 

# Track the game state with a boolean. game_running means we are playing
game_running = True 
while game_running: 
    # Handle clicking in the game, and trying to close the window
    for event in pygame.event.get(): 
        if event.type == QUIT: 
            # If we're trying to close the window, both the game and program stop
            game_running = False
    
    # Actually draw the things
    GAME_WINDOW.blit(BACKGROUND, (0, 0)) 
    GAME_WINDOW.blit(VAMPIRE_PIZZA, (900, 400)) 

    # Make the changes visible onscreen
    display.update() 

# Tell pygame we're done
pygame.quit() 