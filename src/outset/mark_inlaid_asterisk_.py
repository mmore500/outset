import typing

import matplotlib.pyplot as plt
from matplotlib import axes as mpl_axes

_color_t = typing.Union[typing.Tuple, str]


def mark_inlaid_asterisk(
    x: typing.Union[float, typing.Sequence[float]],
    y: typing.Union[float, typing.Sequence[float]],
    ax: typing.Optional[mpl_axes.Axes] = None,
    *,
    asterisk_edgewidth: float = 1,
    color: str = "black",
    color_accent: str = "white",
    color_asterisk_edge: _color_t = ("color", 0.7),
    color_asterisk_face: _color_t = ("color", 0.7),
    color_badge: _color_t = ("color", 0.3),
    color_underlay: _color_t = "color_accent",
    marker: typing.Tuple = (6, 2, 0),  # 6 points, rotated 0 degrees
    marker_badge: str = "o",
    marker_underlay: str = "o",
    linecolor: str = "none",
    markersize: float = 22,
    scale_asterisk: float = 0.3,
    scale_badge: float = 0.8,
    **kwargs,
) -> None:
    """
    Draw asterisk badge marker(s) at specified location(s) on a matplotlib plot.

    This function stacks matplotlib markers to render an asterisk overlaid onto a circular badge with a slightly larger circular underlay.

    Parameters
    ----------
    x : float or sequence of floats
        The x-coordinate(s) where the asterisk badge(s) will be placed.
    y : float or sequence of floats
        The y-coordinate(s) where the asterisk badge(s) will be placed.
    ax : mpl_axes.Axes, optional
        The axes object on which to draw the markers. If None, plt.gca() will be used.
    asterisk_edgewidth : float, default 1
        The edge width of the asterisk marker.
    color : str, default "black"
        The primary color for the glyph.
    color_asterisk_edge : Union[str, tuple], default ("color", 0.7)
        The edge color of the asterisk marker.

        If "color", primary color will be substituted.
    color_asterisk_face : Union[str, tuple], default ("color", 0.7)
        The face color of the asterisk marker.

        If "color", primary color will be substituted.
    color_badge : Union[str, tuple], default ("color", 0.3)
        The color of the badge.

        If "color", primary color will be substituted.
    color_underlay : Union[str, tuple], default "white"
        The color of the underlay.
    marker : tuple, default (6, 2, 0)
        The marker style for the asterisk. Default is 6 points, rotated 0 degrees.
    marker_badge : str, default "o"
        The marker style for the badge.
    marker_underlay : str, default "o"
        The marker style for the underlay.
    linecolor : str, default "none"
        The color of the line connecting markers, if any.
    markersize : float, default 22
        Size for glyph's largest marker element.
    scale_asterisk : float, default 0.3
        The scaling factor for the asterisk size.
    scale_badge : float, default 0.8
        The scaling factor for the badge size.
    **kwargs : dict, optional
        Additional keyword arguments forward to matplotlib `plot`.

    Returns
    -------
    None
    """
    if ax is None:
        ax = plt.gca()

    # substitute "color" with color kwarg
    def substitute_color(query: _color_t) -> _color_t:
        if query == "color":
            return color
        elif query == "color_accent":
            return color_accent
        elif isinstance(query, tuple):
            if not query:
                raise ValueError("color tuple must have at least one element")
            first, *rest = query
            if first == "color":
                return (color, *rest)
            elif first == "color_accent":
                return (color_accent, *rest)
            else:
                return query
        else:
            return query

    colors = {
        "color_asterisk_edge": substitute_color(color_asterisk_edge),
        "color_asterisk_face": substitute_color(color_asterisk_face),
        "color_badge": substitute_color(color_badge),
        "color_underlay": substitute_color(color_underlay),
    }

    # Base underlay
    ax.plot(
        x,
        y,
        color=linecolor,
        marker=marker_underlay,
        markeredgecolor="none",
        markerfacecolor=colors["color_underlay"],
        markersize=markersize,
        **kwargs,
    )

    # Badge
    ax.plot(
        x,
        y,
        color="none",
        marker=marker_badge,
        markeredgecolor="none",
        markerfacecolor=colors["color_badge"],
        markersize=markersize * scale_badge,
        **kwargs,
    )

    # Asterisk
    plt.plot(
        x,
        y,
        marker=marker,
        markeredgewidth=asterisk_edgewidth,
        markeredgecolor=colors["color_asterisk_edge"],
        markerfacecolor=colors["color_asterisk_face"],
        markersize=markersize * scale_asterisk,
        **kwargs,
    )
