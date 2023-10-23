# Source: https://github.com/loctvl842/monokai-pro.nvim/tree/master

from ..base import ColorPalette, Color
DARK2 = Color(
    "dark2",
    (22, 24, 33),
    "#161821",
    (229, 20, 10)
)

DARK1 = Color(
    "dark1",
    (30, 31, 43),
    "#1E1F2B",
    (235, 17, 14)
)

BACKGROUND = Color(
    "background",
    (40, 42, 58),
    "#282A3A",
    (233, 18, 19)
)

TEXT = Color(
    "text",
    (234, 242, 241),
    "#EAF2F1",
    (172, 23, 93)
)

ACCENT1 = Color(
    "accent1",
    (255, 101, 122),
    "#FF657A",
    (351, 100, 69)
)

ACCENT2 = Color(
    "accent2",
    (255, 155, 94),
    "#FF9B5E",
    (22, 100, 68)
)

ACCENT3 = Color(
    "accent3",
    (255, 215, 109),
    "#FFD76D",
    (43, 100, 71)
)

ACCENT4 = Color(
    "accent4",
    (186, 215, 97),
    "#BAD761",
    (74, 59, 61)
)

ACCENT5 = Color(
    "accent5",
    (156, 209, 187),
    "#9CD1BB",
    (155, 36, 71)
)

ACCENT6 = Color(
    "accent6",
    (195, 154, 201),
    "#C39AC9",
    (292, 30, 69)
)

DIMMED1 = Color(
    "dimmed1",
    (178, 185, 189),
    "#B2B9BD",
    (201, 7, 71)
)

DIMMED2 = Color(
    "dimmed2",
    (136, 141, 148),
    "#888D94",
    (215, 5, 55)
)

DIMMED3 = Color(
    "dimmed3",
    (105, 109, 119),
    "#696D77",
    (222, 6, 43)
)

DIMMED4 = Color(
    "dimmed4",
    (83, 87, 99),
    "#535763",
    (225, 8, 35)
)

DIMMED5 = Color(
    "dimmed5",
    (58, 61, 75),
    "#3A3D4B",
    (229, 12, 26)
)

MonokaiOctagon = ColorPalette(
    name="Monokai Octagon",
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