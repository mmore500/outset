import typing

import matplotlib.pyplot as plt
from matplotlib import axes as mpl_axes
from matplotlib import markers as mpl_markers


def mark_arrow(
    x: typing.Union[float, typing.Sequence[float]],
    y: typing.Union[float, typing.Sequence[float]],
    ax: typing.Optional[mpl_axes.Axes] = None,
    *,
    alpha: float = 1.0,
    color: str = "black",
    color_accent: str = "white",
    linecolor: str = "none",
    markersize: float = 15,
    rotate_angle: float = 20,
    **kwargs,
) -> None:
    """Draw arrow marker(s) at specified location(s) on a matplotlib plot.

    This function creates an arrow glyph by combining and rotating matplotlib
    markers.

    Parameters
    ----------
    x : float or sequence of floats
        The x-coordinate(s) where the arrow(s) will be placed.
    y : float or sequence of floats
        The y-coordinate(s) where the arrow(s) will be placed.
    ax : mpl_axes.Axes, optional
        The axes object on which to draw the markers. If None, `plt.gca()` will
        be used.
    alpha : float, default 1.0
        The transparency level of the markers.
    color : str, default "black"
        The primary color for the glyph components.
    color_accent : str, default "white"
        The color used for the accent layer of the glyph, enhancing visibility.
    linecolor : str, default "none"
        Color for connecting lines between markers, if any.
    markersize : float, default 15
        Size for glyph's largest marker element.
    rotate_angle : float, default 20
        The angle (in degrees) to rotate the arrow part of the glyph.
    **kwargs : dict, optional
        Additional keyword arguments forward to matplotlib `plot`.

    Returns
    -------
    matplotlib.axes.Axes
        The matplotlib axes containing the plot.
    """
    if ax is None:
        ax = plt.gca()

    # rotated tickdown marker for handle
    # adapted from https://stackoverflow.com/a/49662573
    head_marker = mpl_markers.MarkerStyle(marker=10)  # CARETUP
    head_marker._transform = head_marker.get_transform().rotate_deg(
        rotate_angle,
    )
    stem_marker = mpl_markers.MarkerStyle(marker=3)  # TICKDOWN
    stem_marker._transform = stem_marker.get_transform().rotate_deg(
        rotate_angle,
    )

    # Scaling factors for different elements relative to markersize
    overlay_scale = 0.8
    stem_scale = 0.6

    # Underlay stem
    ax.plot(
        x,
        y,
        alpha=alpha,
        color=linecolor,
        marker=stem_marker,
        markeredgecolor=color_accent,
        markeredgewidth=markersize * 0.75,
        markersize=markersize * stem_scale,
        **kwargs,
    )

    # Draw stem
    ax.plot(
        x,
        y,
        alpha=0.8 * alpha,
        color="none",  # line rendering is handled above
        marker=stem_marker,
        markeredgecolor=color,
        markeredgewidth=markersize * 0.5,
        markerfacecolor=color,
        markersize=markersize * overlay_scale * stem_scale,
        **kwargs,
    )

    # Underlay arrowhead
    ax.plot(
        x,
        y,
        alpha=alpha,
        color="none",  # line rendering is handled above
        marker=head_marker,
        markeredgecolor=color_accent,
        markeredgewidth=markersize / 12,
        markerfacecolor=color_accent,
        markersize=markersize,
        **kwargs,
    )

    # draw arrowhead
    ax.plot(
        x,
        y,
        alpha=0.8 * alpha,
        color="none",  # line rendering is handled above
        marker=head_marker,
        markeredgecolor="none",
        markerfacecolor=color,
        markersize=markersize * overlay_scale,
        **kwargs,
    )
