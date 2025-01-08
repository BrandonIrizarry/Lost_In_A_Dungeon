import pygame
from enum import Enum, auto
import random
import constants as cs
import maze


type Point = tuple[int, int]


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

    CRAWLER_DOWN_1 = (pygame.math.Vector2(0, 7),
                      pygame.Color("#747474"))

    CRAWLER_DOWN_2 = (pygame.math.Vector2(1, 7),
                      pygame.Color("#747474"))

    CRAWLER_UP_1 = (pygame.math.Vector2(2, 7),
                    pygame.Color("#747474"))

    CRAWLER_UP_2 = (pygame.math.Vector2(3, 7),
                    pygame.Color("#747474"))

    CRAWLER_LEFT_1 = (pygame.math.Vector2(4, 7),
                      pygame.Color("#747474"))

    CRAWLER_LEFT_2 = (pygame.math.Vector2(5, 7),
                      pygame.Color("#747474"))

    CRAWLER_RIGHT_1 = (pygame.math.Vector2(6, 7),
                       pygame.Color("#747474"))

    CRAWLER_RIGHT_2 = (pygame.math.Vector2(7, 7),
                       pygame.Color("#747474"))

    FLOOR = (pygame.math.Vector2(6, 1), None)


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


class Crawler(pygame.sprite.Sprite):
    ANIMATION_SPEED = 5

    def __init__(self, spritesheet: Spritesheet, x: int, y: int, *groups):
        super().__init__(*groups)

        down1 = spritesheet.get(TileDef.CRAWLER_DOWN_1)
        down2 = spritesheet.get(TileDef.CRAWLER_DOWN_2)
        up1 = spritesheet.get(TileDef.CRAWLER_UP_1)
        up2 = spritesheet.get(TileDef.CRAWLER_UP_2)
        left1 = spritesheet.get(TileDef.CRAWLER_LEFT_1)
        left2 = spritesheet.get(TileDef.CRAWLER_LEFT_2)
        right1 = spritesheet.get(TileDef.CRAWLER_RIGHT_1)
        right2 = spritesheet.get(TileDef.CRAWLER_RIGHT_2)

        self.walk_down = [down1, down2]
        self.walk_up = [up1, up2]
        self.walk_left = [left1, left2]
        self.walk_right = [right1, right2]

        self.index = 0
        self.image = random.choice([up1, down1, left1, right1])

        xs, ys = cs.compute_pixel_coords(x, y)
        self.rect = self.image.get_rect(x=xs, y=ys)

    def update(self, dt, dx, dy):
        # Update position
        self.rect.x += dx
        self.rect.y += dy

        # Update walking animation
        vector = (dx, dy)

        walk = None

        if vector == (0, -1):
            walk = self.walk_up
        elif vector == (0, 1):
            walk = self.walk_down
        elif vector == (-1, 0):
            walk = self.walk_left
        elif vector == (1, 0):
            walk = self.walk_right

        if walk is None:
            return

        self.index += self.ANIMATION_SPEED * dt

        if self.index >= len(walk):
            self.index = 0

        self.image = walk[int(self.index)]


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

        xs, ys = cs.compute_pixel_coords(x, y)
        self.rect = self.image.get_rect(x=xs, y=ys)

    def update(self, dt, dx, dy):
        """The obligatory 'update' override.

        This in turn calls various private helper methods.

        """

        self._update_position(dx, dy)

        still = dx == 0 and dy == 0
        self._animation_state(dt, still)

    def _update_position(self, dx, dy):
        """Interface with the current keypress to determine a player
        action, and update the details of the player's state.
        """

        vector = (dx, dy)

        if vector == (0, -1):
            self.orientation = Orientation.UP
        elif vector == (0, 1):
            self.orientation = Orientation.DOWN
        elif vector == (-1, 0):
            self.orientation = Orientation.LEFT
        elif vector == (1, 0):
            self.orientation = Orientation.RIGHT

        self.rect.x += dx
        self.rect.y += dy

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

        xs, ys = cs.compute_pixel_coords(x, y)
        self.rect = self.image.get_rect(x=xs, y=ys)


