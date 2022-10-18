import pygame
import math

import settings
from settings import Colors

from player import Player
from map import world_map
from ray_casting import ray_casting


pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()

player = Player()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    player.movement()

    screen.fill(Colors.BLACK)

    pygame.draw.rect(screen, Colors.BLUE, (0, 0, settings.WIDTH, settings.HALF_HEIGHT))
    pygame.draw.rect(screen, Colors.DARKGREY, (0, settings.HALF_HEIGHT, settings.WIDTH, settings.HALF_HEIGHT))

    ray_casting(screen, player.pos, player.angle)

    # # DRAW PLAYER
    # pygame.draw.circle(screen, Colors.GREEN, player.pos, 20)
    # pygame.draw.line(
    #     screen,
    #     Colors.GREEN,
    #     player.pos,
    #     (player.x + settings.WIDTH * math.cos(player.angle),
    #      player.y + settings.HEIGHT * math.sin(player.angle))
    # )

    # # DRAW MAP
    # for x, y in world_map:
    #     pygame.draw.rect(screen, Colors.DARKGREY, (x, y, settings.TILE_SIZE, settings.TILE_SIZE), 2)

    pygame.display.flip()
    clock.tick(settings.FPS)
