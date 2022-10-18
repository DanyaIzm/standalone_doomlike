import settings

text_map = [
    '111112211111',
    '1..........1',
    '1..11......1',
    '1......222.1',
    '1.......2..1',
    '1.......2..2',
    '1.......2..2',
    '222221122222',
]

world_map = {}
mini_world_map = set()

for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            mini_world_map.add((i * settings.MAP_TILE_SIZE, j * settings.MAP_TILE_SIZE))
            world_map[(i * settings.TILE_SIZE, j * settings.TILE_SIZE)] = char
