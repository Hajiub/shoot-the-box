#!/usr/bin/env python3

import pygame as pg
import sys
import random
import os
from enum import Enum

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
BULLET_SIZE = 10
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 10
BULLET_DELAY = 350

# Initialize Pygame
pg.init()
pg.mixer.init()
main_dir = os.path.split(os.path.abspath(__file__))[0]

# Load Image Function
def load_image(file, scale=1):
    file = os.path.join(main_dir, "imgs", file)
    try:
        image = pg.image.load(file)
        size = (image.get_width() * scale, image.get_height() * scale)
        image = pg.transform.scale(image, size)
    except pg.error:
        raise SystemExit(f"Could not load image '{file}' {pg.get_error()}")
    return image, image.get_rect()

# Load Sound Function
def load_sound(file):
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "audio", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print(f"Warning, unable to load, {file}")
    return None

# Enum for Directions
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Bullet Class
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction: Direction):
        super().__init__()
        self.image = pg.Surface((BULLET_SIZE, BULLET_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.sound_duration = 290

    def update(self):
        if self.direction == Direction.LEFT:
            self.rect.x -= BULLET_SPEED
        elif self.direction == Direction.RIGHT:
            self.rect.x += BULLET_SPEED
        elif self.direction == Direction.UP:
            self.rect.y -= BULLET_SPEED
        elif self.direction == Direction.DOWN:
            self.rect.y += BULLET_SPEED

        if (
            self.rect.top <= 0
            or self.rect.bottom >= SCREEN_HEIGHT
            or self.rect.left < 0
            or self.rect.right > SCREEN_WIDTH
        ):
            self.kill()

# Player Class
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image, self.rect = load_image("player.png")
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.direction = Direction.RIGHT
        self.rotated_image = self.original_image
        self.rotated = Direction.RIGHT
        self.image = self.original_image  
        self.bullets = pg.sprite.Group()
        self.last_bullet_time = 0


    def update(self):
        self.move()
        self.rotate()
        self.bullets.update()

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
            self.direction = Direction.LEFT
        elif keys[pg.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
            self.direction = Direction.RIGHT
        elif keys[pg.K_UP]:
            self.rect.y -= PLAYER_SPEED
            self.direction = Direction.UP
        elif keys[pg.K_DOWN]:
            self.rect.y += PLAYER_SPEED
            self.direction = Direction.DOWN

        if keys[pg.K_SPACE]:
            self.shoot()

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

    def rotate(self):
        if self.direction != self.rotated:
            if self.direction == Direction.DOWN:
                self.rotated_image = pg.transform.rotate(self.original_image, 180)
            elif self.direction == Direction.UP:
                self.rotated_image = pg.transform.rotate(self.original_image, 0)
            elif self.direction == Direction.LEFT:
                self.rotated_image = pg.transform.rotate(self.original_image, 90)
            elif self.direction == Direction.RIGHT:
                self.rotated_image = pg.transform.rotate(self.original_image, -90)

            self.rotated = self.direction
            self.image = self.rotated_image

    def shoot(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_bullet_time > BULLET_DELAY:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            self.bullets.add(bullet)
            self.last_bullet_time = current_time

# Enemy Class
class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image, self.rect = load_image("enemy.png")
        self.rect.topleft = (x, y)
        self.bullets = pg.sprite.Group()
        self.last_bullet_time = 0
        self.direction = Direction(random.randint(1, 4))
        self.rotated = None
        self.rotated_image = self.original_image

    def update(self):
        self.rotate()
        self.move()
        if random.randint(0, 200) < 1:
            self.shoot()
        self.bullets.update()

    def move(self):
        if self.direction == Direction.LEFT:
            self.rect.x -= ENEMY_SPEED
        elif self.direction == Direction.RIGHT:
            self.rect.x += ENEMY_SPEED
        elif self.direction == Direction.UP:
            self.rect.y -= ENEMY_SPEED
        elif self.direction == Direction.DOWN:
            self.rect.y += ENEMY_SPEED

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

        if random.randint(0, 100) < 2:
            self.direction = Direction(random.randint(1, 4))

    def shoot(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_bullet_time > BULLET_DELAY:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            self.bullets.add(bullet)
            self.last_bullet_time = current_time

    def rotate(self):
        if self.direction != self.rotated:
            if self.direction == Direction.DOWN:
                self.rotated_image = pg.transform.rotate(self.original_image, 180)
            elif self.direction == Direction.UP:
                self.rotated_image = pg.transform.rotate(self.original_image, 0)
            elif self.direction == Direction.LEFT:
                self.rotated_image = pg.transform.rotate(self.original_image, 90)
            elif self.direction == Direction.RIGHT:
                self.rotated_image = pg.transform.rotate(self.original_image, -90)

            self.rotated = self.direction
            self.image = self.rotated_image

# Create sprite groups
player_group = pg.sprite.Group()
player_group.add(Player())
enemy_group = pg.sprite.Group()

# Create enemy instances
enemies = [Enemy(0, 0), Enemy(SCREEN_WIDTH - 100, 0), Enemy(0, SCREEN_HEIGHT - 100), Enemy(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)]
enemy_group.add(enemies)

# Create the game window
screen = pg.display.set_mode((900, 900))
pg.display.set_caption("Shot the box")

# Load sound
explosion = load_sound("explosion.wav")


clock = pg.time.Clock()

# Main game loop
running = True
game_over = False
PLAYER_SIZE = 100
while running:
    clock.tick(60)
    screen.fill((255, 255, 255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if hits := pg.sprite.groupcollide(enemy_group, player_group.sprites()[0].bullets, True, True):
        explosion.play()
        for _ in hits:
            new_enemy = Enemy(random.randint(0, SCREEN_WIDTH - PLAYER_SIZE), random.randint(0, SCREEN_HEIGHT - PLAYER_SIZE))
            enemy_group.add(new_enemy)

    player_group.sprites()[0].bullets.draw(screen)

    for en in enemy_group:
        en.bullets.draw(screen)
        if pg.sprite.groupcollide(player_group, en.bullets, False, False):
            game_over = True

    if not game_over:
        player_group.update()
        enemy_group.update()

    player_group.draw(screen)
    enemy_group.draw(screen)
    pg.display.flip()

pg.quit()
sys.exit()
