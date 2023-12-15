from matplotlib import axes as mpl_axes
import numpy as np


def calc_aspect(ax: mpl_axes.Axes, physical: bool = False) -> float:
    """Calculate the aspect ratio of the axes.

    If physical is True, the aspect ratio is calculated based on the size ratio
    between unit values unit on each axis after rendering transforms. If
    physical is False, the aspect ratio is based on the axis viewport limits.
    """
    if physical:
        # Transform a point one unit right and one unit up from the origin
        origin = ax.transData.transform((0, 0))
        one_unit_right = ax.transData.transform((1, 0))
        one_unit_up = ax.transData.transform((0, 1))

        # Calculate the distance in pixels for one unit on each axis
        dx = np.sqrt(
            (one_unit_right[0] - origin[0]) ** 2
            + (one_unit_right[1] - origin[1]) ** 2
        )
        dy = np.sqrt(
            (one_unit_up[0] - origin[0]) ** 2
            + (one_unit_up[1] - origin[1]) ** 2
        )

        # Calculate the physical aspect ratio
        aspect_ratio = dx / dy
    else:
        # Calculate the aspect ratio based on data limits.
        aspect_ratio = np.ptp(ax.get_ylim()) / np.ptp(ax.get_xlim())

    return aspect_ratio
