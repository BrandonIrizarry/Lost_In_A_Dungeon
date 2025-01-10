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


class CollisionType(Enum):
    """Define a collision type based on the kind of action or result
    meant to take place.

    """
    TAKE_DAMAGE = auto(),
    DO_DAMAGE = auto(),
    BLOCK = auto()


class Moving(pygame.sprite.Sprite, abc.ABC):
    """Parent class of player and crawler sprites."""

    def __init__(self, x: int, y: int, **animations):
        pygame.sprite.Sprite.__init__(self)

        self.motions_table = {
            cs.DOWN: [animations["down"][0], animations["down"][1]],
            cs.UP: [animations["up"][0], animations["up"][1]],
            cs.LEFT: [animations["left"][0], animations["left"][1]],
            cs.RIGHT: [animations["right"][0], animations["right"][1]]
        }

        self.animation_speed = 5
        self.animation_index = 0
        self.speed = 200
        self.direction = cs.DOWN

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

    def get_sword(self, x, y):
        """Get the sword sprite."""
        tile_def = None

        match self.direction:
            case cs.UP:
                tile_def = TileDef.SWORD_UP
            case cs.DOWN:
                tile_def = TileDef.SWORD_DOWN
            case cs.LEFT:
                tile_def = TileDef.SWORD_LEFT
            case cs.RIGHT:
                tile_def = TileDef.SWORD_RIGHT

        return Fixture(x, y, sheet.get(tile_def))

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

        dx, dy = 0, 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_s]:
            dy = 1
        elif keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_d]:
            dx = 1
        elif keys[pygame.K_k]:
            sx, sy = cs.compute_grid_coords(self.rect.centerx,
                                            self.rect.centery)
            sword = self.get_sword(sx + self.direction[0] * 0.5,
                                   sy + self.direction[1] * 0.5)
            self.sword_group.add(sword)
            self.timer = self.cooldown

        proposed_disp = Vector2(dx, dy) * self.speed * dt
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

        # Update the player's direction.
        if dx != 0 or dy != 0:
            self.direction = (dx, dy)


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

    def update(self, dt, coltype: dict[CollisionType,
                                       list[pygame.sprite.Group]]):
        self.timer -= dt

        if self.timer <= 0:
            self.direction = random.choice([cs.UP,
                                            cs.DOWN,
                                            cs.LEFT,
                                            cs.RIGHT])
            self.timer = self.cooldown

        dx, dy = self.direction

        proposed_disp = Vector2(dx, dy) * self.speed * dt
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


class LevelDefinition:
    def __init__(self, sheet: Spritesheet):
        # Use a set, so that we can remove duplicates (we don't add a pillar
        # twice to a given board position.)
        self.pillar_positions: set[Point] = set()
        self.sheet = sheet

    def define_pillar_tiles(self) -> pygame.sprite.Group:
        """Define pillar positions in the level."""

        pillar_group: pygame.sprite.Group = pygame.sprite.Group()

        for x in range(cs.GRID_X):
            for y in range(cs.GRID_Y):
                pos = maze.compute_pillar_position(grid, x, y)

                for p in pos:
                    self.pillar_positions.add(p)

            for x, y in self.pillar_positions:
                pillar = Fixture(x, y, self.sheet.get(TileDef.PILLAR))
                pillar_group.add(pillar)

        return pillar_group

    def define_floor_tiles(self) -> pygame.sprite.Group:
        """Define floor tile positions in the level."""

        floor_group: pygame.sprite.Group = pygame.sprite.Group()

        for x in range(cs.NUM_TILES_X):
            for y in range(cs.NUM_TILES_Y):
                if (x, y) not in self.pillar_positions:
                    floor = Fixture(x, y, self.sheet.get(TileDef.FLOOR))
                    floor_group.add(floor)

        return floor_group

    def define_crawlers(self):
        """Define initial crawler positions in the level."""

        for x in range(cs.NUM_TILES_X):
            for y in range(cs.NUM_TILES_Y):
                if (x, y) not in self.pillar_positions:
                    if random.random() <= 1/100:
                        Crawler.spawn(x, y)

    def define_player(self) -> pygame.sprite.GroupSingle:
        """Define the initial player position."""

        player_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()

        player = Player(1, 1)
        player_group.add(player)

        return player_group


pygame.init()
screen_dimensions = cs.compute_pixel_coords(cs.NUM_TILES_X, cs.NUM_TILES_Y)
screen = pygame.display.set_mode(screen_dimensions)
sheet = Spritesheet("../graphics/spritesheet.png")

grid = maze.Grid(cs.GRID_X, cs.GRID_Y)
grid.carve()


def mainloop():
    """The main pygame loop.

    The loop is encapsulated inside this function so that we can easily
    quit the game with a 'return' statement.

    """
    clock = pygame.time.Clock()
    dt = 0

    level = LevelDefinition(sheet)
    pillar_group = level.define_pillar_tiles()
    floor_group = level.define_floor_tiles()
    crawler_group = Crawler.group
    player_group = Player.group
    sword_group = Player.sword_group

    Player.spawn(1, 1)
    level.define_crawlers()

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
        sword_group.draw(screen)

        player_group.update(dt, {
            CollisionType.BLOCK: [pillar_group],
            CollisionType.TAKE_DAMAGE: [crawler_group],
        })

        crawler_group.update(dt, {
            CollisionType.BLOCK: [crawler_group, pillar_group],
            CollisionType.TAKE_DAMAGE: [sword_group],
        })

        if player_group.sprites() == []:
            return

        pygame.display.flip()

        dt = clock.tick(60) / 1000


mainloop()
pygame.quit()
