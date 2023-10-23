# Source: https://github.com/joshdick/onedark.vim

from ..base import ColorPalette, Color

BLACK = Color(
    "black",
    (40, 44, 51),
    "#282C33",
    (218.18, 12.09, 17.84)
)

BACKGROUND = Color(
    "background",
    (40, 44, 51),
    "#282C33",
    (218.18, 12.09, 17.84)
)

RED = Color(
    "red",
    (224, 107, 116),
    "#E06B74",
    (355.38, 65.36, 64.9),
)

GREEN = Color(
    "green",
    (152, 195, 121),
    "#98C379",
    (94.86, 38.14, 61.96),
)

YELLOW = Color(
    "yellow",
    (229, 192, 112),
    "#E5C07A",
    (39.25, 67.3, 68.82),
)

BLUE = Color(
    "blue",
    (98, 174, 239),
    "#62AEEf",
    (98, 174, 239),
)


PURPLE = Color(
    "purple",
    (198, 120, 221),
    "#C678DD",
    (286.34, 59.76, 66.86),
)

TEAL = Color(
    "teal",
    (85, 182, 194),
    "#55B6C2",
    (186.61, 47.19, 54.71),
)

GRAY = Color(
    "gray",
    (171, 178, 191),
    "#ABB2BF",
    (219, 13.51, 70.98),
)
OneDark = ColorPalette(
    name="One Dark",
    colors_list=[
        BACKGROUND,
        BLACK,
        RED,
        GREEN,
        YELLOW,
        BLUE,
        PURPLE,
        TEAL,
        GRAY,
    ]
)