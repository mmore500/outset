import matplotlib.pyplot as plt

from outset import draw_outset


def test_draw_outset_one():
    plt.clf()
    draw_outset(
        xlim=(0, 1),
        ylim=(0, 2),
        color="mediumpurple",
        box_facecolor="white",
        box_linewidth=0.5,
        clip_on=False,
        hide_outer_spines=True,
        markersize=15,
        zoom_linestyle=":",
        zoom_linewidth=2,
        stretch=0.14,
    )
    outpath = "/tmp/test_draw_outset_one.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_draw_outset_several():
    _fig, ax = plt.subplots(figsize=(6, 4))

    draw_outset(
        xlim=[1, 1.25],
        ylim=(0.5, 1.5),
        ax=ax,
    )
    draw_outset(
        xlim=[2, 3.9],
        ylim=(0.5, 1.5),
        ax=ax,
    )
    draw_outset(
        xlim=[1, 2],
        ylim=(2, 3),
        ax=ax,
    )

    # Set limits and hide axes for a clean presentation
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)

    # Display the updated plot
    outpath = "/tmp/test_draw_outset_several.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
