import pygame
import math
from numba import njit

import settings
from map import world_map
from ray_casting import _mapping


@njit(fastmath=True, cache=True)
def ray_casting_npc_to_player(npc_x, npc_y, blocked_doors, world_map, player_pos):
    xo, yo = player_pos
    xm, ym = _mapping(xo, yo)
    delta_x, delta_y = xo - npc_x, yo - npc_y
    current_angle = math.atan2(delta_y, delta_x) + math.pi

    angle_sin = math.sin(current_angle)
    angle_sin = angle_sin if angle_sin else 0.000001
    angle_cos = math.cos(current_angle)
    angle_cos = angle_cos if angle_cos else 0.000001

    # VERTICALS
    x, dx = (xm + settings.TILE_SIZE, 1) if angle_cos >= 0 else (xm, -1)

    for _ in range(0, int(abs(delta_x)), settings.TILE_SIZE):
        depth_v = (x - xo) / angle_cos
        yv = yo + depth_v * angle_sin
        tile_v = _mapping(x + dx, yv)

        if tile_v in world_map or tile_v in blocked_doors:
            return False
        x += dx * settings.TILE_SIZE

    # HORIZONTALS
    y, dy = (ym + settings.TILE_SIZE, 1) if angle_sin >= 0 else (ym, -1)

    for _ in range(0, int(abs(delta_y)), settings.TILE_SIZE):
        depth_h = (y - yo) / angle_sin
        xh = xo + depth_h * angle_cos
        tile_h = _mapping(xh, y + dy)

        if tile_h in world_map or tile_h in blocked_doors:
            return False
        y += dy * settings.TILE_SIZE
    
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.pain_sound = pygame.mixer.Sound('sound/pain.wav')
    
    def interaction_objects(self):
        if self.player.shot and self.drawing.shot_animation_trigger:
            for object in sorted(self.sprites.list_of_objects, key=lambda object: object.distance_to_sprite):
                if object.is_on_fire[1]:
                    if object.is_dead != 'immortal' and not object.is_dead:
                        if ray_casting_npc_to_player(object.x, object.y, self.sprites.blocked_doors, world_map, self.player.pos):
                            if object.flag == 'npc':
                                self.pain_sound.play()
                            object.is_dead = True
                            object.blocked = None
                    if object.flag in {'door_h', 'door_v'} and object.distance_to_sprite < settings.TILE_SIZE:
                        object.door_open_trigger = True
                        object.blocked = None
                    break
    
    def npc_aciton(self):
        for object in self.sprites.list_of_objects:
            if object.flag == 'npc' and not object.is_dead:
                if ray_casting_npc_to_player(object.x, object.y, self.sprites.blocked_doors, world_map, self.player.pos):
                    object.npc_action_trigger = True
                    self.move_npc(object)
                else:
                    object.npc_action_trigger = False

    def move_npc(self, object):
        if object.distance_to_sprite > settings.TILE_SIZE:
            dx = object.x - self.player.pos[0]
            dy = object.y - self.player.pos[1]
            object.x = object.x + 1 if dx < 0 else object.x - 1
            object.y = object.y + 1 if dy < 0 else object.y - 1
    
    def clear_world(self):
        deleted_objects = self.sprites.list_of_objects[:]
        [self.sprites.list_of_objects.remove(object) for object in deleted_objects if object.deleted]

    def play_music(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('sound/theme.mp3')
        pygame.mixer.music.play(10)
    
    def check_win(self):
        if not len([object for object in self.sprites.list_of_objects if object.flag == 'npc' and not object.is_dead]):
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sound/win.mp3')
            pygame.mixer.music.play()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                self.drawing.draw_win()
