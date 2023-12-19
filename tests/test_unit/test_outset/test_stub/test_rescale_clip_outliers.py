import matplotlib.pyplot as plt
import numpy as np
import pytest
import seaborn as sns

from outset.stub import rescale_clip_outliers


def test_rescale_clip_outliers():
    np.random.seed(0)
    x = np.append(np.random.normal(0, 1, 100), [10, 15])  # with two outliers
    y = np.append(np.random.normal(0, 1, 100), [10, 20])

    fig, ax = plt.subplots()
    ax.scatter(x, y)

    # Apply the rescale_clip_outliers function
    xlim_, ylim_ = ax.get_xlim(), ax.get_ylim()
    rescale_clip_outliers(ax)
    assert xlim_ != ax.get_xlim() and ylim_ != ax.get_ylim()

    # Get new axis limits after rescaling
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()

    # Check if outliers are clipped
    assert len(x) - 10 <= sum(x0 <= x_ <= x1 for x_ in x) < len(x)
    assert len(y) - 10 <= sum(y0 <= y_ <= y1 for y_ in y) < len(y)


def test_rescale_clip_outliers_with_seaborn():
    np.random.seed(0)
    x = np.append(np.random.normal(0, 1, 100), [10, 15])  # with two outliers
    y = np.append(np.random.normal(0, 1, 100), [10, 20])
    data = {"x": x, "y": y}

    # Create a Seaborn plot
    ax = sns.scatterplot(x="x", y="y", data=data)

    # Apply the rescale_clip_outliers function
    xlim_, ylim_ = ax.get_xlim(), ax.get_ylim()
    rescale_clip_outliers(ax)
    assert xlim_ != ax.get_xlim() and ylim_ != ax.get_ylim()

    # Get new axis limits after rescaling
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()

    # Check if outliers are clipped
    assert len(x) - 10 <= sum(x0 <= x_ <= x1 for x_ in x) < len(x)
    assert len(y) - 10 <= sum(y0 <= y_ <= y1 for y_ in y) < len(y)


def test_rescale_clip_empty():
    fig, ax = plt.subplots()
    ax.scatter([], [])

    xlim_, ylim_ = ax.get_xlim(), ax.get_ylim()
    rescale_clip_outliers(ax)

    assert xlim_ == ax.get_xlim()
    assert ylim_ == ax.get_ylim()


@pytest.mark.parametrize("pad", [0.01, 0.1])
def test_rescale_clip_singleton(pad: float):
    fig, ax = plt.subplots()
    ax.scatter([3], [4])

    rescale_clip_outliers(
        calc_outlier_bounds=lambda x: (min(x), max(x)),
        pad=pad,
    )

    assert (3 - 3 * pad, 3 + 3 * pad) == ax.get_xlim()
    assert (4 - 4 * pad, 4 + 4 * pad) == ax.get_ylim()
