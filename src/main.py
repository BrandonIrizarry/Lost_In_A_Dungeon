import pygame
from enum import Enum


class TileDef(Enum):
    STAIRS_DOWN = pygame.math.Vector2(5, 2)
    STAIRS_UP = pygame.math.Vector2(4, 2)
    TREASURE = pygame.math.Vector2(5, 3)
    PILLAR = pygame.math.Vector2(3, 2)


class Spritesheet:
    def __init__(self, filename, size):
        self.sheet = pygame.image.load(filename).convert()
        self.size = size

    def get(self,
            x: int,
            y: int,
            width: int,
            height: int) -> pygame.Surface:
        """Fetch a sprite image.

        In other words, return the Surface corresponding to the given
        measured-out section of the spritesheet, in cookie-cutter
        fashion.

        """
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))

        return sprite

    def load(self, tile_def: TileDef) -> pygame.Surface:
        """Load a single, discrete, tile from the 'info' field.

        """
        x_tile, y_tile = tile_def.value

        rect = pygame.Rect(x_tile * self.size,
                           y_tile * self.size,
                           self.size,
                           self.size)

        image = self.sheet.subsurface(rect)
        return image


pygame.init()
screen = pygame.display.set_mode((800, 500))

sheet = Spritesheet("../graphics/ff_castle.png", 16)


def mainloop():
    """The main pygame loop.

    The loop is encapsulated inside this function so that we can easily
    quit the game with a 'return' statement.

    """
    floor = sheet.load(TileDef.STAIRS_DOWN)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        return

        screen.blit(floor, (0, 0))

        pygame.display.flip()
        clock.tick(60)


mainloop()
pygame.quit()
