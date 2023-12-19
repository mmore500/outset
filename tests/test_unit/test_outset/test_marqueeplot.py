import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.testing import decorators as mpl_testing_decorators

from outset import draw_marquee, marqueeplot
from outset.mark import mark_magnifying_glass

# Sample data for testing
data = pd.DataFrame(
    {"x": [1, 2, 3, 4], "y": [1, 3, 2, 1], "outset": ["A", "B", "A", "B"]}
)


@mpl_testing_decorators.check_figures_equal()
def test_marqueeplot_vs_draw_marquee(fig_test: plt.Figure, fig_ref: plt.Figure):
    # Using marqueeplot
    ax_test = fig_test.subplots()
    marqueeplot(
        data, x="x", y="y", ax=ax_test, mark_glyph=mark_magnifying_glass
    )

    # Expected output using draw_marquee
    ax_ref = fig_ref.subplots()
    ax_ref.set_xlim(*ax_test.get_xlim())
    ax_ref.set_ylim(*ax_test.get_ylim())
    draw_marquee(
        (1, 4),
        (1, 3),
        ax=ax_ref,
        color=sns.color_palette()[0],
        frame_inner_pad=0.1,
        frame_outer_pad=0.0,
    )


@mpl_testing_decorators.check_figures_equal()
def test_marqueeplot_vs_draw_marquee_split(
    fig_test: plt.Figure, fig_ref: plt.Figure
):
    palette = ["green", "red"]
    # Using marqueeplot
    ax_test = fig_test.subplots()
    marqueeplot(
        data,
        x="x",
        y="y",
        mark_glyph=mark_magnifying_glass,
        outset="outset",
        outset_order=["A", "B"],
        hue="outset",
        ax=ax_test,
        frame_inner_pad=0.0,
        frame_outer_pad=0.0,
        palette=palette,
    )

    # Expected output using draw_marquee
    ax_ref = fig_ref.subplots()
    ax_ref.set_xlim(*ax_test.get_xlim())
    ax_ref.set_ylim(*ax_test.get_ylim())
    draw_marquee(
        (1, 3),
        (1, 2),
        ax=ax_ref,
        color=palette[0],
        frame_inner_pad=0.0,
        frame_outer_pad=0.0,
    )
    draw_marquee(
        (2, 4),
        (1, 3),
        ax=ax_ref,
        color=palette[1],
        frame_inner_pad=0.0,
        frame_outer_pad=0.0,
    )
    ax_ref.set_xlim(*ax_test.get_xlim())
    ax_ref.set_ylim(*ax_test.get_ylim())


def test_marqueeplot_one():
    # Create a sample dataframe
    data = pd.DataFrame({"x": [0.5], "y": [1]})
    sns.scatterplot(data=data, x="x", y="y")
    marqueeplot(
        data=data,
        x="x",
        y="y",
        frame_inner_pad=0.2,
    )
    outpath = "/tmp/test_marqueeplot_one.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_marqueeplot_several():
    _fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    # Create sample data with a 'outset' column for grouping
    data = pd.DataFrame(
        {
            "x": [0.825, 3.1, 0.5, 1.3, 2.2, 2],
            "y": [1.2, 0.8, 3.5, 2.3, 1.1, 3.7],
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

    sns.scatterplot(data=data, x="x", y="y", hue="outset", ax=ax)
    marqueeplot(
        data=data, x="x", y="y", outset="outset", ax=ax, leader_stretch=0.0
    )

    outpath = "/tmp/test_marqueeplot_several.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
