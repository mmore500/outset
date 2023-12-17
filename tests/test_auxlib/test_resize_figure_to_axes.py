import pytest
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from outset._auxlib.resize_figure_to_axes_ import resize_figure_to_axes


def test_resize_figure_to_axes():
    # Setup a figure and axes
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax2.set_position([0.2, 0.2, 0.2, 0.2])

    # Save the original size and position
    before_size = fig.get_size_inches()
    before_pos_bounds = ax1.get_position().bounds
    before_pos_in_inches = [
        before_pos_bounds[0] * before_size[0],
        before_pos_bounds[1] * before_size[1],
        before_pos_bounds[2] * before_size[0],
        before_pos_bounds[3] * before_size[1],
    ]

    # Call the function
    resize_figure_to_axes(fig, ax1)

    # Get the new size and position
    after_size = fig.get_size_inches()
    after_pos_bounds = ax1.get_position().bounds
    after_pos_in_inches = [
        after_pos_bounds[0] * after_size[0],
        after_pos_bounds[1] * after_size[1],
        after_pos_bounds[2] * after_size[0],
        after_pos_bounds[3] * after_size[1],
    ]

    # Check that the size has changed
    assert tuple(after_size) != tuple(before_size)

    # Check that axes position in inches is approximately the same
    assert np.allclose(after_pos_in_inches, before_pos_in_inches, atol=0.01)
