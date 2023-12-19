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
