TILE_LEN = 16
SCALE_FACTOR = 1
GRID_X = 10
GRID_Y = 10
NUM_TILES_X = 3 * GRID_X + 1
NUM_TILES_Y = 3 * GRID_Y + 1
LEVEL_FACTOR = TILE_LEN * SCALE_FACTOR


def configure_scale_factor(scale_factor: int = 1):
    """Configure SCALE_FACTOR from the outside.

    This also accordingly reconfigures LEVEL_FACTOR."""

    global SCALE_FACTOR, LEVEL_FACTOR

    SCALE_FACTOR = scale_factor
    LEVEL_FACTOR = TILE_LEN * SCALE_FACTOR


def compute_pixel_coords(x_grid: int, y_grid: int) -> tuple[int, int]:
    """Return inputs scaled to pixel units, appropriate for display on
    the pygame screen."""

    xs = x_grid * LEVEL_FACTOR
    ys = y_grid * LEVEL_FACTOR

    return xs, ys


def compute_grid_coords(x_pixel: int, y_pixel: int) -> tuple[int, int]:
    """Return inputs scaled to grid units, appropriate for handling
    sprite logic."""

    xs = x_pixel // LEVEL_FACTOR
    ys = y_pixel // LEVEL_FACTOR

    return xs, ys
