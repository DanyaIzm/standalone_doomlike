import pygame
import math

import settings
from settings import Colors

import sprite_object
from ray_casting import ray_casting

from player import Player
from drawing import Drawing


pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
minimap_surface = pygame.Surface(settings.MINIMAP_RESOLUTION)

clock = pygame.time.Clock()

# Set mouse pointer to invisible state
pygame.mouse.set_visible(False)

drawing = Drawing(screen, minimap_surface)

sprites = sprite_object.Sprites()
player = Player(sprites)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    player.move()

    screen.fill(Colors.BLACK)

    drawing.draw_background(player.angle)

    walls = ray_casting(player, drawing.textures)
    drawing.draw_world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])

    drawing.draw_minimap(player)
    drawing.draw_fps(clock)

    pygame.display.flip()
    clock.tick(settings.FPS)
