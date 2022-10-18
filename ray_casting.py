import pygame
import math

import settings
from settings import Colors
from map import world_map


def ray_casting(screen, player_pos, player_angle):
    current_angle = player_angle - settings.HALF_FOV
    xo, yo = player_pos

    for ray in range(settings.NUM_RAYS):
        angle_sin = math.sin(current_angle)
        angle_cos = math.cos(current_angle)

        for depth in range(settings.MAX_DEPTH):
            x = xo + depth * angle_cos
            y = yo + depth * angle_sin

            if (x // settings.TILE_SIZE * settings.TILE_SIZE, y // settings.TILE_SIZE * settings.TILE_SIZE) in world_map:
                depth *= math.cos(player_angle - current_angle)
                proj_height = settings.PROJ_COEFF / depth
                color_depth = 255 / (1 + depth * depth * 0.0001)
                color = (color_depth, color_depth, color_depth)
                pygame.draw.rect(screen, color, (ray * settings.SCALE, settings.HALF_HEIGHT - proj_height // 2, settings.SCALE, proj_height))
                break 

        current_angle += settings.DELTA_ANGLE
