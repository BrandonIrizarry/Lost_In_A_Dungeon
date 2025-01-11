TILE_LEN = 16
SCALE_FACTOR = 2
GRID_X = 10
GRID_Y = 10
NUM_TILES_X = 3 * GRID_X + 1
NUM_TILES_Y = 3 * GRID_Y + 1
GRID_FACTOR = TILE_LEN * SCALE_FACTOR


def compute_pixel_coords(x_grid: int, y_grid: int) -> tuple[int, int]:
    """Return inputs scaled to pixel units, appropriate for display on
    the pygame screen."""

    xs = x_grid * GRID_FACTOR
    ys = y_grid * GRID_FACTOR

    return xs, ys


def compute_grid_coords(x_pixel: int, y_pixel: int) -> tuple[int, int]:
    """Return inputs scaled to grid units, appropriate for handling
    sprite logic."""

    xs = x_pixel // GRID_FACTOR
    ys = y_pixel // GRID_FACTOR

    return xs, ys
