import pygame
import math

import settings
from settings import Colors
from ray_casting import ray_casting
from map import mini_world_map


class Drawing:
    def __init__(self, screen, minimap_surface):
        self.screen = screen
        self.minimap_surface = minimap_surface
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {
            1: pygame.image.load('img/wall3.png').convert(),
            2: pygame.image.load('img/wall4.png').convert(),
            3: pygame.image.load('img/wall5.png').convert(),
            4: pygame.image.load('img/wall6.png').convert(),
            'SKY': pygame.image.load('img/sky1.png').convert(),
        }

    def draw_background(self, angle):
        sky_offset = -10 * math.degrees(angle) % settings.WIDTH
        self.screen.blit(self.textures['SKY'], (sky_offset, 0))
        self.screen.blit(self.textures['SKY'], (sky_offset - settings.WIDTH, 0))
        self.screen.blit(self.textures['SKY'], (sky_offset + settings.WIDTH, 0))
        pygame.draw.rect(self.screen, Colors.DARKGREY, (0, settings.HALF_HEIGHT, settings.WIDTH, settings.HALF_HEIGHT))
    
    def draw_world(self, world_objects):
        for object in sorted(world_objects, key=lambda x: x[0], reverse=True):
            if object[0]:
                _, object, object_pos = object
                self.screen.blit(object, object_pos)


    def draw_fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        rendered_text = self.font.render(display_fps, 0, Colors.DARKORANGE)
        self.screen.blit(rendered_text, settings.FPS_POS)

    def draw_minimap(self, player):
        self.minimap_surface.fill(Colors.BLACK)

        map_x, map_y = (value // settings.MAP_SCALE for value in player.pos)

        pygame.draw.line(
            self.minimap_surface,
            Colors.YELLOW,
            (map_x, map_y),
            (map_x + 12 * math.cos(player.angle),
            map_y + 12 * math.sin(player.angle)),
            2
        )
        pygame.draw.circle(self.minimap_surface, Colors.RED, (map_x, map_y), 5)

        # DRAW MAP
        for x, y in mini_world_map:
            pygame.draw.rect(self.minimap_surface, Colors.DARKBROWN, (x, y, settings.MAP_TILE_SIZE, settings.MAP_TILE_SIZE))

        self.screen.blit(self.minimap_surface, settings.MAP_POS)
