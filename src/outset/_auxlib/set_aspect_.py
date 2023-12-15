from matplotlib import axes as mpl_axes
import numpy as np

from .calc_aspect_ import calc_aspect


def set_aspect(
    ax: mpl_axes.Axes, aspect: float, physical: bool = False
) -> None:
    """Adjust the ratio between ylim span length and xlim span length.

    The function calculates the current aspect ratio of the Axes object and
    adjusts its x-axis or y-axis limits to match the desired aspect ratio.
    If the desired aspect ratio is less than the current, the function
    increases the width of the x-axis. If it is greater, the height of the
    y-axis is increased.

    Note that axes limits are only ever widened. Axes widening is performed
    symmetrically.
    """
    cur_aspect = calc_aspect(ax, physical=physical)
    cur_width = np.ptp(ax.get_xlim())
    cur_height = np.ptp(ax.get_ylim())
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    if aspect == cur_aspect:
        # The current aspect ratio matches the desired one, no action needed
        pass
    elif aspect < cur_aspect:
        # The desired aspect ratio is less than the current,
        # meaning the plot is too tall. We need to increase the width evenly.
        new_width = cur_width / aspect * cur_aspect
        width_extend = (new_width - cur_width) / 2
        ax.set_xlim(x_min - width_extend, x_max + width_extend)
    elif aspect > cur_aspect:
        # The desired aspect ratio is greater than the current,
        # meaning the plot is too wide. We need to increase the height evenly.
        new_height = cur_height * aspect / cur_aspect
        height_extend = (new_height - cur_height) / 2
        ax.set_ylim(y_min - height_extend, y_max + height_extend)
    else:
        assert False, (aspect, cur_aspect)

    new_aspect = calc_aspect(ax, physical=physical)
    assert np.isclose(new_aspect, aspect), (new_aspect, aspect)

    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    assert x0 <= x_min and y0 <= y_min and x1 >= x_max and y1 >= y_max
    assert np.isclose(x0 - x_min, x_max - x1)
    assert np.isclose(y0 - y_min, y_max - y1)
