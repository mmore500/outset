from matplotlib import pyplot as plt
import pandas as pd
import pytest

import outset


@pytest.mark.integration
def test_make_taxonomy():
    # Create sample data with a 'outset' column for grouping
    data = pd.DataFrame(
        {
            "x": [0, 2, 5, 6],
            "y": [1, 4, 3, 9],
            "outset": [
                "group1",
                "group1",
                "group2",
                "group2",
            ],
        }
    )

    g = outset.OutsetGrid(data=data, x="x", y="y", col="outset", hue="outset")
    g.marqueeplot()

    g.source_axes.annotate(
        "callout mark",
        xy=(3, 5),
        xytext=(3.5, 4),
        horizontalalignment="left",
        arrowprops=dict(arrowstyle="->", lw=1),
    )
    g.source_axes.annotate(
        "callout leader",
        xy=(2.5, 4),
        xytext=(3.5, 3),
        horizontalalignment="left",
        arrowprops=dict(arrowstyle="->", lw=1),
    )
    g.source_axes.annotate(
        "frame",
        xy=(1, 2),
        xytext=(1, 2),
        horizontalalignment="center",
    )
    g.source_axes.annotate(
        "marquee",
        xy=(1.5, 6),
        xytext=(1.5, 6.5),
        ha="center",
        va="bottom",
        arrowprops=dict(
            arrowstyle="-[, widthB=4.0, lengthB=1.0", lw=2.0, color="k"
        ),
    )
    g.broadcast_source(lambda ax: ax.set_title("source axes"))
    g.broadcast_outset(lambda ax: ax.set_title("outset axes"))

    outpath = "/tmp/test_taxonomy_outset.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")

    outset.inset_outsets(g, insets="NW")
    g.source_axes.annotate(
        "inset outset axes",
        xy=(1.5, 10.9),
        xytext=(1.5, 11),
        ha="center",
        va="bottom",
        arrowprops=dict(
            arrowstyle="-[, widthB=5, lengthB=0.5", lw=2.0, color="k"
        ),
    )
    outset.inset_outsets(g, insets="NW")
    g.source_axes.annotate(
        "",
        xy=(2.5, 11.9),
        xytext=(2.5, 12),
        ha="center",
        va="bottom",
        arrowprops=dict(
            arrowstyle="-[, widthB=10, lengthB=0.5", lw=2.0, color="k"
        ),
        annotation_clip=False,
    )

    # additional annotations for other marquees
    # g.source_axes.annotate(
    #     "marquee",
    #     xy=(1.5, 10.5),
    #     xytext=(4.5, 11.5),
    #     ha="center",
    #     arrowprops=dict(arrowstyle="->", lw=1),
    # )
    # g.source_axes.annotate(
    #     "",
    #     xy=(3.25, 10.75),
    #     xytext=(4, 11.25),
    #     ha="center",
    #     arrowprops=dict(arrowstyle="->", lw=1),
    # )
    # g.source_axes.annotate(
    #     "",
    #     xy=(5.5, 8),
    #     xytext=(4.5, 11.25),
    #     ha="center",
    #     arrowprops=dict(arrowstyle="->", lw=1),
    # )

    outpath = "/tmp/test_taxonomy_inset.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
