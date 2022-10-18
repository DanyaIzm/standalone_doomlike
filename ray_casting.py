import pygame
import math

import settings
from map import world_map


def _mapping(a, b):
    return (a // settings.TILE_SIZE) * settings.TILE_SIZE, (b // settings.TILE_SIZE) * settings.TILE_SIZE


def ray_casting(screen, player_pos, player_angle):
    xo, yo = player_pos
    xm, ym = _mapping(xo, yo)
    current_angle = player_angle - settings.HALF_FOV

    for ray in range(settings.NUM_RAYS):
        angle_sin = math.sin(current_angle)
        angle_cos = math.cos(current_angle)

        # VERTICALS
        x, dx = (xm + settings.TILE_SIZE, 1) if angle_cos >= 0 else (xm, -1)

        for i in range(0, settings.WIDTH, settings.TILE_SIZE):
            depth_v = (x - xo) / angle_cos
            y = yo + depth_v * angle_sin

            if _mapping(x + dx, y) in world_map:
                break
            x += dx * settings.TILE_SIZE

        # HORIZONTALS
        y, dy = (ym + settings.TILE_SIZE, 1) if angle_sin >= 0 else (ym, -1)

        for i in range(0, settings.HEIGHT, settings.TILE_SIZE):
            depth_h = (y - yo) / angle_sin
            x = xo + depth_h * angle_cos

            if _mapping(x, y + dy) in world_map:
                break
            y += dy * settings.TILE_SIZE
        
        depth = depth_v if depth_v < depth_h else depth_h
        depth *= math.cos(player_angle - current_angle)

        proj_height = settings.PROJ_COEFF / depth
        color_depth = 255 / (1 + depth * depth * 0.00002)
        color = (color_depth, color_depth // 2, color_depth // 3)
        pygame.draw.rect(screen, color, (ray * settings.SCALE, settings.HALF_HEIGHT - proj_height // 2, settings.SCALE, proj_height))
        current_angle += settings.DELTA_ANGLE
