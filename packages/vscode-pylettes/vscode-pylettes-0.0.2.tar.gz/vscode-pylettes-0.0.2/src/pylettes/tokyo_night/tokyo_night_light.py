# Source: https://github.com/enkia/tokyo-night-vscode-theme

from ..base import ColorPalette, Color

BACKGROUND = Color(
    "background",
    (140, 67, 81),
    "#8C4351",
    (348, 35, 40)
)

GRAY = Color(
    "gray",
    (150, 153, 163),
    "#9699A3",
    (226, 6, 61)
)

BLACK = Color(
    "black",
    (15, 15, 20),
    "#0F0F14",
    (240, 14, 6)
)

COFFEE = Color(
    "coffee",
    (99, 79, 48),
    "#634F30",
    (36, 34, 28)
)

CORAL_BLACK = Color(
    "coral_black",
    (86, 90, 110),
    "#565A6E",
    (229, 12, 38)
)

CHARCOAL = Color(
    "charcoal",
    (52, 59, 88),
    "#343B58",
    (228, 25, 27)
)

PURPLE = Color(
    "purple",
    (90, 74, 120),
    "#5A4A78",
    (260, 23, 38)
)

DARK_BLUE = Color(
    "dark_blue",
    (52, 84, 138),
    "#34548A",
    (217, 45, 37)
)

DARK_TEAL = Color(
    "dark_teal",
    (15, 75, 110),
    "#0F4B6E",
    (202, 76, 24)
)

TEAL = Color(
    "teal",
    (22, 103, 117),
    "#166775",
    (188, 68, 27)
)

DARK_GREEN = Color(
    "dark_green",
    (51, 99, 92),
    "#33635C",
    (171, 32, 29)
)

GREEN = Color(
    "green",
    (72, 94, 48),
    "#485E30",
    (88, 32, 27)
)

BROWN = Color(
    "brown",
    (143, 94, 21),
    "#8F5E15",
    (35, 74, 32)
)

ORANGE = Color(
    "orange",
    (150, 80, 39),
    "#965027",
    (22, 58, 37)
)

RED = Color(
    "red",
    (140, 67, 81),
    "#8C4351",
    (348, 35, 40)
)

TokyoNightLight = ColorPalette(
    name="Tokyo Night Light",
    colors_list=[
        BACKGROUND,
        GRAY,
        BLACK,
        COFFEE,
        CORAL_BLACK,
        CHARCOAL,
        PURPLE,
        DARK_BLUE,
        DARK_TEAL,
        TEAL,
        DARK_GREEN,
        GREEN,
        BROWN,
        ORANGE,
        RED
    ]
)