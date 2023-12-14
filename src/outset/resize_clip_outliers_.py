import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection
import numpy as np


def _calculate_iqr_bounds(data, multiplier):
    quartile1, quartile3 = np.percentile(data, [25, 75])
    iqr = quartile3 - quartile1
    lower_bound = quartile1 - (multiplier * iqr)
    upper_bound = quartile3 + (multiplier * iqr)
    return lower_bound, upper_bound


def resize_clip_outliers(ax, iqr_multiplier=1.5):
    x_points, y_points = [], []

    # Gather all points from the plot
    for collection in ax.collections:
        if isinstance(collection, PathCollection):
            x_points.extend(collection.get_offsets()[:, 0])
            y_points.extend(collection.get_offsets()[:, 1])

    # Calculate IQR bounds for x and y data
    x_lower, x_upper = _calculate_iqr_bounds(x_points, iqr_multiplier)
    y_lower, y_upper = _calculate_iqr_bounds(y_points, iqr_multiplier)

    # Filter outliers and determine new axis limits
    x_points_filtered = [x for x in x_points if x_lower <= x <= x_upper]
    y_points_filtered = [y for y in y_points if y_lower <= y <= y_upper]

    if x_points_filtered:
        ax.set_xlim(min(x_points_filtered), max(x_points_filtered))
    if y_points_filtered:
        ax.set_ylim(min(y_points_filtered), max(y_points_filtered))
