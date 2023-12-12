from matplotlib import pyplot as plt

from outset._auxlib.calc_aspect_ import calc_aspect


def test_calc_aspect_square():
    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 1)
    assert calc_aspect(plt.gca()) == 1


def test_calc_aspect_tall():
    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 2)
    assert calc_aspect(plt.gca()) == 2


def test_calc_aspect_wide():
    plt.gca().set_xlim(-1, 3)
    plt.gca().set_ylim(0, 2)
    assert calc_aspect(plt.gca()) == 0.5
