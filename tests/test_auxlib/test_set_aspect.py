from matplotlib import pyplot as plt

from outset._auxlib.set_aspect_ import set_aspect


def test_calc_aspect_square():
    plt.gca().set_ylim(0, 1)
    plt.gca().set_xlim(0, 1)
    set_aspect(plt.gca(), 0.5) == 1
    assert plt.gca().get_xlim() == (-0.5, 1.5)
    assert plt.gca().get_ylim() == (0, 1)

    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(1, 2)
    set_aspect(plt.gca(), 2) == 1
    assert plt.gca().get_xlim() == (0, 1)
    assert plt.gca().get_ylim() == (0.5, 2.5)


def test_calc_aspect_tall():
    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 2)
    set_aspect(plt.gca(), 1)
    assert plt.gca().get_xlim() == (-0.5, 1.5)
    assert plt.gca().get_ylim() == (0, 2)

    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 2)
    set_aspect(plt.gca(), 4)
    assert plt.gca().get_xlim() == (0, 1)
    assert plt.gca().get_ylim() == (-1, 3)

    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 2)
    set_aspect(plt.gca(), 0.5)
    assert plt.gca().get_ylim() == (0, 2)
    assert plt.gca().get_xlim() == (-1.5, 2.5)


def test_calc_aspect_wide():
    plt.gca().set_ylim(0, 1)
    plt.gca().set_xlim(0, 2)
    set_aspect(plt.gca(), 1)
    assert plt.gca().get_ylim() == (-0.5, 1.5)
    assert plt.gca().get_xlim() == (0, 2)

    plt.gca().set_ylim(0, 1)
    plt.gca().set_xlim(0, 2)
    set_aspect(plt.gca(), 1 / 4)
    assert plt.gca().get_ylim() == (0, 1)
    assert plt.gca().get_xlim() == (-1, 3)

    plt.gca().set_ylim(0, 1)
    plt.gca().set_xlim(0, 2)
    set_aspect(plt.gca(), 1 / 0.5)
    assert plt.gca().get_xlim() == (0, 2)
    assert plt.gca().get_ylim() == (-1.5, 2.5)
