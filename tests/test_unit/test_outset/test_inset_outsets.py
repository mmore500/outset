import matplotlib.pyplot as plt
import pandas as pd
import pytest
import seaborn as sns

from outset import inset_outsets, OutsetGrid

# Sample data for testing
data = pd.DataFrame(
    {
        "x": [1, 10, 1.5, 4, 7, 7.4, 4, 5],
        "y": [1.5, 3, 2, 11, 2.05, 2, 4, 5],
        "outset": ["A", "B", "A", "B", "C", "C", "D", "D"],
    }
)


def test_inset_outsets_one():
    # Create a sample dataframe
    og = OutsetGrid(
        data=data,
        x="x",
        y="y",
        col="outset",
        col_order=["A"],
        marqueeplot_kwargs={
            "frame_inner_pad": 0.1,
            "frame_outer_pad": 0.3,
        },
    )
    og.map_dataframe(sns.scatterplot, x="x", y="y")
    og.marqueeplot()
    inset_outsets(og, [(0.8, 0.6, 0.1, 0.1)])
    outpath = "/tmp/test_inset_outsets_one.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_inset_outsets_two():
    # Create a sample dataframe
    og = OutsetGrid(
        data=data,
        x="x",
        y="y",
        col="outset",
        col_order=["A", "C"],
        marqueeplot_kwargs={
            "frame_inner_pad": 0.3,
            "frame_outer_pad": 0.1,
            "frame_outer_pad_unit": "axes",
        },
        marqueeplot_outset_kwargs={
            "frame_outer_pad": 0.2,
            "frame_outer_pad_unit": "inches",
            "mark_glyph_kwargs": {"markersize": 16},
        },
        aspect=1.2,
    )
    og.map_dataframe(sns.scatterplot, x="x", y="y", hue="outset", legend=False)
    inset_outsets(
        og,
        [
            (0.1, 0.5, 0.3, 0.3),
            (0.5, 0.5, 0.5, 0.3),
        ],
    )
    og.marqueeplot()

    outpath = "/tmp/test_inset_outsets_two.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


@pytest.mark.parametrize("corner", ["NE", "NW", "SE", "SW"])
def test_inset_outsets_three(corner: str):
    # Create a sample dataframe
    og = OutsetGrid(
        data=data,
        x="x",
        y="y",
        col="outset",
        col_order=["A", "B", "C"],
        marqueeplot_kwargs={
            "frame_inner_pad": 0.1,
            "frame_outer_pad": 0.1,
            "frame_outer_pad_unit": "axes",
        },
        marqueeplot_outset_kwargs={
            "frame_outer_pad": 0.1,
            "frame_outer_pad_unit": "inches",
            "mark_glyph_kwargs": {"markersize": 16},
        },
        aspect=1.2,
    )
    og.map_dataframe(
        sns.scatterplot, x="x", y="y", hue="outset", legend=False, zorder=-1
    )
    inset_outsets(og, insets=corner, strip_spines=False)
    og.equalize_aspect()
    og.marqueeplot()

    assert og._is_inset()

    outpath = f"/tmp/test_inset_outsets_three_{corner}.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
