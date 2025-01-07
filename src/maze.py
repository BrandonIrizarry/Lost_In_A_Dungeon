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

    def tour(self) -> None:
        """Attempt to perform a random walk around 'grid', until all paths
        forward lead either to a visited cell, or would take us
        out-of-bounds.

        """
        start_x = random.randrange(self.width)
        start_y = random.randrange(self.height)

        # Initialize x and y for the following loop.
        x = start_x
        y = start_y

        while True:
            neighbors: list[Point] = get_neighbors(x, y, self.width, self.height)
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


    def __repr__(self):
        """Return a string representation of the grid.

        The ith column of the grid corresponds to the ith row of the
        representation.

        """
        buffer = []

        for column in self.grid:
            subbuffer = []

            for cell in column:
                subbuffer.append(str(cell))

            buffer.append(" ".join(subbuffer))

        return "\n".join(buffer)


grid = Grid(10, 10)

grid.tour()

print(grid)
