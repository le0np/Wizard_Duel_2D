# This is my first Python project and it is just a simple duel-style game 
# Background music downloaded from https://pixabay.com/music/main-title-risk-136788/

import pygame as py
import os

# Initialize Pygame fonts and sound mixer
py.font.init()
py.mixer.init()


# Game environment variables   
WIDTH, HEIGHT = 1000, 500
WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("WizardWars")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 ,0)
BLUE = (0,0,255)

# Define a Pygame Rect object to create the center line
BORDER = py.Rect(WIDTH//2 -5, 0, 10, HEIGHT)

# Load spell sound effects and music
SPELL_CAST_SOUND = py.mixer.Sound(os.path.join('Assets','spell_fired.wav' ))
SPELL_HIT_SOUND = py.mixer.Sound(os.path.join('Assets','spell_hit_sound.mp3' ))

# Load background music
py.mixer.music.load('Assets/risk.mp3')

# Play the background music
py.mixer.music.play(-1)  # the '-1' will loop the music indefinitely

# Set the volume of the background music
py.mixer.music.set_volume(0.4)  # a value between 0 and 1

# Initialize Pygame fonts
HEALTH_FONT = py.font.SysFont('comicsans', 40)
WINNER_FONT = py.font.SysFont('comicsans', 100)

# Define game variables   
FPS = 60 
VELOCITY = 5 
SPELL_VELOCITY = 7

# Define character, spells size and maximum number of spells on screen
WIZARD_WIDTH, WIZARD_HEIGHT = 65, 75
MAX_SPELL = 5

# Define Pygame custom events to be used for handling spell collisions
RED_HIT = py.USEREVENT + 1
BLUE_HIT = py.USEREVENT + 2


# Load character,spells images and background 
RED_WIZARD_IMAGE = py.image.load(
    os.path.join('Assets','red_mage.png'))
RED_WIZARD = py.transform.scale(RED_WIZARD_IMAGE, (WIZARD_WIDTH, WIZARD_HEIGHT))

BLUE_WIZARD_IMAGE = py.image.load(
    os.path.join('Assets','blue_mage.png'))
BLUE_WIZARD = py.transform.scale(BLUE_WIZARD_IMAGE, (WIZARD_WIDTH, WIZARD_HEIGHT))

MAP = py.transform.scale(py.image.load(
    os.path.join('Assets', 'map3.jpg')), (WIDTH, HEIGHT))

# Draw the game window and its components 
def draw_window(red, blue, red_spells, blue_spells, red_health, blue_health):
    WIN.blit(MAP, (0, 0))
    py.draw.rect(WIN, BLACK, BORDER)

    # Draw health bars
    red_health_text = HEALTH_FONT.render(
    "Health:" + str(red_health), 1, WHITE)
    
    blue_health_text = HEALTH_FONT.render(
    "Health:" + str(blue_health), 1, WHITE)

    # Draw characters and their spells
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(blue_health_text, (10, 10))

    WIN.blit(RED_WIZARD, (red.x, red.y))
    WIN.blit(BLUE_WIZARD, (blue.x, blue.y))
    
    for spell in red_spells:
        py.draw.rect(WIN, RED, spell)

    for spell in blue_spells:
        py.draw.rect(WIN, BLUE, spell)
    
    # Update the display 
    py.display.update()  

# Define red character movements 
def red_wizard_movement(keys_pressed, red):
        if keys_pressed[py.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width :  # LEFT
            red.x -= VELOCITY
        if keys_pressed[py.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH : # RIGHT  
            red.x += VELOCITY
        if keys_pressed[py.K_UP] and red.y - VELOCITY > 0 : # UP 
            red.y -= VELOCITY
        if keys_pressed[py.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT : # DOWN 
            red.y += VELOCITY

# Define blue character movements 
def blue_wizard_movement(keys_pressed, blue):
        if keys_pressed[py.K_a] and blue.x - VELOCITY > 0:  # LEFT 
            blue.x -= VELOCITY
        if keys_pressed[py.K_d] and blue.x + VELOCITY + blue.width < BORDER.x :# RIGHT 
            blue.x += VELOCITY
        if keys_pressed[py.K_w] and blue.y - VELOCITY > 0 : # UP 
            blue.y -= VELOCITY
        if keys_pressed[py.K_s] and blue.y + VELOCITY + blue.height < HEIGHT : # DOWN 
            blue.y += VELOCITY

# Define spell movements 
def handle_spells(red_spells, blue_spells, red, blue):
    for spell in red_spells:
        spell.x -= SPELL_VELOCITY
        if blue.colliderect(spell):
            py.event.post(py.event.Event(BLUE_HIT))
            red_spells.remove(spell)
        elif spell.x < 0 :  # remove spell if it goes out of screen
            red_spells.remove(spell)

    for spell in blue_spells:
        spell.x += SPELL_VELOCITY
        if red.colliderect(spell):
            py.event.post(py.event.Event(RED_HIT))
            blue_spells.remove(spell)
        elif spell.x > WIDTH:  # remove spell if it goes out of screen
            blue_spells.remove(spell)

# Define text on screen when someone wins   
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    py.display.update()
    py.time.delay(5000)

# Define main game window
def main():
    red = py.Rect(830, 430, WIZARD_WIDTH, WIZARD_HEIGHT)
    blue = py.Rect(10, 10, WIZARD_WIDTH, WIZARD_HEIGHT)

# Empty list for spells 
    red_spells = []
    blue_spells = []

    # Health bars 
    red_health = 10
    blue_health = 10
    
    # Game clock?
    clock = py.time.Clock()
    # Main game loop
    run = True
    while run:
        # Set FPS
        clock.tick(FPS)
        # Quit game on window close
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
            # Number,sound and size of projectiles on screen 
            if event.type == py.KEYDOWN:
                if event.key == py.K_LCTRL and len(blue_spells) < MAX_SPELL:
                    spell = py.Rect(
                        blue.x + blue.width, blue.y + blue.height//2 -2, 10, 5)
                    blue_spells.append(spell)
                    SPELL_CAST_SOUND.play()

                if event.key == py.K_RCTRL and len(red_spells) < MAX_SPELL:
                    spell = py.Rect(
                        red.x, red.y + red.height//2 -2, 10, 5)
                    red_spells.append(spell)
                    SPELL_CAST_SOUND.play()

            # Implementing damage
            if event.type == RED_HIT:
                red_health -= 1
                SPELL_HIT_SOUND.play()

            if event.type == BLUE_HIT:
                blue_health -= 1
                SPELL_HIT_SOUND.play()
        # Text on screen in case of either character win
        winner_text = ""
        if red_health <= 0:
            winner_text = "Blue Mage Wins!"

        if blue_health <= 0:
            winner_text = "Red Mage Wins!"  

        if winner_text != "":
            draw_winner(winner_text)
            break
        # Get keys pressed
        keys_pressed = py.key.get_pressed()
        # Move characters
        red_wizard_movement(keys_pressed, red)
        blue_wizard_movement(keys_pressed, blue)
        # Handle spells 
        handle_spells(red_spells, blue_spells, red, blue)
        # Draw game window
        draw_window(red, blue, red_spells, blue_spells, red_health, blue_health)
    main()

if __name__ == "__main__":
    main()


