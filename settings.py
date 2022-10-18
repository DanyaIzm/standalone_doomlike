""" GAME SETTINGS FILE """
import math
from dataclasses import dataclass

# SCREEN
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS_POS = (WIDTH - 65, 5)

# TIME
FPS = 60

# PLAYER SETTINGS
PLAYER_START_POS = (HALF_WIDTH, HALF_HEIGHT)
PLAYER_START_ANGLE = 0
PLAYER_NORMAL_SPEED = 2

# MAP SETTINGS
TILE_SIZE = 100

# MINIMAP SETTINGS
MAP_SCALE = 5
MAP_TILE_SIZE = TILE_SIZE // MAP_SCALE
MAP_POS = (0, HEIGHT - HEIGHT // MAP_SCALE)

# RAY CASTINGS SETTINGS
FOV = math.pi / 3                               # field of view
HALF_FOV = FOV / 2
NUM_RAYS = 300                                  # amount of rays
MAX_DEPTH = 800                                 # drawing distance
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = DIST * TILE_SIZE
SCALE = WIDTH // NUM_RAYS                       # scaling coef

#TEXTTURE SETTINGS
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
TEXTURE_SCALE = TEXTURE_WIDTH // TILE_SIZE

# COLORS
@dataclass
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 0, 0)
    GREEN = (0, 80, 0)
    BLUE = (0, 0, 255)
    DARKGREY = (40, 40, 40)
    PURPLE = (120, 0, 120)
    SKYBLUE = (0, 186, 255)
    YELLOW = (220, 220, 0)
    SANDY = (244, 164, 96)
