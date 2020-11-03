
import random

import pygame

from settings import *

vec = pygame.math.Vector2


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_walls(sprite, group, direction: str):
    '''
    Checks for collision of a sprite and a group of sprites
    '''
    if direction == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if direction == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x: int, y: int):
        '''
        Main player properties, takes our game class, position
        '''
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # Define player's image, rectangle and his rect_center
        self.image = self.game.player_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # self.hit_rect = PLAYER_HIT_RECT
        # self.hit_rect.center = self.rect.center

        # Player move properties
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        # Rotation property
        self.rot = 0
        self.health = PLAYER_HEALTH

    def get_keys(self):
        '''
        Get the keys pressed and set the player movement properties to appropriate
        '''
        self.rot_speed = 0
        # We need vel to be constantly updated
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()
        # Set the rotation speed or just the player speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)


    def update(self):
        '''
        Same update as in the game loop
        '''
        self.get_keys()

        # The image has to be set
        self.image = self.game.player_image
        # Constantly get the image rectangle and apply the position
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # Get the rotation degrees and player image state(This is pretty complicated)
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pygame.transform.rotate(self.image, self.rot)

        # Do the same code(Becouse we rotated)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # Apply movement
        self.pos += self.vel * self.game.dt

        # Check for collisions and apply position(for later)
        self.rect.centerx = self.pos.x
        # collide_with_walls(self, self.game.walls, 'x')
        self.rect.centery = self.pos.y
        # collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.rect.center
