import pygame as pg
from .utils import load_image
from .config import Direction, GameConfig


class Bullet(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: Direction):
        super().__init__()
        self.image, self.rect = load_image("1.png")
        self.rect.center = (x, y)
        self.direction = direction
        self.bullet_speed = GameConfig.BULLET_SPEED

    def update(self):
        if self.direction == Direction.LEFT:
            self.rect.x -= self.bullet_speed
        elif self.direction == Direction.RIGHT:
            self.rect.x += self.bullet_speed
        elif self.direction == Direction.UP:
            self.rect.y -= self.bullet_speed
        elif self.direction == Direction.DOWN:
            self.rect.y += self.bullet_speed

        if (
            self.rect.top <= 0
            or self.rect.bottom >= GameConfig.SCREEN_HEIGHT
            or self.rect.left < 0
            or self.rect.right > GameConfig.SCREEN_WIDTH
        ):
            self.kill()
