import pygame
import math
import sys
from collections import deque
from random import randrange

import settings
from settings import Colors
from ray_casting import ray_casting
from map import mini_world_map


class Drawing:
    def __init__(self, screen, minimap_surface, player, clock):
        self.screen = screen
        self.minimap_surface = minimap_surface
        self.player = player

        self.clock = clock

        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_win = pygame.font.Font('font/font.ttf', 144, bold=True)

        self.textures = {
            1: pygame.image.load('img/wall3.png').convert(),
            2: pygame.image.load('img/wall4.png').convert(),
            3: pygame.image.load('img/wall5.png').convert(),
            4: pygame.image.load('img/wall6.png').convert(),
            'SKY': pygame.image.load('img/sky1.png').convert(),
        }

        # menu 
        self.menu_trigger = True
        self.menu_picture = pygame.image.load('img/bg.jpg').convert()

        # weapon parameters
        self.weapon_base_sprite = pygame.image.load('sprites/weapons/shotgun/base/0.png').convert_alpha()
        self.weapon_shot_animation = deque([pygame.image.load(f'sprites/weapons/shotgun/shot/{i}.png').convert_alpha()
                                            for i in range(20)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (settings.HALF_WIDTH - self.weapon_rect.width // 2, settings.HEIGHT - self.weapon_rect.height)
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 3
        self.shot_animation_count = 0
        self.shot_animation_trigger = True
        self.shot_sound = pygame.mixer.Sound('sound/shotgun.wav')

        # sfx parameters
        self.sfx = deque([pygame.image.load(f'sprites/weapons/sfx/{i}.png').convert_alpha() for i in range(9)])
        self.sfx_length = len(self.sfx)
        self.sfx_length_count = 0

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

    def draw_player_weapon(self, shots):
        if self.player.shot:
            if not self.shot_animation_count and not self.shot_length_count:
                self.shot_sound.play()
            self.shot_projection = min(shots)[1] // 2
            self.draw_bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.screen.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_animation_trigger = False
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_animation_trigger = True
        else:
            self.screen.blit(self.weapon_base_sprite, self.weapon_pos)
    
    def draw_bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.screen.blit(sfx, (settings.HALF_WIDTH - sfx_rect.width // 2, settings.HALF_HEIGHT - sfx_rect.height // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)


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

    def draw_win(self):
        win_text = self.font_win.render('YOU WIN!!!', 1, (randrange(40, 120), 0, 0))
        rect = pygame.Rect(0, 0, 1000, 300)
        rect.center = settings.HALF_WIDTH, settings.HALF_HEIGHT
        pygame.draw.rect(self.screen, Colors.BLACK, rect, border_radius=50)
        self.screen.blit(win_text, (rect.centerx - 430, rect.centery - 140))
        pygame.display.flip()
        self.clock.tick(15)

    def draw_menu(self):
        x = 0
        button_font = pygame.font.Font('font/font.ttf', 72)
        label_font = pygame.font.Font('font/font1.otf', 400)
        start = button_font.render('START', True, pygame.Color('lightgray'))
        button_start= pygame.Rect(0, 0, 400, 150)
        button_start.center = settings.HALF_WIDTH, settings.HALF_HEIGHT
        exit = button_font.render('EXIT ', True, pygame.Color('lightgray'))
        button_exit= pygame.Rect(0, 0, 400, 150)
        button_exit.center = settings.HALF_WIDTH, settings.HALF_HEIGHT + 200

        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.blit(self.menu_picture, (0, 0), (x % settings.WIDTH, settings.HALF_HEIGHT, settings.WIDTH, settings.HEIGHT))
            x += 1

            pygame.draw.rect(self.screen, Colors.BLACK, button_start, border_radius=25, width=10)
            self.screen.blit(start, (button_start.centerx - 130, button_start.centery - 70))

            pygame.draw.rect(self.screen, Colors.BLACK, button_exit, border_radius=25, width=10)
            self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

            color = randrange(40)
            label = label_font.render('DOOM', True, (color, color, color))
            self.screen.blit(label, (settings.HALF_WIDTH - label.get_rect().width // 2, -30))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, Colors.BLACK, button_start, border_radius=25)
                self.screen.blit(start, (button_start.centerx - 130, button_start.centery - 70))
                if mouse_click[0]:
                    self.menu_trigger = False
            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, Colors.BLACK, button_exit, border_radius=25)
                self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)
