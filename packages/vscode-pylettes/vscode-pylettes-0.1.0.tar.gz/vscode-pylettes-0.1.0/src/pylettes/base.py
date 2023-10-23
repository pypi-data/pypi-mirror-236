class Color:
    def __init__(self, name: str, rgb_code: str, hex_code: str|None = None, hsl_code: str|None = None):
        self.name = name
        self.rgb = rgb_code
        self.r = self.rgb[0]
        self.g = self.rgb[1]
        self.b = self.rgb[2]
        self.hex = self.hex_code(hex_code)
        self.hsl = self.hsl_code(hsl_code)
        
    def __str__(self):
        return f"Color with rgb {self.rgb}, hex {self.hex} and hsl {self.hsl}"
    
    def __repr__(self) -> str:
        return self.__str__()
        
    def hex_code(self, code: str|None):
        if code != None:
            return code
        
        return Color.rgb_to_hex(self.r, self.g, self.b)
    
    def hsl_code(self, code: str|None):
        if code != None:
            return code
        
        return Color.rgb_to_hsl(self.r, self.g, self.b)
    
    
    @classmethod
    def rgb_to_hex(r, g, b):
        return "#{:02X}{:02X}{:02X}".format(r, g, b)
        
    @classmethod
    def rgb_to_hsl(r, g, b):
        red, green, blue = r / 255.0, g / 255.0, b / 255.0

        max_value = max(red, green, blue)
        min_value = min(red, green, blue)

        lightness = (max_value + min_value) / 2.0

        if max_value == min_value:
            saturation = 0
            hue = 0
        else:
            if lightness <= 0.5:
                saturation = (max_value - min_value) / (max_value + min_value)
            else:
                saturation = (max_value - min_value) / (2.0 - max_value - min_value)

            delta = max_value - min_value
            if max_value == red:
                hue = (green - blue) / delta + (6 if green < blue else 0)
            elif max_value == green:
                hue = (blue - red) / delta + 2
            else:
                hue = (red - green) / delta + 4

            hue = (hue / 6.0) % 1.0

        return hue, saturation, lightness


class ColorPalette:
    def __init__(self, name: str, colors_list: list[Color]):
        self.name = name
        self.colors_list = colors_list
        self.color_scheme = self.color_scheme_list()
        self.rgb = self.rgb_dict()
        self.hex = self.hex_dict()
        self.hsl = self.hsl_dict()
        
        for color in colors_list:
            setattr(self, color.name, color)
            
    def __str__(self):
        return f"Palette {self.name} with colors {self.color_scheme}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def color_scheme_list(self) -> list:
        return [color.name for color in self.colors_list]
        
    def rgb_dict(self) -> dict:
        return {color.name: color.rgb for color in self.colors_list}
        
    def hex_dict(self) -> dict:
        return {color.name: color.hex for color in self.colors_list}
        
    def hsl_dict(self) -> dict:
        return {color.name: color.hsl for color in self.colors_list}
        
