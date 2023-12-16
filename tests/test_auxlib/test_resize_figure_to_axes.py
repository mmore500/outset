import pytest
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from outset._auxlib.resize_figure_to_axes_ import resize_figure_to_axes


def test_resize_figure_to_axes():
    # Setup a figure and axes
    fig, ax = plt.subplots()

    # Save the original size and position
    original_size = fig.get_size_inches()
    original_pos_bounds = ax.get_position().bounds
    original_pos_in_inches = [
        original_pos_bounds[0] * original_size[0],
        original_pos_bounds[1] * original_size[1],
        original_pos_bounds[2] * original_size[0],
        original_pos_bounds[3] * original_size[1],
    ]

    # Call the function
    resize_figure_to_axes(fig, ax)

    # Get the new size and position
    new_size = fig.get_size_inches()
    new_pos_bounds = ax.get_position().bounds
    new_pos_in_inches = [
        new_pos_bounds[0] * new_size[0],
        new_pos_bounds[1] * new_size[1],
        new_pos_bounds[2] * new_size[0],
        new_pos_bounds[3] * new_size[1],
    ]

    # Check that the size has changed
    assert new_size[0] != original_size[0]
    assert new_size[1] != original_size[1]

    # Check that the position in inches is approximately the same
    assert np.allclose(
        new_pos_in_inches, original_pos_in_inches, atol=0.01
    )  # allow a small tolerance
