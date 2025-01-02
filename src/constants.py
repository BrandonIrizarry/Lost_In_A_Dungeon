TILE_LEN = 16
NUM_UNITS = 36
SCREEN_LEN = NUM_UNITS * TILE_LEN
NUM_TILES = 18
SCALE_FACTOR = NUM_UNITS // NUM_TILES


def compute_index(index: int) -> int:
    return index * TILE_LEN * SCALE_FACTOR
