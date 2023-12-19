import typing

from matplotlib.axes import Axes as mpl_Axes
from matplotlib.collections import PathCollection
from matplotlib import pyplot as plt
import numpy as np

from ._CalcBoundsIQR import CalcBoundsIQR


def rescale_clip_outliers(
    ax: typing.Optional[mpl_Axes] = None,
    calc_outlier_bounds: typing.Union[
        typing.Callable,
        typing.Tuple[typing.Callable, typing.Callable],
        None,
    ] = None,
    *,
    pad: float = 0.1,
) -> None:
    """Rescale the axes of a Matplotlib axes with plotted points to exclude
    outliers.

    This function inspects plotted points already on the axes object.

    Parameters
    ----------
    ax : mpl_Axes, optional
        The Matplotlib Axes object to rescale.

        If None, plt.gca() will be used.
    calc_outlier_bounds : Union[Callable, Tuple[Callable, Callable]], optional
        A function or a tuple of two functions to calculate the outlier bounds
        for the x and y data points.

        Each function should accept an array of data points and return a tuple
        of (lower, upper) bounds. If None, defaults to interquartile
        range-based calculation (`CalcBoundsIQR` with
        multiplier 1.5).
    pad : float, default 0.1
        How far should axes limits be padded beyond the non-outlier data range?

    Returns
    -------
    None

    Notes
    -----
    In cases where there are no outliers or all points are outliers, axes limits
    will not be adjusted In cases where non-outliers take on only a single
    value, padding will be applied relative to that value or, if zero, one.
    """
    if ax is None:
        ax = plt.gca()

    if calc_outlier_bounds is None:
        calc_outlier_bounds_x = CalcBoundsIQR(iqr_multiplier=1.5)
        calc_outlier_bounds_y = CalcBoundsIQR(iqr_multiplier=1.5)
    elif isinstance(calc_outlier_bounds, tuple):
        calc_outlier_bounds_x, calc_outlier_bounds_y = calc_outlier_bounds
    elif callable(calc_outlier_bounds):
        calc_outlier_bounds_x = calc_outlier_bounds
        calc_outlier_bounds_y = calc_outlier_bounds
    else:
        raise ValueError(
            "calc_outlier_bounds must be callable or tuple, not "
            f"{calc_outlier_bounds}",
        )

    x_points, y_points = [], []

    # Gather all points from the plot
    for collection in ax.collections:
        if isinstance(collection, PathCollection):
            x_points.extend(collection.get_offsets()[:, 0])
            y_points.extend(collection.get_offsets()[:, 1])

    # Calculate IQR bounds for x and y data
    x_lower, x_upper = calc_outlier_bounds_x(x_points)
    y_lower, y_upper = calc_outlier_bounds_y(y_points)

    # Filter outliers and determine new axis limits
    x_points_filtered = [x for x in x_points if x_lower <= x <= x_upper]
    y_points_filtered = [y for y in y_points if y_lower <= y <= y_upper]

    if len(x_points_filtered):
        x0, x1 = min(x_points_filtered), max(x_points_filtered)
        xpad = pad * ((x1 - x0) or x0 or 1)
        ax.set_xlim(x0 - xpad, x1 + xpad)
        assert np.ptp(ax.get_xlim()) or pad == 0
    if len(y_points_filtered):
        y0, y1 = min(y_points_filtered), max(y_points_filtered)
        ypad = pad * ((y1 - y0) or y0 or 1)
        ax.set_ylim(y0 - ypad, y1 + ypad)
        assert np.ptp(ax.get_ylim()) or pad == 0
