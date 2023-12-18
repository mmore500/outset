from matplotlib import pyplot as plt
import pytest

from outset._auxlib.calc_aspect_ import calc_aspect


def test_calc_aspect_square_physical():
    fig, ax = plt.subplots(figsize=(6, 6))  # Create a 6x6 inch figure
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    assert calc_aspect(ax) == pytest.approx(1, abs=0.1)


def test_calc_aspect_tall_physical():
    fig, ax = plt.subplots(figsize=(6, 12))  # Create a 6x12 inch figure
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    assert calc_aspect(ax) == pytest.approx(2, abs=0.1)


def test_calc_aspect_wide_physical():
    fig, ax = plt.subplots(figsize=(12, 6))  # Create a 12x6 inch figure
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    assert calc_aspect(ax) == pytest.approx(0.5, abs=0.1)


def test_calc_aspect_square():
    fig, ax = plt.subplots(figsize=(6, 6))  # Create a 6x6 inch figure
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    assert calc_aspect(ax) == pytest.approx(1, abs=0.1)


def test_calc_aspect_tall():
    fig, ax = plt.subplots(figsize=(6, 6))  # Create a 6x6 inch figure
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2)
    assert calc_aspect(ax) == pytest.approx(0.5, abs=0.1)


def test_calc_aspect_wide():
    fig, ax = plt.subplots(figsize=(6, 6))  # Create a 6x6 inch figure
    ax.set_xlim(-1, 3)
    ax.set_ylim(0, 2)
    assert calc_aspect(ax) == pytest.approx(2, abs=0.1)
