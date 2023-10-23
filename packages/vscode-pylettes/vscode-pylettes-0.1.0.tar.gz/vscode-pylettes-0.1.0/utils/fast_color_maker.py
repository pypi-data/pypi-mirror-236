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
