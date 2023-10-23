from manim import *
import pylettes

max_width = 12
max_height = 6
class MakePalette(Scene):
    def __init__(self, palette, renderer=None, camera_class=Camera, always_update_mobjects=False, random_seed=None, skip_animations=False):
        super().__init__(renderer, camera_class, always_update_mobjects, random_seed, skip_animations)
        self.palette = palette
        
    def draw_rectangle(self, color, width):
        height = 8
        self.add(Rectangle(height=height, width=width, color=color, fill_opacity=1))
        
    def get_palette_colors_list(self, palette):
        colors_list = eval(f"pylettes.{palette}.color_scheme")
        return [eval(f"pylettes.{palette}.{color}.hex") for color in colors_list]
    
    def get_correct_width(self, colors, rect_width):
        # Worst way I could think of. Make it better
        text_width = colors[0].get_width()
        max_w = rect_width*0.9
        while text_width > max_w:
            colors = [color.scale(0.9) for color in colors]
            text_width = colors[0].get_width()
            
        return colors
    
    def make_palette_rectangles(self, palette):
        colors_list = self.get_palette_colors_list(palette)
        rect_width = max_width/(len(colors_list)+1)
        rects_list = [Rectangle(height=max_height, width=rect_width, color=color, fill_opacity=1) for color in colors_list]
        text_colors_list = self.get_correct_width([Text(f"{color}") for color in colors_list], rect_width)
        rects_g = VGroup(*rects_list).arrange(buff=0).shift(DOWN)
        text_color_g = VGroup(*text_colors_list)
        
        for name, rect in zip(text_color_g, rects_g):
            name.next_to(rect, UP)
        
        named_rects = VGroup(rects_g, text_color_g)
        return named_rects
    
    def make_palette_name(self, palette):
        t = Text(eval(f"pylettes.{palette}.name")).shift(3*UP)
        
        return t
    
    def construct(self):
        self.add(self.make_palette_rectangles(self.palette))
        self.add(self.make_palette_name(self.palette))




items = dir(pylettes)
palettes = [palette for palette in items if palette[0].isupper()]
palettes_direction = []
for palette in palettes:
    palette_name = eval(f"pylettes.{palette}.name").replace(" ", "_")
    config.output_file = f"{palette_name}.png"
    pal = MakePalette(palette)
    pal.render(preview=True)
    palettes_direction.append(f"![{palette}]()./palettes_examples/{palette_name}.png)")
    
for palette_direction in palettes_direction:
    print(palette_direction)