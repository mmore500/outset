import typing

import pytest
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from slugify import slugify

import outset
from outset._auxlib.resize_figure_to_axes_ import resize_figure_to_axes


@pytest.mark.parametrize(
    "plot", [sns.scatterplot, outset.marqueeplot, lambda *args, **kwargs: None]
)
def test_resize_figure_to_axes(plot: typing.Callable):
    plt.close("all")
    # Setup a figure and axes
    fig, (ax1, ax2) = plt.subplots(1, 2)
    plot(
        data=pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 2]}),
        ax=ax1,
        x="x",
        y="y",
    )

    outpath = f"/tmp/test_resize_figure_to_axes_{slugify(plot.__name__)}_a.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")

    ax2.set_position([0.2, 0.2, 0.2, 0.2])

    outpath = f"/tmp/test_resize_figure_to_axes_{slugify(plot.__name__)}_b.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")

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

    outpath = f"/tmp/test_resize_figure_to_axes_{slugify(plot.__name__)}_c.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")

    # Check that the size has changed
    assert tuple(after_size) != tuple(before_size)

    # Check that axes position in inches is approximately the same
    assert np.allclose(after_pos_in_inches, before_pos_in_inches, atol=0.01)


@pytest.mark.parametrize(
    "plot", [sns.scatterplot, lambda *args, **kwargs: None]
)
def test_resize_figure_to_axes_FacetGrid(plot: typing.Callable):
    plt.close("all")
    # Setup a figure and axes
    g = sns.FacetGrid(
        pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 2], "col": [0, 1, 1]}),
        col="col",
    )
    g.map(plot, "x", "y")

    g.axes.flat[1].set_position([0.2, 0.2, 0.2, 0.2])

    # Save the original size and position
    before_size = g.figure.get_size_inches()
    before_pos_bounds = g.axes.flat[0].get_position().bounds
    before_pos_in_inches = [
        before_pos_bounds[0] * before_size[0],
        before_pos_bounds[1] * before_size[1],
        before_pos_bounds[2] * before_size[0],
        before_pos_bounds[3] * before_size[1],
    ]

    # Call the function
    resize_figure_to_axes(g.figure, g.axes.flat[0])

    # Get the new size and position
    after_size = g.figure.get_size_inches()
    after_pos_bounds = g.axes.flat[0].get_position().bounds
    after_pos_in_inches = [
        after_pos_bounds[0] * after_size[0],
        after_pos_bounds[1] * after_size[1],
        after_pos_bounds[2] * after_size[0],
        after_pos_bounds[3] * after_size[1],
    ]

    outpath = (
        f"/tmp/test_resize_figure_to_axes_facet_{slugify(plot.__name__)}.png"
    )
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")

    # Check that the size has changed
    assert tuple(after_size) != tuple(before_size)

    # Check that axes position in inches is approximately the same
    assert np.allclose(after_pos_in_inches, before_pos_in_inches, atol=0.01)


@pytest.mark.parametrize(
    "plot", [sns.scatterplot, lambda *args, **kwargs: None]
)
def test_resize_figure_to_axes_OutsetGrid(plot: typing.Callable):
    plt.close("all")
    # Setup a figure and axes
    g = outset.OutsetGrid(
        pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 2], "col": [1, 1, 1]}),
        col="col",
        x="x",
        y="y",
    )
    g.map_dataframe(plot, x="x", y="y", legend=False)

    outpath = (
        f"/tmp/test_resize_figure_to_axes_outset_{slugify(plot.__name__)}_a.png"
    )
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")

    g.axes.flat[1].set_position([0.2, 0.2, 0.2, 0.2])

    # Save the original size and position
    outpath = (
        f"/tmp/test_resize_figure_to_axes_outset_{slugify(plot.__name__)}_b.png"
    )
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")

    before_size = g.figure.get_size_inches()
    before_pos_bounds = g.axes.flat[0].get_position().bounds
    before_pos_in_inches = [
        before_pos_bounds[0] * before_size[0],
        before_pos_bounds[1] * before_size[1],
        before_pos_bounds[2] * before_size[0],
        before_pos_bounds[3] * before_size[1],
    ]

    # Call the function
    resize_figure_to_axes(g.figure, g.axes.flat[0])

    # Get the new size and position
    after_size = g.figure.get_size_inches()
    after_pos_bounds = g.axes.flat[0].get_position().bounds
    after_pos_in_inches = [
        after_pos_bounds[0] * after_size[0],
        after_pos_bounds[1] * after_size[1],
        after_pos_bounds[2] * after_size[0],
        after_pos_bounds[3] * after_size[1],
    ]

    g.marqueeplot()

    outpath = (
        f"/tmp/test_resize_figure_to_axes_outset_{slugify(plot.__name__)}_c.png"
    )
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")

    # Check that the size has changed
    assert tuple(after_size) != tuple(before_size)

    # # Check that axes position in inches is approximately the same
    assert np.allclose(after_pos_in_inches, before_pos_in_inches, atol=0.01)
