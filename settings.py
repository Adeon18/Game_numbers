'''
This module contains all of the game settings
'''

import pygame


# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (104, 243, 243)

# Game settings
WIDTH = 1200
HEIGHT = 960
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = (39, 174, 96)
# The size of a tile(helps when creating a map)
TILESIZE = 48
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_IMG = 'player.png'
PLAYER_HIT_RECT = pygame.Rect(0, 0, 35, 35)
PLAYER_LAYER = 2
PLAYER_HEALTH = 5
PLAYER_HEALTH_MAX = 10
PLAYER_ROT_SPEED = 250  # Deg per sec
PLAYER_SPEED = 300

MAX_SECONDS = 20

# Wall settings
WALL_IMG = 'wall.png'
WALL_LAYER = 1
# Boss settings
BOSS_IMG = 'boss.png'
# Key settings
KEY_IMG = 'key.png'
KEY_LAYER = 1
# Chest settings
CHEST_IMG = 'chest.png'

# BOB_RANGE = 5
# BOB_SPEED = 0.25

CANDY_IMG = 'candy.png'

KEY_SOUND = 'key_found.wav'
CORRECT_SOUND = 'correct_answer.wav'
WRONG_SOUND = 'wrong_answer.wav'

