import pygame as pg
from .box import Box
from .config import GameConfig

class Background:
    def __init__(self):
        self.background = pg.Surface(GameConfig.SCREEN_SIZE)
        self.background.fill(GameConfig.BACKGROUND_COLOR)
        self.rect = self.background.get_rect()
        self.box_size = GameConfig.BULLET_SIZE
        self.rows = GameConfig.SCREEN_WIDTH // self.box_size
        self.cols = GameConfig.SCREEN_HEIGHT // self.box_size

    def fill(self):
        for i in range(self.cols):
            for j in range(self.rows):
                box = Box(i * self.box_size, j * self.box_size)
                self.background.blit(box.image, box.rect)

    def render(self, win):
        win.blit(self.background, self.rect)
