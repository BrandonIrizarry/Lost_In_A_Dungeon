from enum import Flag, auto
import random


class Cell(Flag):
    """Represent a cell in a maze in terms of which of its directions
    are open for traversal.

    Note that a cell is visited in a maze construction if and only if
    its value isn't zero (i.e, Cell(0)).

    """
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def unvisited(self) -> bool:
        return self == Cell(0)

    def visited(self) -> bool:
        return not self.unvisited()


type Point = tuple[int, int]


def get_neighbors(x, y, xmax, ymax) -> list[Point]:
    """Return the list of taxicab neighbors of the given point, with
    bounds checking.

    """

    neighbors: list[Point] = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            # Exactly one of these has to be 0 for taxicab adjacency.
            if (dx == 0) ^ (dy == 0):
                new_x = x + dx
                new_y = y + dy

                x_valid = new_x in range(xmax)
                y_valid = new_y in range(ymax)

                if x_valid and y_valid:
                    neighbors.append((new_x, new_y))

    return neighbors


class Grid:
    def __init__(self, width, height):
        self.grid = []
        self.width = width
        self.height = height

        for i in range(width):
            self.grid.append([])

            for j in range(height):
                self.grid[-1].append(Cell(0))

    def not_yet_visited(self, point: Point):
        """Return True iff the given grid point has not yet been visited."""
        x, y = point

        return self.grid[x][y] == Cell(0)

    def get_random_point(self) -> Point:
        """Return a random pair of coordinates from within the grid.

        """

        x_start = random.randrange(self.width)
        y_start = random.randrange(self.height)

        return x_start, y_start

    def tour(self, x_start, y_start) -> None:
        """Attempt to perform a random walk around 'grid', until all paths
        forward lead either to a visited cell, or would take us
        out-of-bounds.

        """

        # Initialize x and y for the following loop.
        x = x_start
        y = y_start

        while True:
            neighbors: list[Point] = get_neighbors(x,
                                                   y,
                                                   self.width,
                                                   self.height)

            neighbors = list(filter(self.not_yet_visited, neighbors))

            if neighbors == []:
                return
            else:
                # Choose a neighbor at random.
                new_x, new_y = random.choice(neighbors)

                if new_x < x:
                    self.grid[x][y] |= Cell.LEFT
                    self.grid[new_x][new_y] |= Cell.RIGHT
                elif new_x > x:
                    self.grid[x][y] |= Cell.RIGHT
                    self.grid[new_x][new_y] |= Cell.LEFT

                if new_y < y:
                    self.grid[x][y] |= Cell.UP
                    self.grid[new_x][new_y] |= Cell.DOWN
                elif new_y > y:
                    self.grid[x][y] |= Cell.DOWN
                    self.grid[new_x][new_y] |= Cell.UP

                x, y = new_x, new_y

    def scan(self) -> Point | None:
        """Find the first Point p such that:

        1. The grid cell there is unvisited.
        2. The grid cell is adjacent to a visited cell."""
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].unvisited():
                    for n in get_neighbors(x, y, self.width, self.height):
                        xn, yn = n

                        if self.grid[xn][yn].visited():
                            return xn, yn

        return None

    def carve(self) -> None:
        """Carve the maze path inside this grid.

        This is the public, top-level method of this class."""

        x, y = self.get_random_point()

        while True:
            self.tour(x, y)
            point = self.scan()

            if point is None:
                break

            x, y = point

    def __repr__(self):
        """Return a string representation of the grid.

        The ith column of the grid corresponds to the ith row of the
        representation.

        """
        buffer = []

        for i in range(self.height):
            subbuffer = []

            for j in range(self.width):
                cell = self.grid[j][i]

                subbuffer.append(str(cell))

            buffer.append(" ".join(subbuffer))

        return "\n".join(buffer)


grid = Grid(5, 5)

grid.carve()

print(grid)
