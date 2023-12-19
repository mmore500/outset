import matplotlib.pyplot as plt
import pytest

from outset._auxlib.calc_outer_pad_ import calc_outer_pad


@pytest.mark.parametrize("pad_unit", ["axes", "figure", "inches"])
def test_calc_outer_pad(pad_unit: str):
    ax = plt.figure().add_subplot(111)
    pad = 0.1
    result = calc_outer_pad(ax, pad, pad_unit)
    assert isinstance(result, tuple)
