import matplotlib.cbook as mpl_cbook
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.testing import decorators as mpl_testing_decorators

from outset import draw_outset, OutsetGrid

# Sample data for testing
data = pd.DataFrame(
    {"x": [1, 2, 3, 4], "y": [1, 3, 2, 1], "outset": ["A", "B", "A", "B"]}
)


def test_OutsetGrid_one():
    plt.clf()
    # Create a sample dataframe
    data = pd.DataFrame({"x": [0.5], "y": [1], "outset": ["A"]})
    sns.scatterplot(data=data, x="x", y="y")
    OutsetGrid(
        data=data,
        x="x",
        y="y",
        outset="outset",
        frame_inner_pad=0.2,
    )
    outpath = "/tmp/test_OutsetGrid_one.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_OutsetGrid_with_sourceplot():
    plt.clf()
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

    g = OutsetGrid(data=data, x="x", y="y", outset="outset")
    g.map_dataframe_all(sns.scatterplot, x="x", y="y")

    outpath = "/tmp/test_OutsetGrid_with_sourceplot.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_OutsetGrid_broadcast():
    plt.clf()

    with mpl_cbook.get_sample_data("grace_hopper.jpg") as image_file:
        image = plt.imread(image_file)

    og = OutsetGrid(
        data=[(40, 60, 60, 80), (10, 40, 14, 21)],
        x="x",
        y="y",
        outset="outset",
        sourceplot_xlim=(0, 100),
        sourceplot_ylim=(0, 100),
    )
    og.broadcast(
        plt.imshow, image, extent=(0, 100, 0, 100), origin="upper", zorder=-1
    )
    plt.savefig("/tmp/test_OutsetGrid_broadcast.png")