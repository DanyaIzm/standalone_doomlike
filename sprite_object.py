import pygame
import math

import settings


class Sprites:
    def __init__(self):
        self.sprite_types = {
            'barrel': pygame.image.load('sprites/barrel/0.png').convert_alpha(),
            'pedestal': pygame.image.load('sprites/pedestal/0.png').convert_alpha(),
            'devil': [pygame.image.load(f'sprites/devil/{i}.png').convert_alpha() for i in range(8)],
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_types['barrel'], True, (7.1, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['barrel'], True, (5.9, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['pedestal'], True, (8.8, 2.5), 1.8, 0.4),
            SpriteObject(self.sprite_types['pedestal'], True, (8.8, 5.6), 1.6, 0.5),
            SpriteObject(self.sprite_types['devil'], False, (7, 4), -0.2, 0.7),
        ]


class SpriteObject:
    def __init__(self, object, is_static, pos, shift, scale):
        self.object = object
        self.is_static = is_static
        self.pos = self.x, self.y = pos[0] * settings.TILE_SIZE, pos[1] * settings.TILE_SIZE
        self.shift = shift
        self.scale = scale

        if not is_static:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}
    
    def object_locate(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta_angle = math.atan2(dy, dx)
        gamma_angle = theta_angle - player.angle

        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma_angle += settings.DOUBLE_PI
        
        delta_rays = int(gamma_angle / settings.DELTA_ANGLE)
        current_ray = settings.CENTRAL_RAY + delta_rays
        distance_to_sprite *= math.cos(settings.HALF_FOV - current_ray * settings.DELTA_ANGLE)

        fake_ray = current_ray + settings.FAKE_RAYS
        if 0 <= fake_ray <= settings.FAKE_RAYS_RANGE and distance_to_sprite > 30:
            proj_height = min(int(settings.PROJ_COEFF / distance_to_sprite * self.scale), settings.DOUBLE_HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height + self.shift

            if not self.is_static:
                if theta_angle < 0:
                    theta_angle += settings.DOUBLE_PI
                theta_angle = 360 - int(math.degrees(theta_angle))

                for angles in self.sprite_angles:
                    if theta_angle in angles:
                        self.object = self.sprite_positions[angles]
                        break

            sprite_pos = (current_ray * settings.SCALE - half_proj_height, settings.HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
