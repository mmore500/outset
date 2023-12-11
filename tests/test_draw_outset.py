import matplotlib.pyplot as plt

from outset import draw_outset


def test_draw_outset_one():
    plt.clf()
    draw_outset(
        frame_xlim=(0, 1),
        frame_ylim=(0, 2),
        color="mediumpurple",
        clip_on=False,
        frame_linewidth=0.5,
        hide_outer_spines=True,
        leader_stretch=0.14,
        mark_glyph_kwargs=dict(markersize=15),
        leader_linestyle=":",
        leader_linewidth=2,
    )
    outpath = "/tmp/test_draw_outset_one.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_draw_outset_no_leader():
    plt.clf()
    draw_outset(
        frame_xlim=(0, 1),
        frame_ylim=(0, 2),
        color="mediumpurple",
        leader_stretch=0.0,
    )
    outpath = "/tmp/test_draw_outset_no_leader.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_draw_outset_several():
    _fig, ax = plt.subplots(figsize=(6, 4))

    # Set limits and hide axes for a clean presentation
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)

    draw_outset(
        frame_xlim=[1, 1.25],
        frame_ylim=(0.5, 1.5),
        ax=ax,
    )
    draw_outset(
        frame_xlim=[2, 3.9],
        frame_ylim=(0.5, 1.5),
        ax=ax,
    )
    draw_outset(
        frame_xlim=[1, 2],
        frame_ylim=(2, 3),
        ax=ax,
    )

    # Display the updated plot
    outpath = "/tmp/test_draw_outset_several.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
