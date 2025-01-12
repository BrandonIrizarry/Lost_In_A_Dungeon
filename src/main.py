import pygame
import random
import constants as cs
from tiledef import TileDef
from typedefs import Point
from spritesheet import Spritesheet
import maze
from pygame.math import Vector2
import abc
from enum import Enum, auto
import os


class CollisionType(Enum):
    """Define a collision type based on the kind of action or result
    meant to take place.

    """
    TAKE_DAMAGE = auto(),
    DO_DAMAGE = auto(),
    BLOCK = auto(),
    WIN = auto()


class Direction(Enum):
    """An enum for using vectors as hashmap keys."""
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)


class Moving(pygame.sprite.Sprite, abc.ABC):
    """Parent class of player and crawler sprites."""

    def __init__(self, x: int, y: int, **animations):
        pygame.sprite.Sprite.__init__(self)

        self.motions_table = {
            Direction.DOWN: [animations["down"][0], animations["down"][1]],
            Direction.UP: [animations["up"][0], animations["up"][1]],
            Direction.LEFT: [animations["left"][0], animations["left"][1]],
            Direction.RIGHT: [animations["right"][0], animations["right"][1]]
        }

        self.animation_speed = 5
        self.animation_index = 0
        self.speed = 200
        self.direction = Direction.DOWN

        # Define the image and rect of this sprite.
        self.image = self.motions_table[self.direction][0]

        xs, ys = cs.compute_pixel_coords(x, y)
        self.rect: pygame.Rect = self.image.get_rect(x=xs, y=ys)
        self.rect = self.rect.inflate(-5.0, -5.0)

    @classmethod
    def spawn(cls, x, y):
        """Spawn an instance of this class."""
        moving = cls(x, y)
        cls.group.add(moving)

    @classmethod
    def kill(cls, sprite):
        """Remove an instance of this class from play."""
        cls.group.remove(sprite)

    def animate(self, dt):
        """Update the image used to display the sprite, based on the
        current direction the sprite is facing.

        The current direction is stored in 'self.direction'.

        """

        images = self.motions_table[self.direction]

        self.animation_index += self.animation_speed * dt

        if self.animation_index >= len(images):
            self.animation_index = 0

        self.image = images[int(self.animation_index)]

    def check_block(self,
                    move_by: Vector2,
                    groups: list[pygame.sprite.Group]) -> Vector2:
        """Return displacement, or zero-vector if an obstacle is
        encountered.

        """

        tentative_pos = self.rect.move(move_by)

        for group in groups:
            for obstacle in group:
                collided = tentative_pos.colliderect(obstacle.rect)

                # Make sure that a given sprite can't "collide" with
                # itself.
                if obstacle.rect != self.rect and collided:
                    return Vector2(0, 0)

        return move_by

    def check_take_damage(self,
                          move_by: Vector2,
                          groups: list[pygame.sprite.Group]):
        """Check whether this sprite initiated
        a collision with a deadly sprite.

        """

        tentative = self.rect.move(move_by)

        for group in groups:
            for sprite in group:
                collided = tentative.colliderect(sprite.rect)

                if collided:
                    self.__class__.kill(self)
                    break

    @abc.abstractmethod
    def update(self, dt, collision_type: dict[CollisionType,
                                              list[pygame.sprite.Group]]):
        """This sprite's 'update' method, to be overridden by child
        classes.

        """
        pass


class Fixture(pygame.sprite.Sprite):
    """A sprite that doesn't move of its own accord.

    It only consists of an image and a rect, and has no update method.

    Such a sprite may or may not be collidable, according to its
    group.

    """

    def __init__(self, x: int, y: int, image: pygame.Surface):
        super().__init__()

        self.image = image

        xs, ys = cs.compute_pixel_coords(x, y)
        self.rect = self.image.get_rect(x=xs, y=ys)


class Pillar(Fixture):
    group: pygame.sprite.Group = pygame.sprite.Group()

    def __init__(self, x: int, y: int):
        super().__init__(x, y, sheet.get(TileDef.PILLAR))

    @classmethod
    def spawn_tiles(cls, occupied_positions: set[Point]):
        """Define pillar positions in the level."""

        for x in range(cs.GRID_X):
            for y in range(cs.GRID_Y):
                pos = maze.compute_pillar_position(grid, x, y)

                for p in pos:
                    occupied_positions.add(p)

            for x, y in occupied_positions:
                pillar = cls(x, y)
                cls.group.add(pillar)


