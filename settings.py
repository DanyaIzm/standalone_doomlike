""" GAME SETTINGS FILE """
import math
from dataclasses import dataclass

# SCREEN
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

# TIME
FPS = 60

# PLAYER SETTINGS
PLAYER_START_POS = (HALF_WIDTH, HALF_HEIGHT)
PLAYER_START_ANGLE = 0
PLAYER_NORMAL_SPEED = 2

# MAP SETTINGS
TILE_SIZE = 100

# RAY CASTINGS SETTINGS
FOV = math.pi / 3                               # field of view
HALF_FOV = FOV / 2
NUM_RAYS = 120                                  # amount of rays
MAX_DEPTH = 800                                 # drawing distance
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE_SIZE
SCALE = WIDTH // NUM_RAYS                       # scaling coef

# COLORS
@dataclass
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 0, 0)
    GREEN = (0, 220, 0)
    BLUE = (0, 0, 255)
    DARKGREY = (40, 40, 40)
    PURPLE = (120, 0, 120)
