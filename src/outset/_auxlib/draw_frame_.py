import typing

import frozendict
from matplotlib import axes as mpl_axes
from matplotlib import patches as mpl_patches
from matplotlib import pyplot as plt


def draw_frame(
    frame_xlim: typing.Tuple[float, float],
    frame_ylim: typing.Tuple[float, float],
    ax: typing.Optional[mpl_axes.Axes] = None,
    frame_edge_kwargs: typing.Dict = frozendict.frozendict(),
    frame_face_kwargs: typing.Dict = frozendict.frozendict(),
    **kwargs,
) -> mpl_axes.Axes:
    """Mark a rectangular region with a frame border and an underlaid color
    underlay fill.

    Parameters
    ----------
    frame_xlim : Tuple[float, float]
        The x-limits of the rectangular frame in the form (xmin, xmax).
    frame_ylim : Tuple[float, float]
        The y-limits of the rectangular frame in the form (ymin, ymax).
    ax : matplotlib.axes.Axes, optional
        The axes object on which to draw. If None, the current active axes will
        be used.
    frame_edge_kwargs : Dict, default {}
        Keyword arguments for customizing the frame's edge appearance.
    frame_face_kwargs : Dict, default {}
        Keyword arguments for customizing the frame's face appearance --- i.e.,
        the underlaid solid fill.
    **kwargs
        Additional keyword arguments for the matplotlib `Rectangle` used to draw
        the frame.

    Returns
    -------
    mpl_axes.Axes
        The modified matplotlib axes object with the frame drawing elements added.
    """
    if ax is None:
        ax = plt.gca()

    frame_face_patch = mpl_patches.Rectangle(
        (frame_xlim[0], frame_ylim[0]),  # lower left corner
        frame_xlim[1] - frame_xlim[0],  # width
        frame_ylim[1] - frame_ylim[0],  # height
        **{
            "alpha": 0.1,
            **kwargs,
            "edgecolor": "none",
            "zorder": -1,
            **frame_face_kwargs,
        },
    )
    ax.add_patch(frame_face_patch)

    frame_edge_patch = mpl_patches.Rectangle(
        (frame_xlim[0], frame_ylim[0]),  # lower left corner
        frame_xlim[1] - frame_xlim[0],  # width
        frame_ylim[1] - frame_ylim[0],  # height
        **{
            **kwargs,
            "facecolor": "none",
            **frame_edge_kwargs,
        },
    )
    ax.add_patch(frame_edge_patch)

    return ax
