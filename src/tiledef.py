from enum import Enum
from pygame.math import Vector2
from pygame import Color


class TileDef(Enum):
    """Labels for each of the sprites used in this game.

    A TileDef is a tuple whose first member is a pair of coordinates
    into the spritesheet, and whose second member is the color_key
    needed to display that sprite correctly.

    Each tile is assumed to be 16x16 pixels.

    """
    STAIRS_DOWN = (Vector2(5, 2), None)
    STAIRS_UP = (Vector2(4, 2), None)
    TREASURE = (Vector2(5, 3), None)
    PILLAR = (Vector2(3, 2), None)
    PLAYER_DOWN_1 = (Vector2(0, 8), Color("#00288c"))
    PLAYER_DOWN_2 = (Vector2(1, 8), Color("#00288c"))
    PLAYER_UP_1 = (Vector2(2, 8), Color("#00288c"))
    PLAYER_UP_2 = (Vector2(3, 8), Color("#00288c"))
    PLAYER_LEFT_1 = (Vector2(4, 8), Color("#00288c"))
    PLAYER_LEFT_2 = (Vector2(5, 8), Color("#00288c"))
    PLAYER_RIGHT_1 = (Vector2(6, 8), Color("#00288c"))
    PLAYER_RIGHT_2 = (Vector2(7, 8), Color("#00288c"))
    CRAWLER_DOWN_1 = (Vector2(0, 7), Color("#747474"))
    CRAWLER_DOWN_2 = (Vector2(1, 7), Color("#747474"))
    CRAWLER_UP_1 = (Vector2(2, 7), Color("#747474"))
    CRAWLER_UP_2 = (Vector2(3, 7), Color("#747474"))
    CRAWLER_LEFT_1 = (Vector2(4, 7), Color("#747474"))
    CRAWLER_LEFT_2 = (Vector2(5, 7), Color("#747474"))
    CRAWLER_RIGHT_1 = (Vector2(6, 7), Color("#747474"))
    CRAWLER_RIGHT_2 = (Vector2(7, 7), Color("#747474"))
    FLOOR = (Vector2(6, 1), None)
    SWORD = (Vector2(0, 6), None)
