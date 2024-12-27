import pygame as pg
import os


# Use platform independent file paths.
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


def load_image(name, colorkey=None, scale=1):
    """Helper function for loading images."""

    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)

    size_x, size_y = image.get_size()
    size = (size_x * scale, size_y * scale)
    image = pg.transform.scale(image, size).convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))

        image.set_colorkey(colorkey, pg.RLEACCEL)

    return image, image.get_rect()
