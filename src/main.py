import pygame as pg
import os
import image_env


# Use platform independent file paths.
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "../data")

ienv = image_env.ImageEnv(win_width=128,
                          win_height=128,
                          scale=2, size=16)

window = ienv.window
tileset_info = ienv.load_image(data_dir, "ff_castle.png")
tile_info = ienv.load_tile(image_env.Tile.STAIRS_DOWN,
                           tileset_info)

window.blit(tile_info.image, (ienv.size, ienv.size))


def mainloop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        pg.display.flip()


mainloop()
pg.quit()
