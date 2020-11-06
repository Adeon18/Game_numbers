import pygame


# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (104, 243, 243)

# Game settings
WIDTH = 1200
HEIGHT = 960
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN
# The size of a tile(helps when creating a map)
TILESIZE = 48
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

PLAYER_IMG = 'player.png'
PLAYER_HIT_RECT = pygame.Rect(0, 0, 35, 35)
PLAYER_LAYER = 1
PLAYER_HEALTH = 5
PLAYER_ROT_SPEED = 250  # Deg per sec
PLAYER_SPEED = 300

BOX_IMG = 'grass.png'
BOX_LAYER = 2

KEY_IMG = 'key.png'
KEY_LAYER = 2


BOSS_XP = 15
EGG_XP = 5
