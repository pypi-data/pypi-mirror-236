# Source: https://github.com/enkia/tokyo-night-vscode-theme

from ..base import ColorPalette, Color

BACKGROUND = Color(
    "background",
    (36, 40, 59),
    "#24283B",
    (229, 24, 18)
)

BLACK = Color(
    "black",
    (65, 72, 104),
    "#414868",
    (229, 23, 33),
)

GRAY_A = Color(
    "gray_a",
    (192, 202, 245),
    "#C0CAF5",
    (229, 73, 86),
)

GRAY_B = Color(
    "gray_b",
    (169, 177, 214),
    "#A9B1D6",
    (229, 35, 75)
)

GRAY_C = Color(
    "gray_c",
    (154, 165, 206),
    "#9AA5CE",
    (227, 34, 70)
)

GRAY_D = Color(
    "gray_d",
    (207, 201, 194),
    "#CFC9C2",
    (32, 11, 78)
)

RED = Color(
    "red",
    (247, 118, 142),
    "#F7768E",
    (348, 88, 71)
)

ORANGE = Color(
    "orange",
    (255, 158, 100),
    "#FF9E64",
    (22, 100, 69)
)

YELLOW = Color(
    "yellow",
    (224, 175, 104),
    "#E0AF68",
    (35, 65, 64)
)

GREEN = Color(
    "green",
    (158, 206, 106),
    "#9ECE6A",
    (88, 50, 61)
)

TEAL = Color(
    "teal",
    (115, 218, 202),
    "#73DACA",
    (170, 58, 65)
)

BLUE_A = Color(
    "blue_a",
    (180, 249, 248),
    "#B4F9F8",
    (179, 85, 84)
)

BLUE_B = Color(
    "blue_b",
    (42, 195, 222),
    "#2AC3DE",
    (189, 73, 51)
)

BLUE_C = Color(
    "blue_c",
    (125, 207, 255),
    "#7DCFFF",
    (202, 100, 74)
)

BLUE_D = Color(
    "blue_d",
    (122, 162, 247),
    "#7AA2F7",
    (220, 88, 72)
)

PURPLE = Color(
    "purple",
    (187, 154, 247),
    "#BB9AF7",
    (261, 85, 78)
)


TokyoNightStorm = ColorPalette(
    name="Tokyo Night Storm",
    colors_list=[
        BACKGROUND,
        BLACK,
        GRAY_A,
        GRAY_B,
        GRAY_C,
        GRAY_D,
        RED,
        ORANGE,
        YELLOW,
        GREEN,
        TEAL,
        BLUE_A,
        BLUE_B,
        BLUE_C,
        BLUE_D,
        PURPLE
    ]
)