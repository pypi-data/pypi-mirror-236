# Source: https://github.com/loctvl842/monokai-pro.nvim/tree/master

from ..base import ColorPalette, Color
DARK2 = Color(
    "dark2",
    (19, 19, 19),
    "#131313",
    (0, 0, 7)
)

DARK1 = Color(
    "dark1",
    (25, 25, 25),
    "#191919",
    (0, 0, 9)
)

BACKGROUND = Color(
    "background",
    (34, 34, 34),
    "#222222",
    (0, 0, 13)
)

TEXT = Color(
    "text",
    (247, 241, 255),
    "#F7F1FF",
    (265, 100, 97)
)

ACCENT1 = Color(
    "accent1",
    (252, 97, 141),
    "#FC618D",
    (342, 96, 68)
)

ACCENT2 = Color(
    "accent2",
    (253, 147, 83),
    "#FD9353",
    (22, 97, 65)
)

ACCENT3 = Color(
    "accent3",
    (252, 229, 102),
    "#FCE566",
    (50, 96, 69)
)

ACCENT4 = Color(
    "accent4",
    (123, 216, 143),
    "#7BD88F",
    (132, 54, 66)
)

ACCENT5 = Color(
    "accent5",
    (90, 212, 230),
    "#5AD4E6",
    (187, 73, 62)
)

ACCENT6 = Color(
    "accent6",
    (148, 138, 227),
    "#948AE3",
    (246, 61, 71)
)

DIMMED1 = Color(
    "dimmed1",
    (186, 182, 192),
    "#BAB6C0",
    (263, 7, 73)
)

DIMMED2 = Color(
    "dimmed2",
    (139, 136, 143),
    "#8B888F",
    (265, 3, 54)
)

DIMMED3 = Color(
    "dimmed3",
    (105, 103, 108),
    "#69676C",
    (263, 2, 41)
)

DIMMED4 = Color(
    "dimmed4",
    (82, 80, 83),
    "#525053",
    (280, 1, 31)
)

DIMMED5 = Color(
    "dimmed5",
    (54, 53, 55),
    "#363537",
    (269, 1, 21)
)

MonokaiSpectrum = ColorPalette(
    name="Monokai Spectrum",
    colors_list=[
        DARK2,
        DARK1,
        BACKGROUND,
        TEXT,
        ACCENT1,
        ACCENT2,
        ACCENT3,
        ACCENT4,
        ACCENT5,
        ACCENT6,
        DIMMED1,
        DIMMED2,
        DIMMED3,
        DIMMED4,
        DIMMED5,
    ]
)