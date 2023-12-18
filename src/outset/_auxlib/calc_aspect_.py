from matplotlib import axes as mpl_axes
import numpy as np


def calc_aspect(ax: mpl_axes.Axes) -> float:
    """Calculate the aspect ratio of the axes.

    If physical is True, the aspect ratio is calculated based on the size ratio
    between unit values unit on each axis after rendering transforms. If
    physical is False, the aspect ratio is based on the axis viewport limits.
    """
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    res = ax._get_aspect_ratio()
    # @MAM WTF, matplotlib is mutating axis limits???
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    assert (xlim, ylim) == (ax.get_xlim(), ax.get_ylim())
    return res
