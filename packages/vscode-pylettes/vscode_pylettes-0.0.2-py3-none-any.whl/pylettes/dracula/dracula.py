# Source: https://draculatheme.com/contribute

from ..base import ColorPalette, Color

BACKGROUND = Color(
    "background",
    (40, 42, 54),
    "#282A36",
    (231, 15, 18),
)

CURRENT_LINE = Color(
    "current_line",
    (68, 71, 90),
    "#44475A",
    (232, 14, 31),
)

FOREGROUND = Color(
    "foreground",
    (248, 248, 242),
    "#F8F8F2",
    (60, 30, 96)
)

COMMENT = Color(
    "comment",
    (98, 114, 164),
    "#6272A4",
    (225, 27, 51)
)

CYAN = Color(
    "cyan",
    (139,233,253),
    "#8BE9FD",
    (190.53, 96.61, 76.86)
)

GREEN = Color(
    "green",
    (80, 250, 123),
    "#50FA7B",
    (135.18, 94.44, 64.71)
)

ORANGE = Color(
    "orange",
    (255,184,108),
    "#FFB86C",
    (31.02, 100, 71.18)
)

PINK = Color(
    "pink",
    (255, 121, 198),
    "#FF79C6",
    (325.52, 100, 73.73)
)

PURPLE = Color(
    "purple",
    (189, 147, 249),
    "#BD93F9",
    (264.71, 89.47, 77.65)
)

RED = Color(
    "red",
    (255, 85, 85),
    "#FF5555",
    (0, 100, 66.67)
)

YELLOW = Color(
    "yellow",
    (241, 250, 140),
    "#F1FA8C",
    (64.91, 91.67, 76.47)
)

Dracula = ColorPalette(
    name="Dracula",
    colors_list=[
        BACKGROUND,
        CURRENT_LINE,
        FOREGROUND,
        COMMENT,
        CYAN,
        GREEN,
        ORANGE,
        PINK,
        PURPLE,
        RED,
        YELLOW
    ]
)