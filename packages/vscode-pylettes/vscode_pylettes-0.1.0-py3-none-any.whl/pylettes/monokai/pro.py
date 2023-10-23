# Source: https://github.com/loctvl842/monokai-pro.nvim/tree/master

from ..base import ColorPalette, Color

DARK2 = Color(
    "dark2",
    (25, 24, 26),
    "#19181A",
    (270, 4, 9)
)

DARK1 = Color(
    "dark1",
    (34, 31, 34),
    "#221F22",
    (300, 4, 12)
)

BACKGROUND = Color(
    "background",
    (45, 42, 46),
    "#2D2A2E",
    (285, 4, 17)
)

TEXT = Color(
    "text",
    (252, 252, 250),
    "#FCFCFA",
    (60, 25, 98)
)

ACCENT1 = Color(
    "accent1",
    (255, 97, 136),
    "#FF6188",
    (345, 100, 69)
)

ACCENT2 = Color(
    "accent2",
    (252, 152, 103),
    "#FC9867",
    (19, 96, 69)
)

ACCENT3 = Color(
    "accent3",
    (255, 216, 102),
    "#FFD866",
    (44, 99, 70)
)

ACCENT4 = Color(
    "accent4",
    (169, 220, 118),
    "#A9DC76",
    (90, 59, 66)
)

ACCENT5 = Color(
    "accent5",
    (120, 220, 232),
    "#78DCE8",
    (186, 70, 69)
)

ACCENT6 = Color(
    "accent6",
    (171, 157, 242),
    "#AB9DF2",
    (249, 76, 78)
)

DIMMED1 = Color(
    "dimmed1",
    (193, 192, 192),
    "#C1C0C0",
    (0, 0, 75)
)

DIMMED2 = Color(
    "dimmed2",
    (147, 146, 147),
    "#939293",
    (300, 0, 57)
)

DIMMED3 = Color(
    "dimmed3",
    (114, 112, 114),
    "#727072",
    (300, 0, 44)
)

DIMMED4 = Color(
    "dimmed4",
    (91, 89, 92),
    "#5B595C",
    (280, 1, 35)
)

DIMMED5 = Color(
    "dimmed5",
    (64, 62, 65),
    "#403E41",
    (280, 2, 24)
)

MonokaiPro = ColorPalette(
    name="Monokai Pro",
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