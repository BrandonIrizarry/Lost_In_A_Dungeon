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
    STAIRS_UP = pg.math.Vector2(4, 2)
    TREASURE = pg.math.Vector2(5, 3)
    PILLAR = pg.math.Vector2(3, 2)


class ImageEnv:
    """Make sure that all image-sizing data is defined and used
    coherently.

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


class Tiles:
    """Convenience class for managing a tileset.

    Fields:

    info: The ImageInfo datclass associated with the tileset.

    ienv: The ImageEnv used by our application.

    """
    def __init__(self, data_dir: str,
                 basename: str,
                 ienv: ImageEnv):
        self.info = ienv.load_image(data_dir, basename)
        self.ienv = ienv

    def load(self, tile_def: TileDef) -> ImageInfo:
        """Load a single, discrete, tile from the 'info' field.

        """
        x_tile, y_tile = tile_def.value
        size = self.ienv.size

        rect = pg.Rect(x_tile * size,
                       y_tile * size,
                       size,
                       size)

        image = self.info.image.subsurface(rect)

        return ImageInfo(image, rect)

    def blit(self, tile_info: ImageInfo, pos: pg.math.Vector2):
        """Blit the given tile onto the ienv window.

        Use the primitive coordinates defined by 'pos'.

        """
        size = self.ienv.size
        self.ienv.window.blit(tile_info.image, (pos.x * size, pos.y * size))
