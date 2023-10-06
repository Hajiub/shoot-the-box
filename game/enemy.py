from .character import Character
import random
from .config import Direction, GameConfig

class Enemy(Character):
    def __init__(self, x, y):
        super().__init__('player.png')
        self.rect.topleft = (x, y)
        self.speed = GameConfig.ENEMY_SPEED

    def move(self):
        if self.direction == Direction.LEFT:
            self.rect.x -= self.speed
        elif self.direction == Direction.RIGHT:
            self.rect.x += self.speed
        elif self.direction == Direction.UP:
            self.rect.y -= self.speed
        elif self.direction == Direction.DOWN:
            self.rect.y += self.speed

        self.rect.x = max(0, min(self.rect.x, GameConfig.SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, GameConfig.SCREEN_HEIGHT - self.rect.height))

        if random.randint(0, 100) < 2:
            self.direction = Direction(random.randint(1, 4))
        
        if random.randint(0, 200) < 1:
            self.shoot()