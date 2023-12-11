import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.testing import decorators as mpl_testing_decorators

from outset import draw_outset, outsetplot

# Sample data for testing
data = pd.DataFrame(
    {"x": [1, 2, 3, 4], "y": [1, 3, 2, 1], "hue": ["A", "B", "A", "B"]}
)


@mpl_testing_decorators.check_figures_equal()
def test_outsetplot_vs_draw_outset(fig_test: plt.Figure, fig_ref: plt.Figure):
    # Using outsetplot
    ax_test = fig_test.subplots()
    outsetplot(data, x="x", y="y", ax=ax_test)

    # Expected output using draw_outset
    ax_ref = fig_ref.subplots()
    draw_outset(
        (1, 4),
        (1, 3),
        ax=ax_ref,
        frame_inner_pad=0.1,
        color=sns.color_palette()[0],
    )


@mpl_testing_decorators.check_figures_equal()
def test_outsetplot_vs_draw_outset_hue(
    fig_test: plt.Figure, fig_ref: plt.Figure
):
    palette = ["green", "red"]
    # Using outsetplot
    ax_test = fig_test.subplots()
    outsetplot(
        data,
        x="x",
        y="y",
        hue="hue",
        hue_order=["A", "B"],
        ax=ax_test,
        frame_inner_pad=0.0,
        palette=palette,
    )
    fig_test.savefig("/tmp/a.png")

    # Expected output using draw_outset
    ax_ref = fig_ref.subplots()
    draw_outset(
        (1, 3),
        (1, 2),
        ax=ax_ref,
        color=palette[0],
        frame_inner_pad=0.0,
    )
    draw_outset(
        (2, 4),
        (1, 3),
        ax=ax_ref,
        color=palette[1],
        frame_inner_pad=0.0,
    )
    fig_ref.savefig("/tmp/b.png")


def test_outsetplot_one():
    plt.clf()
    # Create a sample dataframe
    data = pd.DataFrame({"x": [0.5], "y": [1]})
    sns.scatterplot(data=data, x="x", y="y")
    outsetplot(
        data=data,
        x="x",
        y="y",
        frame_inner_pad=0.2,
    )
    outpath = "/tmp/test_outsetplot_one.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_outsetplot_several():
    plt.clf()
    _fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    # Create sample data with a 'hue' column for grouping
    data = pd.DataFrame(
        {
            "x": [0.825, 3.1, 0.5, 1.3, 2.2, 2],
            "y": [1.2, 0.8, 3.5, 2.3, 1.1, 3.7],
            "hue": ["group1", "group1", "group2", "group2", "group3", "group3"],
        }
    )

    sns.scatterplot(data=data, x="x", y="y", hue="hue", ax=ax)
    outsetplot(data=data, x="x", y="y", hue="hue", ax=ax, leader_stretch=0.0)

    outpath = "/tmp/test_outsetplot_several.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
