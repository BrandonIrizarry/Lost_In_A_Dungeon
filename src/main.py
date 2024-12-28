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

stairs_down = ienv.load_tile(image_env.TileDef.STAIRS_DOWN,
                             tileset_info)

stairs_up = ienv.load_tile(image_env.TileDef.STAIRS_UP,
                           tileset_info)

treasure = ienv.load_tile(image_env.TileDef.TREASURE,
                          tileset_info)

pillar = ienv.load_tile(image_env.TileDef.PILLAR,
                        tileset_info)

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
