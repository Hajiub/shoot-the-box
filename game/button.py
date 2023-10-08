from .utils import load_image
import pygame as pg
from .config import GameConfig


# I mean a class for a single button come on
class Button(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image, self.rect = load_image('button.png', 0.6)
        self.rect.center = (GameConfig.SCREEN_WIDTH / 2, GameConfig.SCREEN_HEIGHT / 2)
