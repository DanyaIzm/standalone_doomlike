import pygame
import math

import settings
from map import world_map


def _mapping(a, b):
    return (a // settings.TILE_SIZE) * settings.TILE_SIZE, (b // settings.TILE_SIZE) * settings.TILE_SIZE


def ray_casting(screen, player_pos, player_angle, textures):
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
            yv = yo + depth_v * angle_sin
            tile_v = _mapping(x + dx, yv)

            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * settings.TILE_SIZE

        # HORIZONTALS
        y, dy = (ym + settings.TILE_SIZE, 1) if angle_sin >= 0 else (ym, -1)

        for i in range(0, settings.HEIGHT, settings.TILE_SIZE):
            depth_h = (y - yo) / angle_sin
            xh = xo + depth_h * angle_cos
            tile_h = _mapping(xh, y + dy)

            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * settings.TILE_SIZE
        
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % settings.TILE_SIZE
        depth *= math.cos(player_angle - current_angle)
        depth = max(depth, 0.00001)

        proj_height = min(int(settings.PROJ_COEFF / depth), settings.HEIGHT * 2)
        
        wall_column = textures[texture].subsurface(offset * settings.TEXTURE_SCALE, 0, settings.TEXTURE_SCALE, settings.TEXTURE_HEIGHT)
        wall_column = pygame.transform.scale(wall_column, (settings.SCALE, proj_height))
        screen.blit(wall_column, (ray * settings.SCALE, settings.HALF_HEIGHT - proj_height // 2))

        current_angle += settings.DELTA_ANGLE
