import pygame as pg
from .utils import load_image


class Box(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image, self.rect = load_image('0.png')
        self.rect.topleft = (x, y)
    