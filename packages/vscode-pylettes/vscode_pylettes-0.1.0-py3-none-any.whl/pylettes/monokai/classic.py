# Source: https://github.com/loctvl842/monokai-pro.nvim/tree/master

from ..base import ColorPalette, Color

DARK2 = Color(
    "dark2",
    (22, 22, 19),
    "#161613",
    (60, 7, 8)
)

DARK1 = Color(
    "dark1",
    (29, 30, 25),
    "#1D1E19",
    (72, 9, 10)
)

BACKGROUND = Color(
    "background",
    (39, 40, 34),
    "#272822",
    (69, 8, 14)
)

TEXT = Color(
    "text",
    (253, 255, 241),
    "#FDFFF1",
    (68, 100, 97)
)

ACCENT1 = Color(
    "accent1",
    (249, 38, 114),
    "#F92672",
    (338, 94, 56)
)

ACCENT2 = Color(
    "accent2",
    (253, 151, 31),
    "#FD971F",
    (32, 98, 55)
)

ACCENT3 = Color(
    "accent3",
    (230, 219, 116),
    "#E6DB74",
    (54, 69, 67)
)

ACCENT4 = Color(
    "accent4",
    (166, 226, 46),
    "#A6E22E",
    (79, 75, 53)
)

ACCENT5 = Color(
    "accent5",
    (102, 217, 239),
    "#66D9EF",
    (189, 81, 66)
)

ACCENT6 = Color(
    "accent6",
    (174, 129, 255),
    "#AE81FF",
    (261, 100, 75)
)

DIMMED1 = Color(
    "dimmed1",
    (192, 193, 181),
    "#C0C1B5",
    (64, 8, 73)
)

DIMMED2 = Color(
    "dimmed2",
    (145, 146, 136),
    "#919288",
    (65, 4, 55)
)

DIMMED3 = Color(
    "dimmed3",
    (110, 112, 102),
    "#6E7066",
    (71, 4, 41)
)

DIMMED4 = Color(
    "dimmed4",
    (87, 88, 79),
    "#57584F",
    (66, 5, 32)
)

DIMMED5 = Color(
    "dimmed5",
    (59, 60, 53),
    "#3B3C35",
    (68, 6, 22)
)

MonokaiClassic = ColorPalette(
    name="Monokai Classic",
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