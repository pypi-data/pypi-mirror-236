from ..base import ColorPalette, Color

BACKGROUND = Color(
    "Background",
    (40, 42, 54),
    "#282A36",
    (231, 15, 18),
)

CURRENT_LINE = Color(
    "CurrentLine",
    (68, 71, 90),
    "#44475A",
    (232, 14, 31),
)

Dracula = ColorPalette(
    name="Dracula",
    colors_list=[BACKGROUND,
    CURRENT_LINE
    ]
)