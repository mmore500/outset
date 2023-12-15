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

    # Apply the equalize_aspect function
    new_aspect = equalize_aspect([ax1, ax2])

    # Calculate aspect ratios after equalization
    aspect_ax1 = calc_aspect(ax1)
    aspect_ax2 = calc_aspect(ax2)

    # Check if both aspect ratios are equal and match the calculated new aspect ratio
    assert aspect_ax1 == pytest.approx(
        new_aspect
    ), "Aspect ratios are not equalized"
    assert aspect_ax2 == pytest.approx(
        new_aspect
    ), "Aspect ratios are not equalized"

    original_aspect1 = 20 / 10
    original_aspect2 = 10 / 10
    expected_new_aspect = (original_aspect1 * original_aspect2) ** 0.5
    assert new_aspect == pytest.approx(
        expected_new_aspect
    ), "New aspect ratio is not the geometric mean of the original aspect ratios"


def test_equalize_aspect_singleton():
    plt.gca().set_xlim(0, 10)
    plt.gca().set_ylim(1, 6)
    assert equalize_aspect([plt.gca()]) == 0.5
    assert plt.gca().get_xlim() == (0, 10)
    assert plt.gca().get_ylim() == (1, 6)


@pytest.mark.parametrize("physical", [True, False])
def test_equalize_aspect_empty(physical: bool):
    assert equalize_aspect([]) == 1.0


def test_equalize_aspect_physical():
    # Create a figure with two subplots having different aspect ratios
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 20)  # Aspect ratio 2:1
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)  # Aspect ratio 1:1

    # Apply the equalize_aspect function
    new_aspect = equalize_aspect([ax1, ax2], physical=True)

    # Calculate aspect ratios after equalization
    aspect_ax1 = calc_aspect(ax1, physical=True)
    aspect_ax2 = calc_aspect(ax2, physical=True)

    # Check if both aspect ratios are equal and match the calculated new aspect ratiox
    assert aspect_ax1 == pytest.approx(new_aspect)
    assert aspect_ax2 == pytest.approx(new_aspect)


def test_equalize_aspect_singleton_physical():
    plt.clf()
    plt.gca().set_xlim(0, 10)
    plt.gca().set_ylim(1, 6)
    assert equalize_aspect([plt.gca()], physical=True)
