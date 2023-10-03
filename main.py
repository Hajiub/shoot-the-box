#!/usr/bin/env python3

import pygame as pg
import sys
import random


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
PLAYER_SIZE = 70
ENEMY_SIZE = 70  
BULLET_SIZE = 10
PLAYER_SPEED = 5
ENEMY_SPEED = 2  
BULLET_SPEED = 10
BULLET_DELAY = 350
ENEM_NUM = 8
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pg.Surface((BULLET_SIZE, BULLET_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction

    def update(self):
        if self.direction == "left":
            self.rect.x -= BULLET_SPEED
        elif self.direction == "right":
            self.rect.x += BULLET_SPEED
        elif self.direction == "up":
            self.rect.y -= BULLET_SPEED
        elif self.direction == "down":
            self.rect.y += BULLET_SPEED
        
        if (
            self.rect.top <= 0 
            or self.rect.bottom >= SCREEN_HEIGHT 
            or self.rect.left < 0 
            or self.rect.right > SCREEN_WIDTH
            ):
            self.kill()

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.bullets = pg.sprite.Group()
        self.last_bullet_time = 0
        self.direction = "right"

    def update(self):
        self.handle_input()
        self.move()
        self.bullets.update()

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.direction = "left"
        elif keys[pg.K_RIGHT]:
            self.direction = "right"
        elif keys[pg.K_DOWN]:
            self.direction = "down"
        elif keys[pg.K_UP]:
            self.direction = "up"

    def shoot(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_bullet_time > BULLET_DELAY:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            self.bullets.add(bullet)
            self.last_bullet_time = current_time

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        elif keys[pg.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        elif keys[pg.K_UP]:
            self.rect.y -= PLAYER_SPEED
        elif keys[pg.K_DOWN]:
            self.rect.y += PLAYER_SPEED
        
        if keys[pg.K_SPACE]:
            self.shoot()
        
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - PLAYER_SIZE))

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        self.bullets = pg.sprite.Group()
        self.last_bullet_time = 0
        self.direction = random.choice(["left", "right", "up", "down"])

    def update(self):
        self.move()
        if random.randint(0, 100) < 2:
            self.shoot()
        self.bullets.update()

    def move(self):
        if self.direction == "left":
            self.rect.x -= ENEMY_SPEED
        elif self.direction == "right":
            self.rect.x += ENEMY_SPEED
        elif self.direction == "up":
            self.rect.y -= ENEMY_SPEED
        elif self.direction == "down":
            self.rect.y += ENEMY_SPEED

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - PLAYER_SIZE))

        if random.randint(0, 100) < 2:
            self.direction = random.choice(["left", "right", "up", "down"])

    def shoot(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_bullet_time > BULLET_DELAY:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            self.bullets.add(bullet)
            self.last_bullet_time = current_time


def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Shoot the Box")
    clock = pg.time.Clock()

    player_group = pg.sprite.Group()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE)
    player_group.add(player)

    enemy_group = pg.sprite.Group()
    for _ in range(ENEM_NUM): 
        enemy = Enemy()
        enemy_group.add(enemy)
    game_over = False

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if not game_over:
            player_group.update()
            enemy_group.update()

        
        hits = pg.sprite.groupcollide(enemy_group, player.bullets, True, True)
        
        
        for _ in hits:
            new_enemy = Enemy()
            enemy_group.add(new_enemy)

        screen.fill((255, 255, 255))
        
        player.bullets.draw(screen)
        

        for enemy in enemy_group:
            enemy.bullets.draw(screen)
            # game over
            if pg.sprite.groupcollide(player_group, enemy.bullets, False, False):
                game_over = True
            pg.sprite.groupcollide(enemy.bullets, player.bullets, True, True)

        enemy_group.draw(screen)
        player_group.draw(screen)
        pg.display.flip()
        clock.tick(60)

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
