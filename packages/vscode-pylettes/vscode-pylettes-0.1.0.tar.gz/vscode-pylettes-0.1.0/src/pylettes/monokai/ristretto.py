# Source: https://github.com/loctvl842/monokai-pro.nvim/tree/master

from ..base import ColorPalette, Color

DARK2 = Color(
    "dark2",
    (25, 21, 21),
    "#191515",
    (0, 8, 9)
)

DARK1 = Color(
    "dark1",
    (33, 28, 28),
    "#211C1C",
    (0, 8, 11)
)

BACKGROUND = Color(
    "background",
    (44, 37, 37),
    "#2C2525",
    (0, 8, 15)
)

TEXT = Color(
    "text",
    (255, 241, 243),
    "#FFF1F3",
    (351, 100, 97)
)

ACCENT1 = Color(
    "accent1",
    (253, 104, 131),
    "#FD6883",
    (349, 97, 70)
)

ACCENT2 = Color(
    "accent2",
    (243, 141, 112),
    "#F38D70",
    (13, 84, 69)
)

ACCENT3 = Color(
    "accent3",
    (249, 204, 108),
    "#F9CC6C",
    (40, 92, 70)
)

ACCENT4 = Color(
    "accent4",
    (173, 218, 120),
    "#ADDA78",
    (87, 56, 66)
)

ACCENT5 = Color(
    "accent5",
    (133, 218, 204),
    "#85DACC",
    (170, 53, 68)
)

ACCENT6 = Color(
    "accent6",
    (168, 169, 235),
    "#A8A9EB",
    (239, 62, 79)
)

DIMMED1 = Color(
    "dimmed1",
    (195, 183, 184),
    "#C3B7B8",
    (355, 9, 74)
)

DIMMED2 = Color(
    "dimmed2",
    (148, 138, 139),
    "#948A8B",
    (354, 4, 56)
)

DIMMED3 = Color(
    "dimmed3",
    (114, 105, 106),
    "#72696A",
    (353, 4, 42)
)

DIMMED4 = Color(
    "dimmed4",
    (91, 83, 83),
    "#5B5353",
    (0, 4, 34)
)

DIMMED5 = Color(
    "dimmed5",
    (64, 56, 56),
    "#403838",
    (0, 6, 23)
)

MonokaiRistretto = ColorPalette(
    name="Monokai Ristretto",
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