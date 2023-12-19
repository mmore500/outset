from outset._auxlib.calc_aspect_ import calc_aspect
from outset._auxlib.equalize_aspect_ import equalize_aspect

from matplotlib import pyplot as plt
import pytest


def test_equalize_aspect():
    # Create a figure with two subplots having different aspect ratios
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 20)  # Aspect ratio 2:1
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)  # Aspect ratio 1:1

    before_aspect1 = calc_aspect(ax1)
    before_aspect2 = calc_aspect(ax2)

    # Apply the equalize_aspect function
    after_aspect = equalize_aspect([ax1, ax2])

    # Calculate aspect ratios after equalization
    after_aspect_ax1 = calc_aspect(ax1)
    after_aspect_ax2 = calc_aspect(ax2)

    # Check if both aspect ratios are equal and match the calculated new aspect ratio
    assert after_aspect_ax1 == pytest.approx(after_aspect)
    assert after_aspect_ax2 == pytest.approx(after_aspect)

    expected_after_aspect = (before_aspect1 * before_aspect2) ** 0.5
    assert after_aspect == pytest.approx(expected_after_aspect)


def test_equalize_aspect_singleton():
    plt.gca().set_xlim(0, 10)
    plt.gca().set_ylim(1, 6)
    aspect_before = calc_aspect(plt.gca())
    assert equalize_aspect([plt.gca()]) == aspect_before
    assert plt.gca().get_xlim() == (0, 10)
    assert plt.gca().get_ylim() == (1, 6)


def test_equalize_aspect_empty():
    assert equalize_aspect([]) == 1.0
