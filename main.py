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
FRAME_RATE = 60

# Adjustable constants
WHITE = (255, 255, 255)
HIGHLIGHT_COLOUR = (238, 190, 47) 

SPAWN_RATE = 360 

STARTING_BUCKS = 15 
BUCK_RATE = 120 
STARTING_BUCK_BOOSTER = 1 

REG_SPEED = 2 
SLOW_SPEED = 1 

DRAW_GRID = True

# Set up the window with a size and name
GAME_WINDOW = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
display.set_caption('Attack of the Vampire Pizzas!') 

# Make a clock, this will regulate the framerate of the game
clock = time.Clock()

# load an image, if only a name is provided, assume that it is a square tile (because most objects in this game are)
def load_img(filename, width=TILE_SIZE, height=TILE_SIZE):
    img = image.load(filename)
    surf = Surface.convert_alpha(img)
    return transform.scale(surf, (width, height))

# Get the Rect() object corresponding to a given row and column
def rect_from_position(row, col):
    return Rect(TILE_SIZE * col, TILE_SIZE * row, TILE_SIZE, TILE_SIZE)

# Draw some text at a given position
def draw_text(game_window, font, text, x, y):
    surf = font.render(text, True, WHITE) 
    rect = surf.get_rect() 
    rect.x = x
    rect.y = y
    game_window.blit(surf, rect) 

# Load all of the assets
BACKGROUND = load_img('restaurant.jpg', WINDOW_WIDTH, WINDOW_HEIGHT)
VAMPIRE_PIZZA = load_img('vampire.png')
GARLIC = load_img('garlic.png')
CUTTER = load_img('pizzacutter.png')
PEPPERONI = load_img('pepperoni.png')

# Load the fonts
SMALL_FONT = font.Font('pizza_font.ttf', 25)

