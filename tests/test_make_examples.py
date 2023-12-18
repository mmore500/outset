import matplotlib.pyplot as plt
import pytest
import seaborn as sns

import outset


@pytest.mark.integration
def test_make_example_hueless():
    og = outset.OutsetGrid(
        data=sns.load_dataset("iris").dropna(),
        x="petal_width",
        y="petal_length",
        col="species",
        col_wrap=2,
        color=sns.color_palette()[1],
        marqueeplot_kwargs={
            "mark_glyph": outset.MarkAlphabeticalBadges,
        },
    )
    og.map_dataframe(
        sns.kdeplot, x="petal_width", y="petal_length", legend=False, zorder=0
    )
    og.map_dataframe_outset(
        sns.scatterplot,
        x="petal_width",
        y="petal_length",
        legend=False,
        zorder=0,
    )
    og.marqueeplot()

    outpath = "/tmp/test_make_example_hueless.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


@pytest.mark.integration
def test_make_example_huefull():
    og = outset.OutsetGrid(
        data=sns.load_dataset("penguins").dropna(),
        x="bill_length_mm",
        y="bill_depth_mm",
        col="island",
        hue="species",
    )
    og.map_dataframe(
        sns.scatterplot, x="bill_length_mm", y="bill_depth_mm", legend=False
    )
    og.marqueeplot()
    og.add_legend()

    outpath = "/tmp/test_make_example_huefull.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
