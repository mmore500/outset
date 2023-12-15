import typing

from matplotlib import axes as mpl_axes
import numpy as np

from .calc_aspect_ import calc_aspect
from .set_aspect_ import set_aspect


def equalize_aspect(
    axs: typing.List[mpl_axes.Axes], physical: bool = False
) -> float:
    """Equalize the aspect ratio across multiple matplotlib Axes objects.

    This function calculates the geometric mean of the aspect ratios of a list
    of Axes objects and sets this common aspect ratio to all Axes in the list.
    The aspect ratio is defined as the ratio of the range of the y-axis to the
    range of the x-axis.

    Parameters
    ----------
    axs : typing.List[mpl_axes.Axes]
        A list of matplotlib Axes objects whose aspect ratios are to be
        equalized.

    Returns
    -------
    float
        The new common aspect ratio set for all Axes objects.
    """
    if not axs:
        return 1.0
    aspects = [calc_aspect(a, physical=physical) for a in axs]
    new_aspect = np.sqrt(min(aspects) * max(aspects))
    for ax in axs:
        set_aspect(ax, new_aspect, physical=physical)
    return new_aspect
