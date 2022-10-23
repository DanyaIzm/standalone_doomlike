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
                'scale': (0.4, 0.4),
                'side': 30,
                'animation': deque(
                    [pygame.image.load(f'sprites/barrel/anim/{i}.png').convert_alpha() for i in range(12)]),
                'death_animation': deque([pygame.image.load(f'sprites/barrel/death/{i}.png')
                                          .convert_alpha() for i in range(4)]),
                'is_dead': None,
                'dead_shift': 2.6,
                'animation_distance': 800,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'decor',
                'obj_action': []
            },
            'sprite_pin': {
                'sprite': pygame.image.load('sprites/pin/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.6,
                'scale': (0.6, 0.6),
                'side': 30,
                'animation': deque([pygame.image.load(f'sprites/pin/anim/{i}.png').convert_alpha() for i in range(8)]),
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': None,
                'animation_distance': 800,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'decor',
                'obj_action': []
            },
            'sprite_flame': {
                'sprite': pygame.image.load('sprites/flame/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.7,
                'scale': (0.6, 0.6),
                'side': 30,
                'animation': deque(
                    [pygame.image.load(f'sprites/flame/anim/{i}.png').convert_alpha() for i in range(16)]),
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 1.8,
                'animation_distance': 1800,
                'animation_speed': 5,
                'blocked': None,
                'flag': 'decor',
                'obj_action': []
            },
            'npc_devil': {
                'sprite': [pygame.image.load(f'sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.0,
                'scale': (1.1, 1.1),
                'side': 50,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/devil/death/{i}.png')
                                           .convert_alpha() for i in range(6)]),
                'is_dead': None,
                'dead_shift': 0.6,
                'animation_distance': None,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque(
                    [pygame.image.load(f'sprites/devil/anim/{i}.png').convert_alpha() for i in range(9)]),
            },
            'sprite_door_v': {
                'sprite': [pygame.image.load(f'sprites/doors/door_v/{i}.png').convert_alpha() for i in range(16)],
                'viewing_angles': True,
                'shift': 0.1,
                'scale': (2.6, 1.2),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_distance': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'door_h',
                'obj_action': []
            },
            'sprite_door_h': {
                'sprite': [pygame.image.load(f'sprites/doors/door_h/{i}.png').convert_alpha() for i in range(16)],
                'viewing_angles': True,
                'shift': 0.1,
                'scale': (2.6, 1.2),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_distance': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'door_v',
                'obj_action': []
            },
            'npc_soldier0': {
                'sprite': [pygame.image.load(f'sprites/npc/soldier0/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.8,
                'scale': (0.4, 0.6),
                'side': 30,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/npc/soldier0/death/{i}.png')
                                         .convert_alpha() for i in range(10)]),
                'is_dead': None,
                'dead_shift': 1.7,
                'animation_distance': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'sprites/npc/soldier0/action/{i}.png')
                                    .convert_alpha() for i in range(4)])
            },
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_params['sprite_barrel'], (7.1, 2.1)),
            SpriteObject(self.sprite_params['sprite_barrel'], (5.9, 2.1)),
            SpriteObject(self.sprite_params['sprite_pin'], (8.7, 2.5)),
            SpriteObject(self.sprite_params['npc_devil'], (7, 4)),
            SpriteObject(self.sprite_params['sprite_flame'], (8.6, 5.6)),
        ]
    
    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.list_of_objects], default=(float('inf'), 0))


class SpriteObject:
    def __init__(self, parameters, pos):
        self.sprite = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        # ---------------------
        self.death_animation = parameters['death_animation'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']
        # ---------------------
        self.animation_distance = parameters['animation_distance']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.flag = parameters['flag']
        self.obj_action = parameters['obj_action'].copy()
        self.x, self.y = pos[0] * settings.TILE_SIZE, pos[1] * settings.TILE_SIZE
        self.side = parameters['side']
        self.death_animation_count = 0
        self.animation_count = 0
        self.npc_action_trigger = False
        self.door_open_trigger = False
        self.door_prev_pos = self.y if self.flag == 'door_h' else self.x
        self.delete = False
        if self.viewing_angles:
            if len(self.sprite) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
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

        theta_angle = math.atan2(dy, dx)
        gamma_angle = theta_angle - player.angle

        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma_angle += settings.DOUBLE_PI
        theta_angle += 1.4 * gamma_angle
          
        delta_rays = int(gamma_angle / settings.DELTA_ANGLE)
        self.current_ray = settings.CENTRAL_RAY + delta_rays
        self.distance_to_sprite *= math.cos(settings.HALF_FOV - self.current_ray * settings.DELTA_ANGLE)

        fake_ray = self.current_ray + settings.FAKE_RAYS
        if 0 <= fake_ray <= settings.FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
            self.proj_height = min(int(settings.PROJ_COEFF / self.distance_to_sprite), settings.DOUBLE_HEIGHT)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_heigth = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_heigth // 2
            shift = half_sprite_height * self.shift

            if self.is_dead and self.is_dead != 'immortal':
                sprite_object = self.play_death_animation()
                shift = half_sprite_height * self.dead_shift
                sprite_heigth = int(sprite_heigth / 1.3)
            elif self.npc_action_trigger:
                sprite_object = self.play_npc_action()
            else:
                self.sprite = self.get_visible_sprite(theta_angle)
                sprite_object = self.play_sprite_animation()
            
            # scale and position sprite
            sprite_pos = (self.current_ray * settings.SCALE - half_sprite_width, settings.HALF_HEIGHT - half_sprite_height + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_heigth))
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def play_sprite_animation(self):
        if self.animation and self.distance_to_sprite < self.animation_distance:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate()
                self.animation_count = 0
                
            return sprite_object

        return self.sprite

    def get_visible_sprite(self, theta_angle):
        if self.viewing_angles:
                if theta_angle < 0:
                    theta_angle += settings.DOUBLE_PI
                theta_angle = 360 - int(math.degrees(theta_angle))

                for angles in self.sprite_angles:
                    if theta_angle in angles:
                        return self.sprite_positions[angles]

        return self.sprite
    
    def play_death_animation(self):
        if len(self.death_animation):
            if self.death_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.death_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.death_animation_count = 0
        
        return self.dead_sprite

    def play_npc_action(self):
        sprite_object = self.obj_action[0]

        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_action.rotate()
            self.animation_count = 0
        
        return sprite_object
