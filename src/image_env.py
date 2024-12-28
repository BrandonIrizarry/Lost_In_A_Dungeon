from enum import Enum
from dataclasses import dataclass
import pygame as pg
import os


@dataclass(frozen=True)
class ImageInfo:
    image: pg.Surface
    rect: pg.Rect


class TileDef(Enum):
    STAIRS_DOWN = pg.math.Vector2(5, 2)


class ImageEnv:
    """A class bundling all image and tile data into a consistent
    whole.

    Fields:

    scale: The overall scale factor applied to the game display as a
    whole.

    size: The *original* size of each sprite in the given tileset, in
    pixels.

    window: The window used to display the game.

    """
    def __init__(self,
                 win_width: float,
                 win_height: float,
                 scale: float,
                 size: float):
        self.scale = scale
        self.size = size * scale
        self.window = pg.display.set_mode((win_width * scale,
                                           win_height * scale))

    def load_tile(self, tile: TileDef, tileset_info: ImageInfo) -> ImageInfo:
        """Load a single, discrete tile from a tileset.

        """

        x_tile, y_tile = tile.value

        rect = pg.Rect(x_tile * self.size,
                       y_tile * self.size,
                       self.size,
                       self.size)

        image = tileset_info.image.subsurface(rect)

        return ImageInfo(image, rect)

    def load_image(self, data_dir, name) -> ImageInfo:
        """Helper function for loading images."""

        fullname = os.path.join(data_dir, name)
        image = pg.image.load(fullname)

        size_x, size_y = image.get_size()
        scale_factor = (size_x * self.scale, size_y * self.scale)
        image = pg.transform.scale(image, scale_factor)

        try:
            image = image.convert()
        except Exception as e:
            print(f"\n---> {e} :)")

        return ImageInfo(image, image.get_rect())
