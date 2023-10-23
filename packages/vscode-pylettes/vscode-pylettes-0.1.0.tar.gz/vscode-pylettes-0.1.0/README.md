# vscode-pylettes
Color Palettes from VSCode most famous themes made available in RGB and HEX. 

# Usage

## Know available palettes
```python
>>> import pylettes
>>> pylettes.palettes_list
['CatpuccinoFrappe', 'CatpuccinoLatte', 'CatpuccinoMacchiato', 'CatpuccinoMocha', 'Dracula', 'Hypersubatomic', 'MonokaiClassic', 'MonokaiMachine', 'MonokaiOctagon', 'MonokaiPro', 'MonokaiRistretto', 'MonokaiSpectrum', 'OneDark', 'TokyoNight', 'TokyoNightLight', 'TokyoNightStorm']
```

## Select a Palette
```python
>>> import pylettes
>>> pylettes.CatpuccinoFrappe
Palette Catpuccino Frappe with colors ['rosewater', 'flamingo', 'pink', 'mauve', 'red', 'maroon', 'peach', 'yellow', 'green', 'teal', 'sky', 'sapphire', 'blue', 'lavender', 'text', 'subtext1', 'subtext0', 'overlay2', 'overlay1', 'overlay0', 'surface2', 'surface1', 'surface0', 'base', 'mantle', 'crust']
```

## Select a Color from a Palette
```python
>>> import pylettes
>>> frappe = pylettes.CatpuccinoFrappe
>>> frappe.green
Color with rgb (166, 209, 137), hex #A6D189 and hsl (95, 43, 67)
>>> frappe.green.rgb
(166, 209, 137)
>>> frappe.green.hex
'#A6D189'
>>> frappe.green.hsl
(95, 43, 67)
```

## Example of use
Below you can see all the supported themes. The images were created automatically using [ManimCE](https://www.manim.community/) with the code inside palettes_examples/make_palettes_examples.py


# Supported Themes

## Catpuccino Themes
[![CatpuccinoFrappe](./palettes_examples/Catpuccino_Frappe.png)](https://catppuccin-website.vercel.app/)
[![CatpuccinoLatte](./palettes_examples/Catpuccino_Latte.png)](https://catppuccin-website.vercel.app/)
[![CatpuccinoMacchiato](./palettes_examples/Catpuccino_Macchiato.png)](https://catppuccin-website.vercel.app/)
[![CatpuccinoMocha](./palettes_examples/Catpuccino_Mocha.png)](https://catppuccin-website.vercel.app/)

## Dracula themes
[![Dracula](./palettes_examples/Dracula.png)](https://draculatheme.com/)

## Hypersubatomic themes
[![Hypersubatomic](./palettes_examples/Hypersubatomic.png)](https://marketplace.visualstudio.com/items?itemName=neilpanchal.hypersubatomic)

## Monkai Themes
[![MonokaiClassic](./palettes_examples/Monokai_Classic.png)](https://github.com/loctvl842/monokai-pro.nvim/tree/master)
[![MonokaiMachine](./palettes_examples/Monokai_Machine.png)](https://github.com/loctvl842/monokai-pro.nvim/tree/master)
[![MonokaiOctagon](./palettes_examples/Monokai_Octagon.png)](https://github.com/loctvl842/monokai-pro.nvim/tree/master)
[![MonokaiPro](./palettes_examples/Monokai_Pro.png)](https://monokai.pro/)
[![MonokaiRistretto](./palettes_examples/Monokai_Ristretto.png)](https://github.com/loctvl842/monokai-pro.nvim/tree/master)
[![MonokaiSpectrum](./palettes_examples/Monokai_Spectrum.png)](https://github.com/loctvl842/monokai-pro.nvim/tree/master)

## One Dark Themes
[![OneDark](./palettes_examples/One_Dark.png)](https://marketplace.visualstudio.com/items?itemName=zhuangtongfa.Material-theme)

## Tokyo Night Themes
[![TokyoNight](./palettes_examples/Tokyo_Night.png)](https://github.com/enkia/tokyo-night-vscode-theme)
[![TokyoNightLight](./palettes_examples/Tokyo_Night_Light.png)](https://github.com/enkia/tokyo-night-vscode-theme)
[![TokyoNightStorm](./palettes_examples/Tokyo_Night_Storm.png)](https://github.com/enkia/tokyo-night-vscode-theme)