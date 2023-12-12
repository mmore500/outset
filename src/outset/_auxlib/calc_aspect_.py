from matplotlib import axes as mpl_axes
import numpy as np


def calc_aspect(ax: mpl_axes.Axes) -> float:
    """Calculate the ratio between ylim span length and xlim span length."""
    return np.ptp(ax.get_ylim()) / np.ptp(ax.get_xlim())
