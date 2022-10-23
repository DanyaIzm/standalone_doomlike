import pygame

import settings

import sprite_object
from ray_casting import ray_casting_walls

from player import Player
from drawing import Drawing
from interaction import Interaction


pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
minimap_surface = pygame.Surface(settings.MINIMAP_RESOLUTION)

clock = pygame.time.Clock()

# Set mouse pointer to invisible state
pygame.mouse.set_visible(False)

sprites = sprite_object.Sprites()
player = Player(sprites)

drawing = Drawing(screen, minimap_surface, player, clock)
interaction = Interaction(player, sprites, drawing)

interaction.play_music()


while True:
    player.move()

    drawing.draw_background(player.angle)

    walls, wall_shot = ray_casting_walls(player, drawing.textures)
    drawing.draw_world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])

    drawing.draw_minimap(player)

    drawing.draw_player_weapon([wall_shot, sprites.sprite_shot])

    interaction.interaction_objects()
    interaction.npc_aciton()
    interaction.clear_world()
    interaction.check_win()

    drawing.draw_fps(clock)

    pygame.display.flip()
    clock.tick(settings.FPS)
