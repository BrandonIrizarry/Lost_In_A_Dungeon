import pygame
from enum import Enum
import constants as cs


class TileDef(Enum):
    STAIRS_DOWN = (pygame.math.Vector2(5, 2), None)
    STAIRS_UP = (pygame.math.Vector2(4, 2), None)
    TREASURE = (pygame.math.Vector2(5, 3), None)
    PILLAR = (pygame.math.Vector2(3, 2), None)

    PLAYER_DOWN_1 = (pygame.math.Vector2(0, 8),
                     pygame.Color("#00288c"))

    PLAYER_DOWN_2 = (pygame.math.Vector2(1, 8),
                     pygame.Color("#00288c"))

    PLAYER_UP_1 = (pygame.math.Vector2(2, 8),
                   pygame.Color("#00288c"))

    PLAYER_UP_2 = (pygame.math.Vector2(3, 8),
                   pygame.Color("#00288c"))

    PLAYER_LEFT_1 = (pygame.math.Vector2(4, 8),
                     pygame.Color("#00288c"))

    PLAYER_LEFT_2 = (pygame.math.Vector2(5, 8),
                     pygame.Color("#00288c"))

    PLAYER_RIGHT_1 = (pygame.math.Vector2(6, 8),
                      pygame.Color("#00288c"))

    PLAYER_RIGHT_2 = (pygame.math.Vector2(7, 8),
                      pygame.Color("#00288c"))


class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def get(self, tile_def: TileDef) -> pygame.Surface:
        """Fetch a single, discrete, tile from 'self.sheet'.

        Return the tile as a pygame.Surface object.

        It's assumed that each tile is a square of 'size'x'size'
        pixels inside the spritesheet.

        """
        tile_data = tile_def.value
        x_tile, y_tile = tile_data[0]
        color_key = tile_data[1]

        rect = pygame.Rect(x_tile * cs.TILE_LEN,
                           y_tile * cs.TILE_LEN,
                           cs.TILE_LEN,
                           cs.TILE_LEN)

        image = self.sheet.subsurface(rect)

        if color_key:
            image.set_colorkey(color_key)

        return pygame.transform.scale_by(image, cs.SCALE_FACTOR)


class Player(pygame.sprite.Sprite):
    def __init__(self, spritesheet: Spritesheet):
        super().__init__()
        down1 = spritesheet.get(TileDef.PLAYER_DOWN_1)
        down2 = spritesheet.get(TileDef.PLAYER_DOWN_2)
        self.walk = [down1, down2]
        self.index = 0

        # Define the image and rect of this sprite.
        self.image = down1
        self.rect = self.image.get_rect()

    def update(self, dt):
        self._handle_player_input()
        self._animation_state(dt)

    def _handle_player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.rect.y -= 1
        elif keys[pygame.K_DOWN]:
            self.rect.y += 1
        elif keys[pygame.K_LEFT]:
            self.rect.x -= 1
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 1

    def _animation_state(self, dt):
        self.index += dt

        if self.index >= len(self.walk):
            self.index = 0

        self.image = self.walk[int(self.index)]


def display(screen, what, x, y):
    xs, ys = cs.compute_coords(x, y)

    return screen.blit(what, (xs, ys))


pygame.init()
screen = pygame.display.set_mode((cs.SCREEN_LEN, cs.SCREEN_LEN))
sheet = Spritesheet("../graphics/spritesheet.png")

player = Player(sheet)
player_group = pygame.sprite.GroupSingle()
player_group.add(player)


def mainloop():
    """The main pygame loop.

    The loop is encapsulated inside this function so that we can easily
    quit the game with a 'return' statement.

    """
    stairs = sheet.get(TileDef.STAIRS_DOWN)
    player = sheet.get(TileDef.PLAYER_DOWN_1)

    clock = pygame.time.Clock()
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        return

        # Important: this prevents moving, animated sprites from
        # leaving streaks.
        screen.fill(pygame.Color("black"))

        for i in range(18):
            display(screen, stairs, i, 0)

        player_group.draw(screen)
        player_group.update(dt)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


mainloop()
pygame.quit()
