import pygame as pg
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ImageInfo:
    image: pg.Surface
    rect: pg.Rect


tile_legend = {
    "stairs_down": pg.math.Vector2(5, 2)
}


# Use platform independent file paths.
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "../data")


def load_image(name, scale=1) -> ImageInfo:
    """Helper function for loading images."""

    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)

    size_x, size_y = image.get_size()
    size = (size_x * scale, size_y * scale)
    image = pg.transform.scale(image, size)

    try:
        image = image.convert()
    except Exception as e:
        print(f"\n---> {e} :)")

    return ImageInfo(image, image.get_rect())


scale = 1
window = pg.display.set_mode((128 * scale, 128 * scale))
tileset_info = load_image("ff_castle.png", scale)


def load_tile(tile_name: str,
              tileset_info: ImageInfo,
              size: float) -> ImageInfo:

    x_tile, y_tile = tile_legend[tile_name]
    rect = pg.Rect(x_tile * size, y_tile * size, size, size)

    image = tileset_info.image.subsurface(rect)

    return ImageInfo(image, rect)


tile_info = load_tile("stairs_down", tileset_info, 16)

window.blit(tile_info.image, (16, 16))


def mainloop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        pg.display.flip()


mainloop()
pg.quit()