class Floor(Fixture):
    group: pygame.sprite.Group = pygame.sprite.Group()

    def __init__(self, x: int, y: int):
        super().__init__(x, y, sheet.get(TileDef.FLOOR))

    @classmethod
    def spawn_tiles(cls, occupied_positions: set[Point]):
        """Define floor tile positions in the level."""

        for x in range(cs.NUM_TILES_X):
            for y in range(cs.NUM_TILES_Y):
                if (x, y) not in occupied_positions:
                    floor = cls(x, y)
                    cls.group.add(floor)


class StairsUp(Fixture):
    group: pygame.sprite.Group = pygame.sprite.Group()

    def __init__(self, x: int, y: int):
        super().__init__(x, y, sheet.get(TileDef.STAIRS_UP))
        self.__class__.group.add(self)


class Sword(pygame.sprite.Sprite):
    """Allow pixel-level positioning."""

    def __init__(self, x: int, y: int, image: pygame.Surface):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(x=x, y=y)


class Player(Moving):
    """The player, controllable by the user via the keyboard."""

    group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
    sword_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()

    def __init__(self, x: int, y: int):
        animations = {
            "down": sheet.get_all([TileDef.PLAYER_DOWN_1,
                                   TileDef.PLAYER_DOWN_2]),
            "up": sheet.get_all([TileDef.PLAYER_UP_1,
                                 TileDef.PLAYER_UP_2]),
            "left": sheet.get_all([TileDef.PLAYER_LEFT_1,
                                   TileDef.PLAYER_LEFT_2]),
            "right": sheet.get_all([TileDef.PLAYER_RIGHT_1,
                                    TileDef.PLAYER_RIGHT_2])
         }

        super().__init__(x, y, **animations)

        self.cooldown = 0.2
        self.timer = 0.0
        self.won = False

    def get_sword(self):
        """Get the sword sprite."""
        tile_def = None

        match self.direction:
            case Direction.UP:
                tile_def = TileDef.SWORD_UP
            case Direction.DOWN:
                tile_def = TileDef.SWORD_DOWN
            case Direction.LEFT:
                tile_def = TileDef.SWORD_LEFT
            case Direction.RIGHT:
                tile_def = TileDef.SWORD_RIGHT

        cv = Vector2(self.rect.x, self.rect.y)
        cv = cv + self.direction.value * cs.LEVEL_FACTOR

        return Sword(cv.x, cv.y, sheet.get(tile_def))

    def check_win(self,
                  move_by: Vector2,
                  groups: list[pygame.sprite.Group]):
        """Check whether the player wins."""

        tentative = self.rect.move(move_by)

        for group in groups:
            for sprite in group:
                collided = tentative.colliderect(sprite.rect)

                if collided:
                    self.won = True
                    break

    def update(self, dt, coltype: dict[CollisionType,
                                       list[pygame.sprite.Group]]):
        """The Player's 'update' override, largely based on the user's
        keyboard input.

        """

        self.timer -= dt

        if self.timer > 0:
            return

        # Remove the sword from gameplay.
        self.sword_group.empty()

        delta = Vector2(0, 0)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            delta.y = -1
        elif keys[pygame.K_s]:
            delta.y = 1
        elif keys[pygame.K_a]:
            delta.x = -1
        elif keys[pygame.K_d]:
            delta.x = 1
        elif keys[pygame.K_k]:
            sword = self.get_sword()
            self.sword_group.add(sword)
            self.timer = self.cooldown

        proposed_disp = delta * self.speed * dt
        actual_disp = self.check_block(proposed_disp,
                                       coltype[CollisionType.BLOCK])

        self.check_take_damage(proposed_disp,
                               coltype[CollisionType.TAKE_DAMAGE])

        self.check_win(proposed_disp,
                       coltype[CollisionType.WIN])

        # The displacement could be the zero vector, either because
        # (dx, dy) is the zero tuple (because the user didn't press a
        # key to move the player), or because the player encountered
        # an obstacle blocking its path.
        if actual_disp != Vector2(0, 0):
            self.rect.move_ip(actual_disp)
            self.animate(dt)

        # Update the player's direction.
        if delta != Vector2(0, 0):
            match delta:
                case Vector2(x=0, y=-1):
                    self.direction = Direction.UP
                case Vector2(x=0, y=1):
                    self.direction = Direction.DOWN
                case Vector2(x=-1, y=0):
                    self.direction = Direction.LEFT
                case Vector2(x=1, y=0):
                    self.direction = Direction.RIGHT
                case _:
                    raise Exception(f"Invalid delta: {delta}")


