import matplotlib.pyplot as plt
import pytest
import seaborn as sns

import outset as otst


@pytest.mark.integration
def test_make_example_hueless():
    og = otst.OutsetGrid(
        data=sns.load_dataset("iris").dropna(),
        x="petal_width",
        y="petal_length",
        col="species",
        col_wrap=2,
        color=sns.color_palette()[1],
        marqueeplot_kwargs={
            "mark_glyph": otst.mark.MarkAlphabeticalBadges,
        },
        marqueeplot_source_kwargs={"leader_tweak": otst.tweak.TweakReflect()},
        marqueeplot_outset_kwargs={
            "leader_tweak": otst.tweak.TweakReflect(vertical=True)
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
    og = otst.OutsetGrid(
        data=sns.load_dataset("penguins").dropna(),
        x="bill_length_mm",
        y="bill_depth_mm",
        col="island",
        hue="species",
        marqueeplot_source_kwargs={
            "leader_tweak": otst.tweak.TweakSpreadArea(
                spread_factor=6, xlim=(47.5, 52)
            ),
        },
    )
    og.map_dataframe(
        sns.scatterplot, x="bill_length_mm", y="bill_depth_mm", legend=False
    )
    og.marqueeplot()
    og.set_axis_labels("bill length (mm)", "bill depth (mm)")
    og.add_legend()

    outpath = "/tmp/test_make_example_huefull.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


@pytest.mark.integration
def test_make_example_sourceless():
    og = otst.OutsetGrid(
        data=sns.load_dataset("penguins").dropna(),
        x="bill_length_mm",
        y="bill_depth_mm",
        col="island",
        hue="species",
        include_sourceplot=False,
        marqueeplot_source_kwargs={
            "leader_tweak": otst.tweak.TweakSpreadArea(
                spread_factor=6, xlim=(47.5, 52)
            ),
        },
    )
    og.map_dataframe(
        sns.scatterplot, x="bill_length_mm", y="bill_depth_mm", legend=False
    )
    og.marqueeplot()
    og.add_legend()

    outpath = "/tmp/test_make_example_sourceless.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


@pytest.mark.integration
def test_make_example_singleton():
    og = otst.OutsetGrid(
        data=[(73.5, 23.5, 78.5, 31.5)],
        color=sns.color_palette()[-1],
        marqueeplot_kwargs={
            "mark_glyph": otst.mark.MarkAlphabeticalBadges,
            "frame_outer_pad": 0.2,
            "frame_outer_pad_unit": "inches",
            "frame_face_kwargs": {"facecolor": "none"},
        },
    )
    og.broadcast(
        sns.scatterplot,
        data=sns.load_dataset("mpg").dropna(),
        x="horsepower",
        y="mpg",
        hue="origin",
        size="weight",
        sizes=(40, 400),
        alpha=0.5,
        palette="muted",
        legend=False,
        zorder=0,
    )
    og.marqueeplot(equalize_aspect=False)

    outpath = "/tmp/test_make_example_singleton.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
