#!/usr/bin/env python3
import pygame as pg
import sys
from game.config import GameConfig
from game.player import Player
from game.enemy import Enemy
from game.utils import load_sound
import random
from game.background import Background

def initialize_game():
    # Initialize Pygame
    pg.init()
    pg.mixer.init()

def create_player_group():
    player_group = pg.sprite.Group()
    player_group.add(Player())
    return player_group

def create_enemy_group():
    enemy_group = pg.sprite.Group()
    enemies = [Enemy(0, 0), Enemy(GameConfig.SCREEN_WIDTH - 100, 0),
               Enemy(0, GameConfig.SCREEN_HEIGHT - 100),
               Enemy(GameConfig.SCREEN_WIDTH - 100, GameConfig.SCREEN_HEIGHT - 100)]
    enemy_group.add(enemies)
    return enemy_group

def create_screen():
    screen = pg.display.set_mode(GameConfig.SCREEN_SIZE)
    pg.display.set_caption("Tanks")
    return screen

# ... (previous code)

def reset_game(player_group, enemy_group):
    player_group.sprites()[0].bullets.empty()
    enemy_group.empty()
    player_group.sprites()[0].rect.center = (GameConfig.SCREEN_WIDTH // 2, GameConfig.SCREEN_HEIGHT // 2)
    enemy_group.add(Enemy(0, 0), Enemy(GameConfig.SCREEN_WIDTH - 100, 0),
                    Enemy(0, GameConfig.SCREEN_HEIGHT - 100),
                    Enemy(GameConfig.SCREEN_WIDTH - 100, GameConfig.SCREEN_HEIGHT - 100))

def main():
    initialize_game()
    bg = Background()
    bg.fill()
    player_group = create_player_group()
    enemy_group = create_enemy_group()
    score = 0

    screen = create_screen()

    explosion = load_sound("explosion.wav")
    clock = pg.time.Clock()

    running = True
    game_over = False

    while running:
        clock.tick(60)
        screen.fill((255, 255, 255))
        bg.render(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and game_over:
                game_over = False
                reset_game(player_group, enemy_group)
                score = 0

        if hits := pg.sprite.groupcollide(enemy_group, player_group.sprites()[0].bullets, True, True):
            explosion.play()
            for _ in hits:
                score += 1
                new_enemy = Enemy(random.randint(0, GameConfig.SCREEN_WIDTH - GameConfig.PLAYER_SIZE),
                                  random.randint(0, GameConfig.SCREEN_HEIGHT - GameConfig.PLAYER_SIZE))
                enemy_group.add(new_enemy)

        player_group.sprites()[0].bullets.draw(screen)

        for en in enemy_group:
            en.bullets.draw(screen)

            if pg.sprite.groupcollide(player_group, en.bullets, False, False):
                game_over = True
            pg.sprite.groupcollide(player_group.sprites()[0].bullets, en.bullets, True, True)

        if not game_over:
            player_group.update()
            enemy_group.update()

        player_group.draw(screen)
        enemy_group.draw(screen)
        pg.display.flip()

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
