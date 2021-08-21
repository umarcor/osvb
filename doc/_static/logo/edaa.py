#!/usr/bin/env python3

import drawSvg as draw

# https://www.materialpalette.com/colors
materialpalette = {
    # Red, Pink, Purple, Light Blue, Light Green, Amber, Deep Orange, Blue Grey
    "900": ["#b71c1c", "#880e4f", "#4a148c", "#01579b", "#33691e", "#ff6f00", "#bf360c", "#263238"],
    "800": ["#c62828", "#ad1457", "#6a1b9a", "#0277bd", "#558b2f", "#ff8f00", "#d84315", "#37474f"],
    "400": ["#ef5350", "#ec407a", "#ab47bc", "#29b6f6", "#9ccc65", "#ffca28", "#ff7043", "#78909c"],
    "A100": ["#ff8a80", "#ff80ab", "#ea80fc", "#80d8ff", "#ccff90", "#ffe57f", "#ff9e80", "#cfd8dc"],
    "A400": ["#ff1744", "#f50057", "#d500f9", "#00b0ff", "#76ff03", "#ffc400", "#ff3d00", "#263238"],
    "A700": ["#d50000", "#c51162", "#aa00ff", "#0091ea", "#64dd17", "#ffab00", "#dd2c00", "#263238"],
}


def _draw(name, colors, shades):
    unit = 50
    d = draw.Drawing(6 * unit, 6 * unit, displayInline=False)
    for x in range(6):
        d.append(draw.Rectangle(2 * unit, x * unit, 2 * unit, unit, fill=materialpalette[shades[0]][colors[x]]))
        d.append(
            draw.Rectangle(
                4 * unit * (1 - (x % 2)), x * unit, 2 * unit, unit, fill=materialpalette[shades[1]][colors[x]]
            )
        )

    d.setPixelScale(1)  # Set number of pixels per geometry unit
    # d.setRenderSize(500,500)  # Alternative to setPixelScale
    d.saveSvg("{0}.svg".format(name))
    # d.savePng('example.png')


red_gray = [7, 5, 4, 3, 2, 0]
pink_gray = [7, 5, 4, 3, 2, 1]
pink_orange = [6, 5, 4, 3, 2, 1]
s800_400 = ["800", "400"]
sA700_A100 = ["A700", "A100"]

_draw("800_400_rg", red_gray, s800_400)
_draw("800_400_pg", pink_gray, s800_400)
_draw("800_400_po", pink_orange, s800_400)
_draw("A700_A100_rg", red_gray, sA700_A100)
_draw("A700_A100_pg", pink_gray, sA700_A100)
_draw("A700_A100_po", pink_orange, sA700_A100)
