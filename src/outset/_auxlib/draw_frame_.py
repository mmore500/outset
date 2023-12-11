import typing

from matplotlib import axes as mpl_axes
from matplotlib import patches as mpl_patches
from matplotlib import pyplot as plt


def draw_frame(
    frame_xlim: typing.Tuple[float, float],
    frame_ylim: typing.Tuple[float, float],
    ax: typing.Optional[mpl_axes.Axes] = None,
    **kwargs,
) -> mpl_axes.Axes:
    """Mark rectangular region as outset.

    Parameters
    ----------
    frame_xlim : Tuple[float, float]
        The x-limits of the rectangular frame in the form (xmin, xmax).
    frame_ylim : Tuple[float, float]
        The y-limits of the rectangular frame in the form (ymin, ymax).
    ax : matplotlib.axes.Axes, optional
        The axes object on which to draw. If None, the current active axes will
        be used.
    **kwargs
        Additional keyword arguments leader matplotlib `Rectangle`.

    Returns
    -------
    mpl_axes.Axes
        The modified matplotlib axes object with the drawing elements added.
    """
    if ax is None:
        ax = plt.gca()

    frame_patch = mpl_patches.Rectangle(
        (frame_xlim[0], frame_ylim[0]),  # lower left corner
        frame_xlim[1] - frame_xlim[0],  # width
        frame_ylim[1] - frame_ylim[0],  # height
        **kwargs,
    )
    ax.add_patch(frame_patch)

    return ax
