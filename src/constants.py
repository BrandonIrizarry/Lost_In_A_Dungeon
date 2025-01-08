TILE_LEN = 16
SCALE_FACTOR = 2
GRID_X = 10
GRID_Y = 10
NUM_TILES_X = 3 * GRID_X + 1
NUM_TILES_Y = 3 * GRID_Y + 1


# Constants related to unit displacement.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def compute_pixel_coords(x_grid: int, y_grid: int) -> tuple[int, int]:
    """Return inputs scaled to pixel units, appropriate for display on
    the pygame screen."""

    xs = x_grid * TILE_LEN * SCALE_FACTOR
    ys = y_grid * TILE_LEN * SCALE_FACTOR

    return xs, ys


def compute_grid_coords(x_pixel: int, y_pixel: int) -> tuple[int, int]:
    """Return inputs scaled to grid units, appropriate for handling
    sprite logic."""

    xs = x_pixel // (TILE_LEN * SCALE_FACTOR)
    ys = y_pixel // (TILE_LEN * SCALE_FACTOR)

    return xs, ys
