import typing

import matplotlib.pyplot as plt
from matplotlib import axes as mpl_axes
from matplotlib import markers as mpl_markers

from .._auxlib.rotate_marker_ import rotate_marker


def mark_magnifying_glass(
    x: typing.Union[float, typing.Sequence[float]],
    y: typing.Union[float, typing.Sequence[float]],
    ax: typing.Optional[mpl_axes.Axes] = None,
    *,
    alpha: float = 1.0,
    color: str = "black",
    color_accent: typing.Optional[str] = None,
    linecolor: str = "none",
    markersize: float = 15,
    rotate_angle: float = 20,
    **kwargs,
) -> None:
    """Draw magnifying glass marker(s) at specified location(s) on a matplotlib
    plot.

    This function creates a magnifying glass glyph by stacking several
    matplotlib markers.

    Parameters
    ----------
    x : float or sequence of floats
        The x-coordinate(s) where the magnifying glass(es) will be placed.
    y : float or sequence of floats
        The y-coordinate(s) where the magnifying glass(es) will be placed.
    ax : mpl_axes.Axes, optional
        The axes object on which to draw the markers.

        If None, `plt.gca()` will be used.
    color_accent : Optional[str], optional
        The default accent color for the glyph.

        If `color` is "white", defaults "black". Otherwise, defaults "white".
    alpha : float, default 1.0
        The transparency level of the markers.
    color : str, default "black"
        The primary color for the glyph components.
    linecolor : str, default "none"
        Color for connecting lines between markers, if any.
    markersize : float, default 15
        Size for glyph's largest marker element.
    rotate_angle : float, default 20
        The angle (in degrees) to rotate the asterisk part of the magnifying
        glass.
    **kwargs : dict, optional
        Additional keyword arguments forward to matplotlib `plot`.

    Returns
    -------
    None
    """
    if ax is None:
        ax = plt.gca()

    if color_accent is None:
        color_accent = "black" if color == "white" else "white"

    handle_marker = rotate_marker(3, rotate_angle)  # TICKDOWN

    # Scaling factors for different elements relative to markersize
    handle_underlay_scale = 1.5 / 1.5
    handle_scale = 1.4 / 1.5
    circle_scale = 1.3 / 1.5
    ring_scale = 1.1 / 1.5

    # Underlay handle
    ax.plot(
        x,
        y,
        alpha=alpha,
        color=linecolor,
        marker=handle_marker,
        markeredgecolor=color_accent,
        markeredgewidth=markersize / 3,
        markersize=markersize * handle_underlay_scale,
        **kwargs,
    )

    # Draw handle
    ax.plot(
        x,
        y,
        alpha=0.8 * alpha,
        color="none",  # line rendering is handled above
        marker=handle_marker,
        markeredgecolor=color,
        markeredgewidth=markersize / 6,
        markerfacecolor=color,
        markersize=markersize * handle_scale,
        **kwargs,
    )

    # Underlay glass lens
    ax.plot(
        x,
        y,
        alpha=alpha,
        color="none",  # line rendering is handled above
        marker="o",
        markeredgecolor=color_accent,
        markeredgewidth=markersize / 12,
        markerfacecolor=color_accent,
        markersize=markersize * circle_scale,
        **kwargs,
    )

    # Tint glass lens
    ax.plot(
        x,
        y,
        alpha=0.1 * alpha,
        color="none",  # line rendering is handled above
        marker="o",
        markeredgecolor="none",
        markeredgewidth=2,
        markerfacecolor=color,
        markersize=markersize * ring_scale,
        **kwargs,
    )

    # Draw glass ring
    ax.plot(
        x,
        y,
        alpha=0.7 * alpha,
        color="none",  # line rendering is handled above
        marker="o",
        markeredgecolor=color,
        markeredgewidth=markersize / 12,
        markerfacecolor="none",
        markersize=markersize * ring_scale,
        **kwargs,
    )


class MarkMagnifyingGlass:
    """Functor interface for `mark_magnifying_glass`."""

    _kws: dict

    def __init__(self: "MarkMagnifyingGlass", **kwargs) -> None:
        """Initialize functor.

        kwargs will forward to `__call__`.
        """
        self._kws = kwargs

    def __call__(self, *args, **kwargs):
        """Forwards to `mark_magnifying_glass`."""
        return mark_magnifying_glass(*args, **{**self._kws, **kwargs})
