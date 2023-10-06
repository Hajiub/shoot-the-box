import pygame as pg
from .character import Character
from .config import GameConfig, Direction

class Player(Character):
    def __init__(self):
        super().__init__('player.png')
        self.rect.center = (GameConfig.SCREEN_WIDTH // 2, GameConfig.SCREEN_HEIGHT // 2)
        self.player_speed = GameConfig.PLAYER_SPEED

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rect.x -= self.player_speed
            self.direction = Direction.LEFT
        elif keys[pg.K_RIGHT]:
            self.rect.x += self.player_speed
            self.direction = Direction.RIGHT
        
        elif keys[pg.K_UP]:
            self.rect.y -= self.player_speed
            self.direction = Direction.UP
        
        elif keys[pg.K_DOWN]:
            self.rect.y += self.player_speed
            self.direction = Direction.DOWN

        if keys[pg.K_SPACE]:
            self.shoot()
        
        self.rect.x = max(0, min(self.rect.x, GameConfig.SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, GameConfig.SCREEN_HEIGHT - self.rect.height))