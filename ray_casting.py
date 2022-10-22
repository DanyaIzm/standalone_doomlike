import pygame
import math
from numba import njit

import settings
from map import world_map, WORLD_WIDTH, WORLD_HEIGHT


@njit(fastmath=True)
def _mapping(a, b):
    return (a // settings.TILE_SIZE) * settings.TILE_SIZE, (b // settings.TILE_SIZE) * settings.TILE_SIZE


@njit(fastmath=True)
def ray_casting(player_pos, player_angle, world_map):
    casted_walls = []
    texture_v, texture_h = 1, 1
    xo, yo = player_pos
    xm, ym = _mapping(xo, yo)
    current_angle = player_angle - settings.HALF_FOV

    for ray in range(settings.NUM_RAYS):
        angle_sin = math.sin(current_angle)
        angle_cos = math.cos(current_angle)

        # VERTICALS
        x, dx = (xm + settings.TILE_SIZE, 1) if angle_cos >= 0 else (xm, -1)

        for _ in range(0, WORLD_WIDTH, settings.TILE_SIZE):
            depth_v = (x - xo) / angle_cos
            yv = yo + depth_v * angle_sin
            tile_v = _mapping(x + dx, yv)

            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * settings.TILE_SIZE

        # HORIZONTALS
        y, dy = (ym + settings.TILE_SIZE, 1) if angle_sin >= 0 else (ym, -1)

        for _ in range(0, WORLD_HEIGHT, settings.TILE_SIZE):
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

        proj_height = int(settings.PROJ_COEFF / depth)

        casted_walls.append((depth, offset, proj_height, texture))
        current_angle += settings.DELTA_ANGLE
    
    return casted_walls


def ray_casting_walls(player, textures):
    casted_walls = ray_casting(player.pos, player.angle, world_map)
    walls = []

    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values

        if proj_height > settings.HEIGHT:
            coeff = proj_height / settings.HEIGHT
            texture_height = settings.TEXTURE_HEIGHT / coeff
            wall_column = textures[texture].subsurface(offset * settings.TEXTURE_SCALE,
                                                       settings.HALF_TEXTURE_HEIGHT - texture_height // 2,
                                                       settings.TEXTURE_SCALE, texture_height)
            wall_column = pygame.transform.scale(wall_column, (settings.SCALE, settings.HEIGHT))
            wall_pos = (ray * settings.SCALE, 0)
        else:
            wall_column = textures[texture].subsurface(offset * settings.TEXTURE_SCALE, 0, settings.TEXTURE_SCALE, settings.TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column, (settings.SCALE, proj_height))
            wall_pos = (ray * settings.SCALE, settings.HALF_HEIGHT - proj_height // 2)
        walls.append((depth, wall_column, wall_pos))
    
    return walls
