import pygame as pg
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ImageInfo:
    image: pg.Surface
    rect: pg.Rect


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


window = pg.display.set_mode((128, 128))
tileset_info = load_image("ff_castle.png")

location = pg.math.Vector2(96, 96)
rectangle = pg.Rect(64, 0, 64, 64)

window.blit(tileset_info.image, (0, 0))


def mainloop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        pg.display.flip()


mainloop()
pg.quit()
