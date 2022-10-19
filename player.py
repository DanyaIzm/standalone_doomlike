import pygame
import math

import settings
from map import collision_walls


class Player:
    def __init__(self, sprites):
        self.x, self.y = settings.PLAYER_START_POS
        self.sprites = sprites
        self.angle = settings.PLAYER_START_ANGLE
        self.sensitivity = 0.004

        # collision parameters
        self.side = 50
        self.rect = pygame.Rect(self.x, self.y, self.side, self.side)
        self.collision_sprites = [pygame.Rect(*x.pos, x.side, x.side)
                                  for x in sprites.list_of_objects
                                  if x.blocked]
        self.collision_list = collision_walls + self.collision_sprites


    @property
    def pos(self):
        return (int(self.x), int(self.y))

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if hit_indexes:
            delta_x, delta_y = 0, 0
            for hit_index  in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0

        # TODO: refactor this
        self.x += dx
        self.y += dy

    def move(self):
        self._control_keys()
        self._control_mouse()
        self.rect.center = self.x, self.y
        self.angle %= settings.DOUBLE_PI

    
    def _control_keys(self):
        angle_sin = math.sin(self.angle)
        angle_cos = math.cos(self.angle)
        
        keys = pygame.key.get_pressed()

        # TODO: refactor this
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            dx = settings.PLAYER_NORMAL_SPEED * angle_cos
            dy = settings.PLAYER_NORMAL_SPEED * angle_sin
            self.detect_collision(dx, dy)

        if keys[pygame.K_s]:
            dx = -settings.PLAYER_NORMAL_SPEED * angle_cos
            dy = -settings.PLAYER_NORMAL_SPEED * angle_sin
            self.detect_collision(dx, dy)

        if keys[pygame.K_a]:
            dx = settings.PLAYER_NORMAL_SPEED * angle_sin
            dy = -settings.PLAYER_NORMAL_SPEED * angle_cos
            self.detect_collision(dx, dy)

        if keys[pygame.K_d]:
            dx = -settings.PLAYER_NORMAL_SPEED * angle_sin
            dy = settings.PLAYER_NORMAL_SPEED * angle_cos
            self.detect_collision(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= 0.02

        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
    
    def _control_mouse(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - settings.HALF_WIDTH
            pygame.mouse.set_pos((settings.HALF_WIDTH, settings.HALF_HEIGHT))
            self.angle += difference * self.sensitivity

