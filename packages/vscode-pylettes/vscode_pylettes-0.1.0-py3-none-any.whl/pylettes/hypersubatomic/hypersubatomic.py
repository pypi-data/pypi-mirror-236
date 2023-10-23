# Source: https://marketplace.visualstudio.com/items?itemName=neilpanchal.hypersubatomic

from ..base import ColorPalette, Color

BACKGROUND = Color(
    "background",
    (15, 17, 26),
    "#0F111A",
    (229, 26, 8)
)

GREEN = Color(
    "green",
    (0, 174, 107),
    "#00AE6B",
    (156, 100, 34)
)

RED = Color(
    "red",
    (242, 40, 60),
    "#F2283C",
    (354, 88, 55)
)

BLUE = Color(
    "blue",
    (39, 125, 255),
    "#277DFF",
    (216, 99, 57)
)

YELLOW = Color(
    "yellow",
    (255, 194, 0),
    "#FFC200",
    (45, 100, 50)
)

PINK = Color(
    "pink",
    (215, 46, 130),
    "#D72E82",
    (330, 67, 51)
)

PURPLE = Color(
    "purple",
    (135, 90, 251),
    "#875AFB",
    (256, 95, 66)
)

ORANGE = Color(
    "orange",
    (255, 122, 0),
    "#FF7A00",
    (28, 100, 50)
)

Hypersubatomic = ColorPalette(
    name="Hypersubatomic",
    colors_list=[
        BACKGROUND,
        GREEN,
        RED,
        BLUE,
        YELLOW,
        PINK,
        PURPLE,
        ORANGE
    ]
)