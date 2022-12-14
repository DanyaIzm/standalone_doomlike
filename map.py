import pygame
from numba.core import types
from numba.typed.typeddict import Dict
from numba import int32

import settings

_ = False

matrix_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, 4, _, _, _, _, _, 1],
    [1, _, 2, 2, _, _, _, _, _, 2, 2, 2, _, _, _, 3, _, _, _, _, 4, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, 2, 2, _, _, _, 3, _, _, _, _, _, _, 1],
    [1, _, 2, 2, _, _, _, _, _, _, _, _, 2, _, 4, _, _, 3, _, _, _, 4, _, 1],
    [1, _, _, _, _, _, 4, _, _, 2, 2, _, 2, _, _, _, _, _, _, 4, _, _, _, 1],
    [1, _, 3, _, _, _, 2, _, _, 2, _, _, 2, _, _, _, 4, _, _, _, _, 4, _, 1],
    [1, _, _, 3, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 3, _, _, _, _, _, _, _, 3, _, _, 3, 3, _, _, _, _, 3, 3, _, _, 1],
    [1, _, 3, _, _, _, 3, 3, _, 3, _, _, _, 3, 3, _, _, _, _, 2, 3, _, _, 1],
    [1, _, _, _, _, 3, _, 3, _, _, 3, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 4, _, 3, _, _, _, _, 3, _, _, 2, _, _, _, _, _, _, _, _, 2, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, 2, _, _, _, _, _, _, 2, 2, _, 1],
    [1, _, _, 4, _, _, _, _, 4, _, _, _, _, 2, 2, 2, 2, 2, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, 4, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

WORLD_WIDTH = len(matrix_map[0]) * settings.TILE_SIZE
WORLD_HEIGHT = len(matrix_map) * settings.TILE_SIZE

world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
mini_world_map = set()

collision_walls = []

for j, row in enumerate(matrix_map):
    for i, tile_type in enumerate(row):
        if tile_type:
            collision_walls.append(
                pygame.Rect(i * settings.TILE_SIZE, j * settings.TILE_SIZE, settings.TILE_SIZE, settings.TILE_SIZE)
            )
            mini_world_map.add((i * settings.MAP_TILE_SIZE, j * settings.MAP_TILE_SIZE))
            world_map[(i * settings.TILE_SIZE, j * settings.TILE_SIZE)] = tile_type
