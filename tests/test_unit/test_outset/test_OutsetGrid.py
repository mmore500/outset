import matplotlib.cbook as mpl_cbook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from outset import inset_outsets, OutsetGrid
from outset import util as otst_util

# Sample data for testing
data = pd.DataFrame(
    {"x": [1, 2, 3, 4], "y": [1, 3, 2, 1], "outset": ["A", "B", "A", "B"]}
)


def test_OutsetGrid_one():
    # Create a sample dataframe
    data = pd.DataFrame({"x": [0.5], "y": [1], "outset": ["A"]})
    sns.scatterplot(data=data, x="x", y="y")
    g = OutsetGrid(
        data=data,
        x="x",
        y="y",
        marqueeplot_kws={
            "frame_inner_pad": 0.2,
        },
    ).marqueeplot()

    assert not g._is_inset()

    outpath = "/tmp/test_OutsetGrid_one.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_OutsetGrid_with_sourceplot_monochrome():
    # Create sample data with a 'outset' column for grouping
    data = pd.DataFrame(
        {
            "x": [0.825, 3.1, 0.5, 0.8, 2.2, 2],
            "y": [1.2, 0.8, 2.5, 2.3, 1.1, 3.7],
            "outset": [
                "group1",
                "group1",
                "group2",
                "group2",
                "group3",
                "group3",
            ],
        }
    )

    g = OutsetGrid(data=data, x="x", y="y", col="outset")
    g.marqueeplot()
    g.map_dataframe(sns.scatterplot, x="x", y="y", hue="outset", legend=False)

    assert not g._is_inset()

    outpath = "/tmp/test_OutsetGrid_with_sourceplot_monochrome.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_OutsetGrid_with_sourceplot_hue():
    # Create sample data with a 'outset' column for grouping
    data = pd.DataFrame(
        {
            "x": [0.825, 3.1, 0.5, 0.8, 2.2, 2],
            "y": [1.2, 0.8, 2.5, 2.3, 1.1, 3.7],
            "outset": [
                "group1",
                "group1",
                "group2",
                "group2",
                "group3",
                "group3",
            ],
        }
    )

    g = OutsetGrid(data=data, x="x", y="y", hue="outset")
    g.marqueeplot()
    g.map_dataframe(
        sns.scatterplot,
        x="x",
        y="y",
        marker=otst_util.SplitKwarg(outset="+", source="o"),
        legend=False,
    )

    assert not g._is_inset()

    outpath = "/tmp/test_OutsetGrid_with_sourceplot_hue.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_OutsetGrid_broadcast():
    with mpl_cbook.get_sample_data("grace_hopper.jpg") as image_file:
        image = plt.imread(image_file)

    og = OutsetGrid(
        data=[(0.42, 0.78, 0.62, 0.98), (0.10, 0.14, 0.40, 0.21)],
        aspect=0.9,
    )
    og.broadcast(
        plt.imshow, image, extent=(0, 1, 0, 1), origin="upper", zorder=-1
    )
    og.broadcast(
        plt.plot,
        [0.5],
        [0.85],
        color="red",
        linewidth=2,
        marker=otst_util.SplitKwarg(outset="+", source="o"),
        zorder=10,
    )
    og.marqueeplot()

    assert not og._is_inset()

    outpath = "/tmp/test_OutsetGrid_broadcast.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_OutsetGrid_broadcast_sourceless():
    with mpl_cbook.get_sample_data("grace_hopper.jpg") as image_file:
        image = plt.imread(image_file)

    og = OutsetGrid(
        data=[(0.42, 0.78, 0.62, 0.98), (0.10, 0.14, 0.40, 0.21)],
        aspect=0.9,
        include_sourceplot=False,
    )
    og.broadcast(
        plt.imshow, image, extent=(0, 1, 0, 1), origin="upper", zorder=-1
    )
    og.marqueeplot(equalize_aspect=False, preserve_aspect=True)

    assert not og._is_inset()

    outpath = "/tmp/test_OutsetGrid_broadcast_sourceless.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_OutsetGrid_empty():
    og = OutsetGrid([])
    og.broadcast(sns.scatterplot, x=[1], y=[2], legend=False)


def test_OutsetGrid_with_row_singleton():
    # Create sample data with a 'outset' column for grouping
    data = pd.DataFrame(
        {
            "x": [0.825, 3.1, 0.5, 0.8, 2.2, 2],
            "y": [1.2, 0.8, 2.5, 2.3, 1.1, 3.7],
            "baz": [0, 0, 0, 1, 1, 1],
            "outset": [
                "group1",
                "group1",
                "group2",
                "group2",
                "group3",
                "group3",
            ],
        }
    )

    g = OutsetGrid(
        data=data, x="x", y="y", col="outset", row="baz", row_order=[0]
    )
    g.marqueeplot()
    g.map_dataframe(sns.scatterplot, x="x", y="y", hue="outset", legend=False)

    assert not g._is_inset()

    outpath = "/tmp/test_OutsetGrid_with_row_singleton.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_OutsetGrid_no_marqueeplot():
    grid = OutsetGrid(
        data=[[(-3, 0), (3, 4)]] * 4,
        aspect=1.5,
    )
    inset_outsets(
        grid,
        insets=otst_util.layout_corner_insets(
            1,
            "NW",
            inset_grid_size=0.35,
        )
        + otst_util.layout_corner_insets(
            3,
            "SE",
            inset_pad_ratio=0.4,
            inset_margin_size=(0.0, 0.1),
        ),
        equalize_aspect=False,
        strip_ticks=False,
    )

    grid.broadcast(
        plt.plot,
        np.linspace(-3, 3, 100),
        np.sin(np.linspace(-3, 3, 100)),
    )

    outpath = "/tmp/test_OutsetGrid_no_marqueeplot.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_OutsetGrid_n():
    grid = OutsetGrid(
        data=3,
        aspect=1.5,
        col_wrap=2,
    )

    outpath = "/tmp/test_OutsetGrid_n.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
