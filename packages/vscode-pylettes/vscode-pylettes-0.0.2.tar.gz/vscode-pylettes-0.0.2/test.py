import colorsys

def hex_to_rgb(hex_color):
    # Remove the "#" character if present
    hex_color = hex_color.lstrip('#')

    # Check if the hex color code is valid
    if not all(c in '0123456789ABCDEFabcdef' for c in hex_color) or len(hex_color) != 6:
        raise ValueError("Invalid hexadecimal color code")

    # Convert the hex values to integers
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return (r, g, b)



def hex_to_hsl(hex_color):
    # Remove the "#" character if present
    hex_color = hex_color.lstrip('#')

    # Check if the hex color code is valid
    if not all(c in '0123456789ABCDEFabcdef' for c in hex_color) or len(hex_color) != 6:
        raise ValueError("Invalid hexadecimal color code")

    # Convert the hex values to integers
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0

    # Convert RGB to HSL
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Scale H, S, and L to the typical HSL range
    h = int(h * 360)
    s = int(s * 100)
    l = int(l * 100)

    return (h, s, l)
 
def hex_to_class(name: str, hex: str) -> str:
    rgb = hex_to_rgb(hex)
    hsl = hex_to_hsl(hex)
    print(f"{name.upper()} = Color(")
    print(f"    \"{name.lower()}\",")
    print(f"    {rgb},")
    print(f"    \"{hex.upper()}\",")
    print(f"    {hsl}")
    print(f")")
    print("")

hex_to_class("background", "#8c4351")
hex_to_class("gray", "#9699a3")
hex_to_class("black", "#0f0f14")
hex_to_class("coffee", "#634f30")
hex_to_class("coral_black", "#565a6e")
hex_to_class("charcoal", "#343b58")
hex_to_class("purple", "#5a4a78")
hex_to_class("dark_blue", "#34548a")
hex_to_class("dark_teal", "#0f4b6e")
hex_to_class("teal", "#166775")
hex_to_class("dark_green", "#33635c")
hex_to_class("green", "#485e30")
hex_to_class("brown", "#8f5e15")
hex_to_class("orange", "#965027")
hex_to_class("red", "#8c4351")