class Crawler(Moving):
    """A subclass of MovingThing applicable to crawlers.

    The only difference is in the implementation of 'update'.

    """

    group: pygame.sprite.Group = pygame.sprite.Group()

    def __init__(self, x: int, y: int):
        animations = {
            "down": sheet.get_all([TileDef.CRAWLER_DOWN_1,
                                   TileDef.CRAWLER_DOWN_2]),
            "up": sheet.get_all([TileDef.CRAWLER_UP_1,
                                 TileDef.CRAWLER_UP_2]),
            "left": sheet.get_all([TileDef.CRAWLER_LEFT_1,
                                   TileDef.CRAWLER_LEFT_2]),
            "right": sheet.get_all([TileDef.CRAWLER_RIGHT_1,
                                    TileDef.CRAWLER_RIGHT_2])
        }

        super().__init__(x, y, **animations)

        # Tweaks for this particular sprite.
        self.cooldown = 1.0
        self.timer = self.cooldown
        self.speed = 100

    @classmethod
    def spawn_crawlers(cls, occupied_positions: set[Point]):
        """Define initial crawler positions in the level.

        The Crawler class manages its own group.

        """

        for x in range(2, cs.NUM_TILES_X):
            for y in range(2, cs.NUM_TILES_Y):
                if (x, y) not in occupied_positions:
                    if random.random() <= 1/20:
                        Crawler.spawn(x, y)

    def update(self, dt, coltype: dict[CollisionType,
                                       list[pygame.sprite.Group]]):
        self.timer -= dt

        if self.timer <= 0:
            self.direction = random.choice([Direction.UP,
                                            Direction.DOWN,
                                            Direction.LEFT,
                                            Direction.RIGHT])
            self.timer = self.cooldown

        proposed_disp = self.direction.value * self.speed * dt
        actual_disp = self.check_block(proposed_disp,
                                       coltype[CollisionType.BLOCK])

        self.check_take_damage(proposed_disp,
                               coltype[CollisionType.TAKE_DAMAGE])

        # The displacement could be the zero vector, either because
        # (dx, dy) is the zero tuple (because the user didn't press a
        # key to move the player), or because the player encountered
        # an obstacle blocking its path.
        if actual_disp != Vector2(0, 0):
            self.rect.move_ip(actual_disp)
            self.animate(dt)
        else:
            self.timer = 0


def mainloop() -> None:
    """The main pygame loop.

    The loop is encapsulated inside this function so that we can easily
    quit the game with a 'return' statement.

    """
    clock = pygame.time.Clock()
    dt = 0.0

    # Use a set, so that we can remove duplicates (we don't add a pillar
    # twice to a given board position.)
    occupied_positions: set[Point] = set()

    Pillar.spawn_tiles(occupied_positions)
    Floor.spawn_tiles(occupied_positions)
    Crawler.spawn_crawlers(occupied_positions)
    Player.spawn(1, 1)
    StairsUp(cs.NUM_TILES_X - 2, cs.NUM_TILES_Y - 2)

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

        Pillar.group.draw(screen)
        Floor.group.draw(screen)
        Player.group.draw(screen)
        Crawler.group.draw(screen)
        Player.sword_group.draw(screen)
        StairsUp.group.draw(screen)

        Player.group.update(dt, {
            CollisionType.BLOCK: [Pillar.group],
            CollisionType.TAKE_DAMAGE: [Crawler.group],
            CollisionType.WIN: [StairsUp.group]
        })

        Crawler.group.update(dt, {
            CollisionType.BLOCK: [Crawler.group, Pillar.group],
            CollisionType.TAKE_DAMAGE: [Player.sword_group],
        })

        if Player.group.sprite is None:
            print("You died!")
            return

        if Player.group.sprite.won:
            print("You won!")
            return

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    pygame.init()
    cs.configure_scale_factor(2)

    screen_dimensions = cs.compute_pixel_coords(cs.NUM_TILES_X, cs.NUM_TILES_Y)
    screen = pygame.display.set_mode(screen_dimensions)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    sheet = Spritesheet(f"{dir_path}/../graphics/spritesheet.png")

    grid = maze.Grid(cs.GRID_X, cs.GRID_Y)
    grid.carve()

    mainloop()
    pygame.quit()
