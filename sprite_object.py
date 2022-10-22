import pygame
import math
from collections import deque

import settings


class Sprites:
    def __init__(self):
        self.sprite_params = {
            'sprite_barrel': {
                'sprite': pygame.image.load('sprites/barrel/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': 0.4,
                'animation': deque([pygame.image.load(f'sprites/barrel/anim/{i}.png').convert_alpha() for i in range(12)]),
                'animation_distance': 800, 
                'animation_speed': 10,
                'blocked': True,
            },
            'sprite_pin': {
                'sprite': pygame.image.load('sprites/pin/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.6,
                'scale': 0.6,
                'animation': deque([pygame.image.load(f'sprites/pin/anim/{i}.png').convert_alpha() for i in range(8)]),
                'animation_distance': 800,
                'animation_speed': 10,
                'blocked': True,
            },
            'sprite_devil': {
                'sprite': [pygame.image.load(f'sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': -0.2,
                'scale': 1.1,
                'animation': deque(
                    [pygame.image.load(f'sprites/devil/anim/{i}.png').convert_alpha() for i in range(9)]),
                'animation_distance': 150,
                'animation_speed': 10,
                'blocked': True,
            },
            'sprite_flame': {
                'sprite': pygame.image.load('sprites/flame/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.7,
                'scale': 0.6,
                'animation': deque(
                    [pygame.image.load(f'sprites/flame/anim/{i}.png').convert_alpha() for i in range(16)]),
                'animation_distance': 800,
                'animation_speed': 5,
                'blocked': False,
            },
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_params['sprite_barrel'], (7.1, 2.1)),
            SpriteObject(self.sprite_params['sprite_barrel'], (5.9, 2.1)),
            SpriteObject(self.sprite_params['sprite_pin'], (8.7, 2.5)),
            SpriteObject(self.sprite_params['sprite_devil'], (7, 4)),
            SpriteObject(self.sprite_params['sprite_flame'], (8.6, 5.6)),
        ]
    
    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.list_of_objects], default=(float('inf'), 0))


class SpriteObject:
    def __init__(self, parameters, pos):
        self.sprite = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation']
        self.animation_distance = parameters['animation_distance']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.side = 30
        self.animation_count = 0
        self.x, self.y = pos[0] * settings.TILE_SIZE, pos[1] * settings.TILE_SIZE

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.sprite)}
    
    @property
    def is_on_fire(self):
        if settings.CENTRAL_RAY - self.side // 2 < self.current_ray < settings.CENTRAL_RAY + self.side // 2 and self.blocked:
            return self.distance_to_sprite, self.proj_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2


    def object_locate(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta_angle = math.atan2(dy, dx)
        gamma_angle = self.theta_angle - player.angle

        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma_angle += settings.DOUBLE_PI
          
        delta_rays = int(gamma_angle / settings.DELTA_ANGLE)
        self.current_ray = settings.CENTRAL_RAY + delta_rays
        self.distance_to_sprite *= math.cos(settings.HALF_FOV - self.current_ray * settings.DELTA_ANGLE)

        fake_ray = self.current_ray + settings.FAKE_RAYS
        if 0 <= fake_ray <= settings.FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
            self.proj_height = min(int(settings.PROJ_COEFF / self.distance_to_sprite * self.scale), settings.DOUBLE_HEIGHT)
            half_proj_height = self.proj_height // 2
            shift = half_proj_height * self.shift

            # change sprite relative to the player angle
            if self.viewing_angles:
                if self.theta_angle < 0:
                    self.theta_angle += settings.DOUBLE_PI
                self.theta_angle = 360 - int(math.degrees(self.theta_angle))

                for angles in self.sprite_angles:
                    if self.theta_angle in angles:
                        self.sprite = self.sprite_positions[angles]
                        break

            # animate sprite
            sprite_object = self.sprite
            if self.animation and self.distance_to_sprite < self.animation_distance:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0
            
            # scale and position sprite
            sprite_pos = (self.current_ray * settings.SCALE - half_proj_height, settings.HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_object, (self.proj_height, self.proj_height))
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
