import matplotlib.cbook as mpl_cbook
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from outset import OutsetGrid

# Sample data for testing
data = pd.DataFrame(
    {"x": [1, 2, 3, 4], "y": [1, 3, 2, 1], "outset": ["A", "B", "A", "B"]}
)


def test_OutsetGrid_one():
    # Create a sample dataframe
    data = pd.DataFrame({"x": [0.5], "y": [1], "outset": ["A"]})
    sns.scatterplot(data=data, x="x", y="y")
    OutsetGrid(
        data=data,
        x="x",
        y="y",
        outset="outset",
        marqueeplot_kwargs={
            "frame_inner_pad": 0.2,
        },
    ).marqueeplot()
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

    g = OutsetGrid(data=data, x="x", y="y", outset="outset")
    g.marqueeplot()
    g.map_dataframe(sns.scatterplot, x="x", y="y", hue="outset", legend=False)

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
    g.map_dataframe(sns.scatterplot, x="x", y="y", legend=False)

    outpath = "/tmp/test_OutsetGrid_with_sourceplot_hue.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_OutsetGrid_broadcast():
    with mpl_cbook.get_sample_data("grace_hopper.jpg") as image_file:
        image = plt.imread(image_file)

    og = OutsetGrid(
        data=[(40, 60, 60, 80), (10, 40, 14, 21)],
        col=True,
        hue=True,
    )
    og.broadcast(
        plt.imshow, image, extent=(0, 100, 0, 100), origin="upper", zorder=-1
    )
    og.marqueeplot()
    plt.savefig("/tmp/test_OutsetGrid_broadcast.png")
