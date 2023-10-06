#!/usr/bin/env python3
import pygame as pg
import sys
from game.config import GameConfig
from game.player import Player
from game.enemy import Enemy
from game.utils import load_sound
import random


SCREEN_WIDTH, SCREEN_HEIGHT = GameConfig.SCREEN_SIZE
pg.init()
pg.mixer.init()

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
