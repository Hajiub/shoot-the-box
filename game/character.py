import pygame as pg
from .bullet import Bullet
from .config import Direction, GameConfig
from .utils import load_image
import random

class Character(pg.sprite.Sprite):
    def __init__(self, file):
        super().__init__()
        self.original_image, self.rect = load_image(file)
        self.current_direction = None
        self.image = self.original_image
        self.bullets = pg.sprite.Group()
        self.last_bullet_time = 0
        self.direction = Direction(random.randint(1, 4))
    def update(self):
        self.move()
        self.rotate()
        self.bullets.update()

    def move(self):
        pass

    def rotate(self):
        if self.direction != self.current_direction:
            if self.direction == Direction.DOWN:
                rotated_image = pg.transform.rotate(self.original_image, 180)
            elif self.direction == Direction.UP:
                rotated_image = pg.transform.rotate(self.original_image, 0)
            elif self.direction == Direction.LEFT:
                rotated_image = pg.transform.rotate(self.original_image, 90)
            elif self.direction == Direction.RIGHT:
                rotated_image = pg.transform.rotate(self.original_image, -90)

        self.current_direcation = self.direction
        self.image = rotated_image

    def shoot(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_bullet_time > GameConfig.BULLET_DELAY:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            self.bullets.add(bullet)
            self.last_bullet_time = current_time
        
