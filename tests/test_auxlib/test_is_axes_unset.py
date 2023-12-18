import matplotlib.pyplot as plt

from outset._auxlib.is_axes_unset_ import is_axes_unset


def test_empty_axis():
    fig, ax = plt.subplots()
    assert is_axes_unset(ax) is True


def test_empty_axis_gca():
    assert is_axes_unset(plt.gca()) is True


def test_axis_with_children():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])  # Add a line plot to the axis
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    assert is_axes_unset(ax) is False


def test_manually_set_limits():
    fig, ax = plt.subplots()
    ax.set_xlim(0.0, 2.0)
    assert is_axes_unset(ax) is False


def test_auto_set_limits():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 2])  # Add a line plot to the axis
    assert is_axes_unset(ax) is False
