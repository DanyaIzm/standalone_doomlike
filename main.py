import pygame
import math

import settings
from settings import Colors

from player import Player
from drawing import Drawing


pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
minimap_surface = pygame.Surface((settings.WIDTH // settings.MAP_SCALE, settings.HEIGHT // settings.MAP_SCALE))

clock = pygame.time.Clock()

drawing = Drawing(screen, minimap_surface)

player = Player()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    player.movement()

    screen.fill(Colors.BLACK)

    drawing.draw_background(player.angle)
    drawing.draw_world(player.pos, player.angle)
    drawing.draw_minimap(player)
    drawing.draw_fps(clock)

    pygame.display.flip()
    clock.tick(settings.FPS)
