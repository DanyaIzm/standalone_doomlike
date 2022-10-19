import settings

text_map = [
    '111111111111',
    '1.....2....1',
    '1.22.....2.1',
    '1..........1',
    '1.22.......1',
    '1.2......2.1',
    '1.....2....1',
    '111111111111',
]

world_map = {}
mini_world_map = set()

for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            mini_world_map.add((i * settings.MAP_TILE_SIZE, j * settings.MAP_TILE_SIZE))
            world_map[(i * settings.TILE_SIZE, j * settings.TILE_SIZE)] = char
