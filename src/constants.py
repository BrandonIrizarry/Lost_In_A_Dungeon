TILE_LEN = 16
NUM_UNITS = 36
SCREEN_LEN = NUM_UNITS * TILE_LEN
NUM_TILES = 18
SCALE_FACTOR = NUM_UNITS // NUM_TILES


def compute_index(index: int) -> int:
    return index * TILE_LEN * SCALE_FACTOR


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
