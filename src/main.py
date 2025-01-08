import pygame
from enum import Enum
import random
import constants as cs
import maze
from pygame.math import Vector2


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

    def get_all(self, tile_defs: list[TileDef]) -> list[pygame.Surface]:
        """Convert the given list of tile defs to a list of surfaces."""

        return [self.get(tile_def) for tile_def in tile_defs]


class Orient(Enum):
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)


class MovingThing(pygame.sprite.Sprite):
    """Parent class (morally) of player and crawler sprites.

    Right now player is a direct instance of this class.

    """

    def __init__(self, x: int, y: int, **animations):
        super().__init__()

        self.motions_table = {
            Orient.DOWN: [animations["down"][0], animations["down"][1]],
            Orient.UP: [animations["up"][0], animations["up"][1]],
            Orient.LEFT: [animations["left"][0], animations["left"][1]],
            Orient.RIGHT: [animations["right"][0], animations["right"][1]]
        }

        self.animation_speed = 5
        self.index = 0
        self.speed = 200

        # Define the image and rect of this sprite.
        self.image = self.motions_table[Orient.DOWN][0]

        xs, ys = cs.compute_pixel_coords(x, y)
        self.rect = self.image.get_rect(x=xs, y=ys)

    def animate(self, dt, walk):
        self.index += self.animation_speed * dt
        images = self.motions_table[walk]

        if self.index >= len(images):
            self.index = 0

        self.image = images[int(self.index)]

    def check_obstacle(self,
                       move_by: pygame.math.Vector2,
                       obstacle_group) -> pygame.math.Vector2:

        # tentative player position.
        tentative = player_group.sprite.rect.move(move_by)

        for obstacle in obstacle_group:
            if tentative.colliderect(obstacle.rect):
                return pygame.math.Vector2(0, 0)

        return move_by

    def update(self, dt, obstacle_group):
        velocity = pygame.math.Vector2(0, 0)

        keys = pygame.key.get_pressed()
        walk = None

        if keys[pygame.K_UP]:
            velocity.y -= 1
            walk = Orient.UP
        elif keys[pygame.K_DOWN]:
            velocity.y += 1
            walk = Orient.DOWN
        elif keys[pygame.K_LEFT]:
            velocity.x -= 1
            walk = Orient.LEFT
        elif keys[pygame.K_RIGHT]:
            velocity.x += 1
            walk = Orient.RIGHT

        displacement = self.check_obstacle(velocity * self.speed * dt,
                                           obstacle_group)

        if displacement != pygame.math.Vector2(0, 0):
            self.rect.move_ip(displacement)
            self.animate(dt, walk)


class Fixture(pygame.sprite.Sprite):
    """A class for describing a sprite not directly involved in
    gameplay. For example, they never move. Such a sprite may or may
    not be collidable, but let the groups handle that.

    """

    def __init__(self, x: int, y: int, image: pygame.Surface):
        super().__init__()

        self.image = image

        xs, ys = cs.compute_pixel_coords(x, y)
        self.rect = self.image.get_rect(x=xs, y=ys)


pygame.init()

grid = maze.Grid(cs.GRID_X, cs.GRID_Y)
grid.carve()

screen_dimensions = cs.compute_pixel_coords(cs.NUM_TILES_X, cs.NUM_TILES_Y)
screen = pygame.display.set_mode(screen_dimensions)
sheet = Spritesheet("../graphics/spritesheet.png")

player = MovingThing(1, 1, **{
    "down": sheet.get_all([TileDef.PLAYER_DOWN_1, TileDef.PLAYER_DOWN_2]),
    "up": sheet.get_all([TileDef.PLAYER_UP_1, TileDef.PLAYER_UP_2]),
    "left": sheet.get_all([TileDef.PLAYER_LEFT_1, TileDef.PLAYER_LEFT_2]),
    "right": sheet.get_all([TileDef.PLAYER_RIGHT_1, TileDef.PLAYER_RIGHT_2])
})


player_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
player_group.add(player)

pillar_group: pygame.sprite.Group = pygame.sprite.Group()
floor_group: pygame.sprite.Group = pygame.sprite.Group()
crawler_group: pygame.sprite.Group = pygame.sprite.Group()

# Use a set, so that we can remove duplicates (we don't add a pillar
# twice to a given board position.)
all_projections = set()

for x in range(cs.GRID_X):
    for y in range(cs.GRID_Y):
        projection = maze.compute_cell_projection(grid, x, y)

        for p in projection:
            all_projections.add(p)

for x, y in all_projections:
    pillar = Fixture(x, y, sheet.get(TileDef.PILLAR))
    pillar_group.add(pillar)


# Add the floor graphics.
for x in range(cs.NUM_TILES_X):
    for y in range(cs.NUM_TILES_Y):
        if (x, y) not in all_projections:
            floor = Fixture(x, y, sheet.get(TileDef.FLOOR))
            floor_group.add(floor)


# Add the crawlers.
crawler = MovingThing(2, 2, **{
    "down": sheet.get_all([TileDef.CRAWLER_DOWN_1, TileDef.CRAWLER_DOWN_2]),
    "up": sheet.get_all([TileDef.CRAWLER_UP_1, TileDef.CRAWLER_UP_2]),
    "left": sheet.get_all([TileDef.CRAWLER_LEFT_1, TileDef.CRAWLER_LEFT_2]),
    "right": sheet.get_all([TileDef.CRAWLER_RIGHT_1, TileDef.CRAWLER_RIGHT_2])
})


def get_next_crawler_move(crawler: MovingThing) -> Point:
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

        player_group.update(dt, pillar_group)
        pygame.display.flip()

        dt = clock.tick(60) / 1000


mainloop()
pygame.quit()
