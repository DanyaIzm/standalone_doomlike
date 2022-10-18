import pygame
import math

import settings


class Player:
    def __init__(self):
        self.x, self.y = settings.PLAYER_START_POS
        self.angle = settings.PLAYER_START_ANGLE

    @property
    def pos(self):
        return (int(self.x), int(self.y))
    
    def movement(self):
        angle_sin = math.sin(self.angle)
        angle_cos = math.cos(self.angle)
        
        keys = pygame.key.get_pressed()

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

