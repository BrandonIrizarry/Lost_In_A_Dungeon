import pygame
from enum import Enum
import constants as cs


class TileDef(Enum):
    STAIRS_DOWN = pygame.math.Vector2(5, 2)
    STAIRS_UP = pygame.math.Vector2(4, 2)
    TREASURE = pygame.math.Vector2(5, 3)
    PILLAR = pygame.math.Vector2(3, 2)
    PLAYER = pygame.math.Vector2(0, 0)


class Spritesheet:
    def __init__(self, filename, tile_len, scale_factor, color_key=None):
        self.sheet = pygame.image.load(filename).convert()
        self.tile_len = tile_len
        self.scale_factor = scale_factor
        self.color_key = color_key

    def get(self, tile_def: TileDef) -> pygame.Surface:
        """Fetch a single, discrete, tile from 'self.sheet'.

        Return the tile as a pygame.Surface object.

        It's assumed that each tile is a square of 'size'x'size'
        pixels inside the spritesheet.

        """
        x_tile, y_tile = tile_def.value

        rect = pygame.Rect(x_tile * self.tile_len,
                           y_tile * self.tile_len,
                           self.tile_len,
                           self.tile_len)

        image = self.sheet.subsurface(rect)

        if self.color_key:
            image.set_colorkey(self.color_key)

        return pygame.transform.scale_by(image, self.scale_factor)


pygame.init()
screen = pygame.display.set_mode((cs.SCREEN_LEN, cs.SCREEN_LEN))
terrain_sheet = Spritesheet("../graphics/ff_castle.png",
                            cs.TILE_LEN,
                            cs.SCALE_FACTOR)
player_sheet = Spritesheet("../graphics/player.png",
                           cs.TILE_LEN,
                           cs.SCALE_FACTOR,
                           pygame.Color("#00288c"))


def mainloop():
    """The main pygame loop.

    The loop is encapsulated inside this function so that we can easily
    quit the game with a 'return' statement.

    """
    floor = terrain_sheet.get(TileDef.STAIRS_DOWN)
    player = player_sheet.get(TileDef.PLAYER)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        return

        for i in range(18):
            index_x, index_y = cs.compute_coords(i, 0)
            screen.blit(floor, (index_x, index_y))

        xs, ys = cs.compute_coords(5, 5)
        screen.blit(player, (xs, ys))

        pygame.display.flip()
        clock.tick(60)


mainloop()
pygame.quit()
