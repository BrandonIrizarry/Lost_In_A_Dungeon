import pygame
from enum import Enum
import constants as cs


class TileDef(Enum):
    STAIRS_DOWN = pygame.math.Vector2(5, 2)
    STAIRS_UP = pygame.math.Vector2(4, 2)
    TREASURE = pygame.math.Vector2(5, 3)
    PILLAR = pygame.math.Vector2(3, 2)


class Spritesheet:
    def __init__(self, filename, size, scale_factor):
        self.sheet = pygame.image.load(filename).convert()
        self.size = size
        self.scale_factor = scale_factor

    def get(self, tile_def: TileDef) -> pygame.Surface:
        """Fetch a single, discrete, tile from 'self.sheet'.

        Return the tile as a pygame.Surface object.

        It's assumed that each tile is a square of 'size'x'size'
        pixels inside the spritesheet.

        """
        x_tile, y_tile = tile_def.value

        rect = pygame.Rect(x_tile * self.size,
                           y_tile * self.size,
                           self.size,
                           self.size)

        image = self.sheet.subsurface(rect)
        return pygame.transform.scale_by(image, self.scale_factor)


pygame.init()
screen = pygame.display.set_mode((cs.SCREEN_LEN, cs.SCREEN_LEN))
sheet = Spritesheet("../graphics/ff_castle.png", cs.TILE_LEN, cs.SCALE_FACTOR)


def mainloop():
    """The main pygame loop.

    The loop is encapsulated inside this function so that we can easily
    quit the game with a 'return' statement.

    """
    floor = sheet.get(TileDef.STAIRS_DOWN)
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
            index_x = cs.compute_index(i)
            index_y = cs.compute_index(0)

            screen.blit(floor, (index_x, index_y))

        pygame.display.flip()
        clock.tick(60)


mainloop()
pygame.quit()