class Floor(pygame.sprite.Sprite):
    def __init__(self, sheet: Spritesheet, x: int, y: int, *groups):
        super().__init__(*groups)

        self.image = sheet.get(TileDef.FLOOR)

        xs, ys = cs.compute_pixel_coords(x, y)
        self.rect = self.image.get_rect(x=xs, y=ys)


pygame.init()

grid = maze.Grid(cs.GRID_X, cs.GRID_Y)
grid.carve()

screen_dimensions = cs.compute_pixel_coords(cs.NUM_TILES_X, cs.NUM_TILES_Y)
screen = pygame.display.set_mode(screen_dimensions)
sheet = Spritesheet("../graphics/spritesheet.png")

player = Player(sheet, 1, 1)
player_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
player_group.add(player)

pillar_group: pygame.sprite.Group = pygame.sprite.Group()
floor_group: pygame.sprite.Group = pygame.sprite.Group()
crawler_group: pygame.sprite.Group = pygame.sprite.Group()


def compute_cell_projection(grid: maze.Grid, x: int, y: int) -> list[Point]:
    """Determine where pillars will be drawn on the board based on a
    given cell.

    'x' and 'y' are coordinates inside the given grid."""

    # Pairs of coordinates where pillars will be drawn.
    targets = []

    # Compute the _inverse_ of a cell, that is, compute which sides
    # should be closed off by pillars.
    cell = ~grid.grid[x][y]

    xi, yi = 3 * x, 3 * y

    # Add the four corners of the projection to 'targets', since these
    # otherwise appear as gaps in the displayed maze.
    targets.extend([(xi, yi), (xi + 3, yi), (xi, yi + 3), (xi + 3, yi + 3)])

    if maze.Cell.UP in cell:
        targets.extend([(xi + 1, yi), (xi + 2, yi)])

    if maze.Cell.DOWN in cell:
        targets.extend([(xi + 1, yi + 3), (xi + 2, yi + 3)])

    if maze.Cell.LEFT in cell:
        targets.extend([(xi, yi + 1), (xi, yi + 2)])

    if maze.Cell.RIGHT in cell:
        targets.extend([(xi + 3, yi + 1), (xi + 3, yi + 2)])

    return targets


# Use a set, so that we can remove duplicates (we don't add a pillar
# twice to a given board position.)
all_projections = set()

for x in range(cs.GRID_X):
    for y in range(cs.GRID_Y):
        projection = compute_cell_projection(grid, x, y)

        for p in projection:
            all_projections.add(p)

for x, y in all_projections:
    Pillar(sheet, x, y, pillar_group)


# Add the floor graphics.
for x in range(cs.NUM_TILES_X):
    for y in range(cs.NUM_TILES_Y):
        if (x, y) not in all_projections:
            Floor(sheet, x, y, floor_group)


# Add the crawlers.
Crawler(sheet, 2, 2, crawler_group)

def get_next_player_move() -> Point:
    """Move the player in the direction provided by the user.

    If there is a blocked collision, don't allow the move.

    """

    # Reset motion vector to 0 for this frame.
    dx, dy = 0, 0

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        dy = -1
    elif keys[pygame.K_DOWN]:
        dy = 1
    elif keys[pygame.K_LEFT]:
        dx = -1
    elif keys[pygame.K_RIGHT]:
        dx = 1

    # The tentative player position.
    tentative = player_group.sprite.rect.move(dx, dy)

    for pillar in pillar_group:
        if tentative.colliderect(pillar.rect):
            return 0, 0

    return dx, dy


def get_next_crawler_move(crawler: Crawler) -> Point:
    dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])

    tentative = crawler.rect.move(dx, dy)

    for pillar in pillar_group:
        if tentative.colliderect(pillar.rect):
            return 0, 0

    return dx, dy


def mainloop():
    """The main pygame loop.

    The loop is encapsulated inside this function so that we can easily
    quit the game with a 'return' statement.

    """
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

        pillar_group.draw(screen)
        floor_group.draw(screen)
        player_group.draw(screen)
        crawler_group.draw(screen)

        dx_player, dy_player = get_next_player_move()
        player_group.update(dt, dx_player, dy_player)

        for crawler in crawler_group:
            dx_crawler, dy_crawler = get_next_crawler_move(crawler)
            crawler.update(dt, dx_crawler, dy_crawler)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


mainloop()
pygame.quit()
