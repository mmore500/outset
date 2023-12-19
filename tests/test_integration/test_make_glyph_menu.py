import itertools as it

from matplotlib import pyplot as plt
from matplotlib import patches as mpl_patches
import numpy as np
import pytest
import seaborn as sns

from outset import mark as otst_mark
from outset._auxlib.lighten_color_ import lighten_color


@pytest.mark.integration
def test_make_glyph_menu():
    markers = {
        "MarkAlphabeticalBadges\nstart='a'": otst_mark.MarkAlphabeticalBadges(
            "a"
        ),
        "MarkAlphabeticalBadges\nstart='A'": otst_mark.MarkAlphabeticalBadges(
            "A"
        ),
        "MarkArrow": otst_mark.MarkArrow(),
        "MarkInlaidAsterisk": otst_mark.MarkInlaidAsterisk(),
        "MarkMagnifyingGlass": otst_mark.MarkMagnifyingGlass(),
        "MarkNumericalBadges": otst_mark.MarkNumericalBadges(),
        "MarkRomanBadges\nupper=False": otst_mark.MarkRomanBadges(upper=False),
        "MarkRomanBadges\nupper=True": otst_mark.MarkRomanBadges(upper=True),
    }

    fig, axs = plt.subplots(ncols=len(markers), figsize=(len(markers), 1))
    for (name, mark), color, ax in zip(
        markers.items(), it.cycle(sns.color_palette()), np.array(axs).flat
    ):
        ax.set_axis_off()
        ax.add_patch(
            mpl_patches.Rectangle(
                (0, 0),
                1,
                1,
                edgecolor="none",
                facecolor=lighten_color(color),
            )
        )
        mark(0.25, 0.75, ax=ax, color=color)
        mark(0.6, 0.4, ax=ax, color=color)
        ax.set_title(name, color=color, loc="left", rotation=60)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    fig.tight_layout()

    # Save and print the path of the output image
    outpath = "/tmp/test_make_glyph_menu.png"
    plt.savefig(outpath, bbox_inches="tight")
    print(f"saved graphic to {outpath}")
