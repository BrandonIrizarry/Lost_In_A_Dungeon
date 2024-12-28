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
tiles = image_env.Tiles(data_dir, "ff_castle.png", ienv)

stairs_down = tiles.load(image_env.TileDef.STAIRS_DOWN)
stairs_up = tiles.load(image_env.TileDef.STAIRS_UP)
treasure = tiles.load(image_env.TileDef.TREASURE)
pillar = tiles.load(image_env.TileDef.PILLAR)

window.blit(stairs_down.image, (ienv.size, ienv.size))
window.blit(stairs_up.image, (2 * ienv.size, 3 * ienv.size))
window.blit(treasure.image, (6 * ienv.size, 3 * ienv.size))
window.blit(pillar.image, (4 * ienv.size, 4 * ienv.size))


def mainloop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        pg.display.flip()


mainloop()
pg.quit()
