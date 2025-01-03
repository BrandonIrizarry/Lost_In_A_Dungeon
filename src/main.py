import pygame
from enum import Enum, auto
import constants as cs


class TileDef(Enum):
    """Labels for each of the sprites used in this game.

    A TileDef is a tuple whose first member is a pair of coordinates
    into the spritesheet, and whose second member is the color_key
    needed to display that sprite correctly.

    Each tile is assumed to be 16x16 pixels.

    """
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


class Orientation(Enum):
    """A set of states used to describe the physical orientation of a
    sprite.

    For example, if a sprite is facing up, it's described using
    'Orientation.UP'.

    """
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Spritesheet:
    """Bundle a sprite sheet image together with a method for fetching
    sprites.

    Fields:

    sheet: The image corresponding to the sprite sheet. This is loaded
    once upon initialization.

    """
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
    """An obligatory definition of the human-controlled Player
    sprite.

    Other than 'image' and 'rect', many of the fields involve
    controlling the player animation.

    The class field 'ANIMATION_SPEED' is used for configuring how
    quickly the player's motion animation is toggled.

    """

    # Configure the player sprite using this variable.
    ANIMATION_SPEED = 5

    def __init__(self, spritesheet: Spritesheet, x: int, y: int):
        super().__init__()
        down1 = spritesheet.get(TileDef.PLAYER_DOWN_1)
        down2 = spritesheet.get(TileDef.PLAYER_DOWN_2)
        up1 = spritesheet.get(TileDef.PLAYER_UP_1)
        up2 = spritesheet.get(TileDef.PLAYER_UP_2)
        left1 = spritesheet.get(TileDef.PLAYER_LEFT_1)
        left2 = spritesheet.get(TileDef.PLAYER_LEFT_2)
        right1 = spritesheet.get(TileDef.PLAYER_RIGHT_1)
        right2 = spritesheet.get(TileDef.PLAYER_RIGHT_2)

        self.walk_down = [down1, down2]
        self.walk_up = [up1, up2]
        self.walk_left = [left1, left2]
        self.walk_right = [right1, right2]
        self.orientation = Orientation.DOWN

        self.index = 0

        # Define the image and rect of this sprite.
        self.image = down1

        xs, ys = cs.compute_coords(x, y)
        self.rect = self.image.get_rect(x=xs, y=ys)

    def update(self, dt, still):
        """The obligatory 'update' override.

        This in turn calls various private helper methods.

        """

        self._handle_player_input()
        self._animation_state(dt, still)

    def _handle_player_input(self):
        """Interface with the current keypress to determine a player
        action, and update the details of the player's state.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.orientation = Orientation.UP
            self.rect.y -= 1
        elif keys[pygame.K_DOWN]:
            self.orientation = Orientation.DOWN
            self.rect.y += 1
        elif keys[pygame.K_LEFT]:
            self.orientation = Orientation.LEFT
            self.rect.x -= 1
        elif keys[pygame.K_RIGHT]:
            self.orientation = Orientation.RIGHT
            self.rect.x += 1

    def _animation_state(self, dt, still):
        """Determine which spritesheet image to display, and which
        toggle to use.

        """
        walk = None

        match self.orientation:
            case Orientation.UP:
                walk = self.walk_up
            case Orientation.DOWN:
                walk = self.walk_down
            case Orientation.LEFT:
                walk = self.walk_left
            case Orientation.RIGHT:
                walk = self.walk_right

        if walk is None:
            raise Exception("'walk' is never set")

        if not still:
            self.index += self.ANIMATION_SPEED * dt

            if self.index >= len(walk):
                self.index = 0

        self.image = walk[int(self.index)]


class Pillar(pygame.sprite.Sprite):
    def __init__(self, sheet: Spritesheet, x: int, y: int, *groups):
        super().__init__(*groups)

        self.image = sheet.get(TileDef.PILLAR)

        xs, ys = cs.compute_coords(x, y)
        self.rect = self.image.get_rect(x=xs, y=ys)


pygame.init()
screen = pygame.display.set_mode((cs.SCREEN_LEN, cs.SCREEN_LEN))
sheet = Spritesheet("../graphics/spritesheet.png")

player = Player(sheet, 1, 1)
player_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
player_group.add(player)

pillar_group: pygame.sprite.Group = pygame.sprite.Group()


for i in range(cs.NUM_TILES):
    Pillar(sheet, i, 0, pillar_group)
    Pillar(sheet, i, cs.NUM_TILES, pillar_group)

for i in range(1, cs.NUM_TILES - 1):
    Pillar(sheet, 0, i, pillar_group)
    Pillar(sheet, cs.NUM_TILES - 1, i, pillar_group)


def mainloop():
    """The main pygame loop.

    The loop is encapsulated inside this function so that we can easily
    quit the game with a 'return' statement.

    """
    clock = pygame.time.Clock()
    dt = 0
    still = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        return

            if event.type == pygame.KEYUP:
                still = True

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] or keys[pygame.K_DOWN]\
               or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                still = False

        # Important: this prevents moving, animated sprites from
        # leaving streaks.
        screen.fill(pygame.Color("black"))

        pillar_group.draw(screen)
        player_group.draw(screen)
        player_group.update(dt, still)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


mainloop()
pygame.quit()
