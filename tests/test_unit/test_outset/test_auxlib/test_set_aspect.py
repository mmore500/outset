from matplotlib import pyplot as plt
import numpy as np

from outset._auxlib.calc_aspect_ import calc_aspect
from outset._auxlib.set_aspect_ import set_aspect


def test_set_aspect_square():
    # note: asserts inside of set_aspect will run
    plt.gca().set_ylim(0, 1)
    plt.gca().set_xlim(0, 1)
    set_aspect(plt.gca(), 0.5) == 1

    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(1, 2)
    set_aspect(plt.gca(), 2) == 1


def test_set_aspect_tall():
    # note: asserts inside of set_aspect will run
    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 2)
    set_aspect(plt.gca(), 1)

    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 2)
    set_aspect(plt.gca(), 4)

    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 2)
    set_aspect(plt.gca(), 0.5)


def test_set_aspect_wide():
    # note: asserts inside of set_aspect will run
    plt.gca().set_ylim(0, 1)
    plt.gca().set_xlim(0, 2)
    set_aspect(plt.gca(), 1)

    plt.gca().set_ylim(0, 1)
    plt.gca().set_xlim(0, 2)
    set_aspect(plt.gca(), 0.25)

    plt.gca().set_ylim(0, 1)
    plt.gca().set_xlim(0, 2)
    set_aspect(plt.gca(), 2)


def test_calc_aspect_nowarning():
    # should run without throwing a warning
    fig, main_ax = plt.subplots()
    main_ax.set_box_aspect(0.5)  # main figure and axes
    inset_ax = main_ax.inset_axes(
        [0.05, 0.75, 0.4, 0.2],
        xlim=[4, 5],
        ylim=[4, 5],
        xticklabels=[],
        yticklabels=[],
    )

    for ax in main_ax, inset_ax:
        ax.plot([0, 9], [0, 9])  # first example line
        ax.plot([0, 9], [1, 8])  # second example line

    main_ax.indicate_inset_zoom(inset_ax, edgecolor="blue")
    set_aspect(inset_ax, calc_aspect(main_ax))