# VampireSprite is the main opponent. This class sets up a vampire, updates its logic, and draw it
class VampireSprite(sprite.Sprite): 
    def __init__(self): 
        super().__init__() 
        self.speed = REG_SPEED 
        self.image = VAMPIRE_PIZZA.copy() 
        y = 50 + randint(0, 4) * 100 
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH, y)) 
        self.health = 200

    def update(self, game_window, counters): 
    
        # Move leftward
        self.rect.x -= self.speed 

        # Find out where we are
        tile_row = tile_grid[self.rect.y//100] 
        vamp_left_side = self.rect.x//100 
        vamp_right_side = (self.rect.x + self.rect.width)//100 

        # Assume that we aren't touching a tile on the left or right
        right_tile = None
        left_tile = None
        # If we are, then update those assumptions...
        if 0 <= vamp_left_side <= 10: 
            left_tile = tile_row[vamp_left_side] 

        if 0 <= vamp_right_side <= 10: 
            right_tile = tile_row[vamp_right_side] 

        # If there is a tile to the left, hit it
        if not left_tile is None:
            self.attack(left_tile)
        # And if there is one on the right, that isn't the same as the one on the left,
        # hit it too.
        if not right_tile is None:
            if right_tile != left_tile:
                self.attack(right_tile)

        # Remove the vampire if it is out of health, or got to the left
        if self.health <= 0 or self.rect.x <= TILE_SIZE: 
            self.kill() 

        # Finally, draw it
        game_window.blit(self.image, (self.rect.x, self.rect.y)) 

    def attack(self, tile): 
        # If a vampire has been slowed, update its speed permanently to show that
        if tile.trap == SLOW: 
            self.speed = SLOW_SPEED 

        # Pizza cutters just deal damage every frame, so reduce its health
        if tile.trap == DAMAGE: 
            self.health -= 1 

        # There are other kinds of tiles, but if we don't handle them, they won't do anything, which
        # is convenient for InactiveTile, etc

# Counters will manage keeping track of all of the game variables that change over time
class Counters(object): 
    def __init__(self): 
        self.loop_count = 0 
        self.pizza_bucks = STARTING_BUCKS 
        self.buck_booster = STARTING_BUCK_BOOSTER

    def update(self, game_window): 
        # Increase the number of frames that have passed
        self.loop_count += 1 
        # Every few frames, award more bucks
        if self.loop_count % BUCK_RATE == 0: 
            self.pizza_bucks += self.buck_booster 

        # Draw the amount of money
        draw_text(game_window, SMALL_FONT, str(self.pizza_bucks), WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50)

# A trap object knows its kind, how expensive it is, and what it looks like.
# Since it doesn't need to do anything else, it only has an __init__ method
class Trap(object): 
    def __init__(self, trap_kind, cost, trap_img): 
        self.trap_kind = trap_kind 
        self.cost = cost 
        self.trap_img = trap_img 

# The TrapApplicator tracks which trap is selected (if any)
# Later, the PlayTile will check to see if the TrapApplicator has a selection,
# and if it does, it will set its own trap to the selection.
# In professional terms, this kind of object (a single use object that other objects
# look to for reference) is called a "Singleton"
class TrapApplicator(object): 
    def __init__(self): 
        self.selected = None 
    
    def select_trap(self, trap): 
        if trap.cost <= counters.pizza_bucks: 
            self.selected = trap 

    def select_tile(self, tile, counters): 
        self.selected = tile.set_trap(self.selected, counters)  

# Every part of the game will be represented by a tile. What they all have in common is that they have a rectangle
# for their position and size, and they refer to a trap in some way
class BackgroundTile(sprite.Sprite): 
    def __init__(self, rect): 
        super().__init__() 
        self.trap = None 
        self.rect = rect 

# A PlayTile represents tiles in the 'lanes' of the game. They can be either empty, or hold one trap in them
class PlayTile(BackgroundTile): 
    # When the user clicks, set_trap is called by TrapApplicator
    def set_trap(self, trap, counters): 
        # If TrapApplicator gave us a trap, and we don't have one already (self.trap is)
        if bool(trap) and self.trap is None: 
            # Pay the cost
            counters.pizza_bucks -= trap.cost 
            self.trap = trap 
            # In the case of the earning trap, we can increase the rate of bucks right away
            if trap == EARN: 
                counters.buck_booster += 1 

    # If and only if this PlayTile also holds a trap, draw the trap image
    def draw(self, game_window, trap_applicator): 
        if not self.trap is None: 
            game_window.blit(self.trap.trap_img, (self.rect.x, self.rect.y)) 

# ButtonTiles represent the three buttons along the bottom of the screen
class ButtonTile(BackgroundTile):   

    def __init__(self, rect, trap):
        super().__init__(rect)
        self.trap = trap

    # When clicked, if the player can afford to buy the trap, return that trap to the caller
    def set_trap(self, trap, counters): 
        if counters.pizza_bucks >= self.trap.cost: 
            return self.trap 

    # draw the button
    def draw(self, game_window, trap_applicator): 
        # Always draw the image of the trap it represents
        GAME_WINDOW.blit(self.trap.trap_img, (self.rect.x, self.rect.y))
        # But if it is also the selected trap, draw a rectangle around it
        if not trap_applicator.selected is None: 
            if trap_applicator.selected == self.trap: 
                draw.rect(game_window, HIGHLIGHT_COLOUR, (self.rect.x, self.rect.y, TILE_SIZE, TILE_SIZE), 5) 

# InactiveTiles do nothing, so we can call pass for both methods
class InactiveTile(BackgroundTile): 
    def set_trap(self, trap, counters): 
        pass 

    def draw(self, game_window, trap_applicator): 
        pass 


# Here, we set up all of the game elements, and store them in varibles
all_vampires = sprite.Group() 
counters = Counters() 

SLOW = Trap('SLOW', 5, GARLIC) 
DAMAGE = Trap('DAMAGE', 3, CUTTER) 
EARN = Trap('EARN', 7, PEPPERONI) 
trap_applicator = TrapApplicator() 

# Set up all of the game tiles. Start by turning tile_grid into a 2D array, and fill it with InactiveTiles
tile_grid = []
for row in range(6): 
    # Every row will be its own list
    row_of_tiles = [] 
    tile_grid.append(row_of_tiles) 

    # For every column in that row...
    for column in range(11): 
        # Add an InactiveTile at that position
        tile_rect = rect_from_position(row, column) 
        row_of_tiles.append(InactiveTile(tile_rect))   

# Go back and add our button tiles at set positions
tile_grid[5][2] = ButtonTile(rect_from_position(5, 2), SLOW)
tile_grid[5][3] = ButtonTile(rect_from_position(5, 3), DAMAGE)
tile_grid[5][4] = ButtonTile(rect_from_position(5, 4), EARN)

# Finally, replace the tiles over the lanes with PlayTiles instead of InactiveTiles
# (since PlayTiles are the only ones that can hold traps)
for column in range(2, 11):
    for row in range(0, 5):
        tile_grid[row][column] = PlayTile(rect_from_position(row, column))
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
        elif event.type == MOUSEBUTTONDOWN: 
            # If the user clicks, find out where
            coordinates = mouse.get_pos() 
            x = coordinates[0] 
            y = coordinates[1] 
            # Convert the click position to tile coordinates
            tile_y = y//100 
            tile_x = x//100 
            # Let the trap applicator deal with the click by passing it the tile
            # that the player clicked on
            trap_applicator.select_tile(tile_grid[tile_y][tile_x], counters)

    # Every frame, paint over the whole screen with the background
    GAME_WINDOW.blit(BACKGROUND, (0, 0)) 

    # Very rarely, spawn a new vampire
    if randint(1, SPAWN_RATE) == 1: 
        all_vampires.add(VampireSprite())

    # Update every vampire
    for vampire in all_vampires: 
        vampire.update(GAME_WINDOW, counters)

    # Draw every tile
    for tile_row in tile_grid: 
        for tile in tile_row: 
            tile.draw(GAME_WINDOW, trap_applicator) 

    # Tick all of the counters
    counters.update(GAME_WINDOW)
    # Make the changes visible onscreen
    display.update() 
    # Let the clock wait until the next frame should start
    clock.tick(FRAME_RATE)

# Tell pygame we're done
pygame.quit() 