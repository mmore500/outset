import colorsys
import typing

import matplotlib.colors as mpl_colors


# adapted from https://stackoverflow.com/a/49601444
def lighten_color(
    color: typing.Union[str, typing.Tuple], amount: float = 0.5
) -> typing.Tuple:
    """Lightens the given color by multiplying (1-luminosity) by the given amount. Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """

    try:
        c = mpl_colors.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mpl_colors.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])
