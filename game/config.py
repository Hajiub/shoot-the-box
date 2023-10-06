from enum import Enum

class GameConfig:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    SCREEN_SIZE  = SCREEN_WIDTH, SCREEN_HEIGHT
    BULLET_SIZE = 40
    PLAYER_SPEED = 5
    PLAYER_SIZE  = 120
    ENEMY_SPEED = 2
    BULLET_SPEED = 10
    BULLET_DELAY = 350
    ENEM_NUM     = 4


class Direction(Enum):
    RIGHT = 1
    LEFT  = 2
    UP    = 3
    DOWN  = 4
