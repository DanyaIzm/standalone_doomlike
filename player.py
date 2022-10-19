import pygame
import math

import settings


class Player:
    def __init__(self):
        self.x, self.y = settings.PLAYER_START_POS
        self.angle = settings.PLAYER_START_ANGLE
        self.sensitivity = 0.004

    @property
    def pos(self):
        return (int(self.x), int(self.y))

    def move(self):
        self._control_keys()
        self._control_mouse()
        self.angle %= settings.DOUBLE_PI

    
    def _control_keys(self):
        angle_sin = math.sin(self.angle)
        angle_cos = math.cos(self.angle)
        
        keys = pygame.key.get_pressed()

        # TODO: refactor this
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            self.x += settings.PLAYER_NORMAL_SPEED * angle_cos
            self.y += settings.PLAYER_NORMAL_SPEED * angle_sin

        if keys[pygame.K_s]:
            self.x -= settings.PLAYER_NORMAL_SPEED * angle_cos
            self.y -= settings.PLAYER_NORMAL_SPEED * angle_sin

        if keys[pygame.K_a]:
            self.x += settings.PLAYER_NORMAL_SPEED * angle_sin
            self.y -= settings.PLAYER_NORMAL_SPEED * angle_cos

        if keys[pygame.K_d]:
            self.x -= settings.PLAYER_NORMAL_SPEED * angle_sin
            self.y += settings.PLAYER_NORMAL_SPEED * angle_cos

        if keys[pygame.K_LEFT]:
            self.angle -= 0.02

        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
    
    def _control_mouse(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - settings.HALF_WIDTH
            pygame.mouse.set_pos((settings.HALF_WIDTH, settings.HALF_HEIGHT))
            self.angle += difference * self.sensitivity

