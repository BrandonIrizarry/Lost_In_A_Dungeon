import pygame


class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

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


pygame.init()
screen = pygame.display.set_mode((800, 500))

sheet = Spritesheet("../graphics/ff_castle.png")


def mainloop():
    """The main pygame loop.

    The loop is encapsulated inside this function so that we can easily
    quit the game with a 'return' statement.

    """
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        return

        pygame.display.flip()
        clock.tick(60)


mainloop()
pygame.quit()
