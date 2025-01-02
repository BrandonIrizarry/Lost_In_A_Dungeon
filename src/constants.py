TILE_LEN = 16
NUM_UNITS = 36
SCREEN_LEN = NUM_UNITS * TILE_LEN
NUM_TILES = 18
SCALE_FACTOR = NUM_UNITS // NUM_TILES


def compute_index(index: int) -> int:
    return index * TILE_LEN * SCALE_FACTOR


def compute_coords(x: int, y: int) -> tuple[int, int]:
    """Return x and y, appropriately scaled."""
    xs = x * TILE_LEN * SCALE_FACTOR
    ys = y * TILE_LEN * SCALE_FACTOR

    return xs, ys
