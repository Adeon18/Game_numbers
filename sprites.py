
import random
import pytweening
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
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_image
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
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
        if self.health > 10:
            self.health = 10
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pygame.transform.rotate(self.game.player_image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x: int, y: int):
        '''
        Main player properties, takes our game class, position
        '''
        self._layer = BOX_LAYER
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.wall_image
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Key(pygame.sprite.Sprite):
    def __init__(self, game, x: int, y: int):
        '''
        Main player properties, takes our game class, position
        '''
        self._layer = BOX_LAYER
        self.groups = game.all_sprites, game.keys_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.key_image
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.pos = (self.rect.x, self.rect.y)

        # self.tween = pytweening.easeInOutSine
        # self.dir = 1
        # self.step = 0

    # def update(self):
    #     # Bobbing motion
    #     offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
    #     self.rect.top = self.pos[0] + offset * self.dir
    #     self.step += BOB_SPEED
    #     if self.step > BOB_RANGE:
    #         self.step = 0
    #         self.dir *= -1


class Chest(pygame.sprite.Sprite):
    def __init__(self, game, x: int, y: int):
        '''
        Main player properties, takes our game class, position
        '''
        self._layer = BOX_LAYER
        self.groups = game.all_sprites, game.eggs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.chest_image
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.pos = (self.rect.x, self.rect.y)

