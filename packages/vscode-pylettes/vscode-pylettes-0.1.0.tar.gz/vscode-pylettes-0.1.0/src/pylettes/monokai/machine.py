# Source: https://github.com/loctvl842/monokai-pro.nvim/tree/master

from ..base import ColorPalette, Color
DARK2 = Color(
    "dark2",
    (22, 27, 30),
    "#161B1E",
    (202, 15, 10)
)

DARK1 = Color(
    "dark1",
    (29, 37, 40),
    "#1D2528",
    (196, 15, 13)
)

BACKGROUND = Color(
    "background",
    (39, 49, 54),
    "#273136",
    (199, 16, 18)
)

TEXT = Color(
    "text",
    (242, 255, 252),
    "#F2FFFC",
    (166, 100, 97)
)

ACCENT1 = Color(
    "accent1",
    (255, 109, 126),
    "#FF6D7E",
    (353, 100, 71)
)

ACCENT2 = Color(
    "accent2",
    (255, 178, 112),
    "#FFB270",
    (27, 100, 71)
)

ACCENT3 = Color(
    "accent3",
    (255, 237, 114),
    "#FFED72",
    (52, 100, 72)
)

ACCENT4 = Color(
    "accent4",
    (162, 229, 123),
    "#A2E57B",
    (97, 67, 69)
)

ACCENT5 = Color(
    "accent5",
    (124, 213, 241),
    "#7CD5F1",
    (194, 80, 71)
)

ACCENT6 = Color(
    "accent6",
    (186, 160, 248),
    "#BAA0F8",
    (257, 86, 80)
)

DIMMED1 = Color(
    "dimmed1",
    (184, 196, 195),
    "#B8C4C3",
    (174, 9, 74)
)

DIMMED2 = Color(
    "dimmed2",
    (139, 151, 152),
    "#8B9798",
    (184, 5, 57)
)

DIMMED3 = Color(
    "dimmed3",
    (107, 118, 120),
    "#6B7678",
    (189, 5, 44)
)

DIMMED4 = Color(
    "dimmed4",
    (84, 95, 98),
    "#545F62",
    (192, 7, 35)
)

DIMMED5 = Color(
    "dimmed5",
    (58, 68, 73),
    "#3A4449",
    (199, 11, 25)
)

MonokaiMachine = ColorPalette(
    name="Monokai Machine",
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