# Colors definined as RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (252, 244, 3)
PURPLE = (252, 3, 240)
BROWN = (128, 87, 0)
ORANGE = (252, 173, 3)

def to_bgr_from_rgb(color):
    return (color[2], color[1], color[0])