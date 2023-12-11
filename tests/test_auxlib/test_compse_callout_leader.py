import numpy as np
import pytest

from outset._auxlib.compose_callout_leader_ import compose_callout_leader


# smoke test
@pytest.mark.parametrize(
    "rect_xlim, rect_ylim, ax_xlim, ax_ylim, stretch",
    [
        ((0, 1), (0, 1), (0, 5), (0, 5), 0.14),
        ((-1, 0), (-1, 0), (-5, 0), (-5, 0), 0.2),
        ((1, 4), (2, 3), (0, 5), (0, 5), 0.1),
    ],
)
def test_compose_callout_leader(
    rect_xlim, rect_ylim, ax_xlim, ax_ylim, stretch
):
    result = compose_callout_leader(
        rect_xlim, rect_ylim, ax_xlim, ax_ylim, stretch
    )
    assert len(result) == 4
    assert all(len(item) == 2 for item in result)

    _lowerleft, upperright = zip(rect_xlim, rect_ylim)
    upperleft, lowerright = zip(rect_xlim, reversed(rect_ylim))
    assert upperleft in result
    assert upperright in result
    assert lowerright in result

    for item in result:
        assert (
            np.array_equal(item, upperleft)
            or np.array_equal(item, lowerright)
            or np.array_equal(item, upperright)
            or (item[0] > rect_xlim[1] and item[1] > rect_ylim[1])
        )

    def test_invalid_limits():
        with pytest.raises(ValueError):
            compose_callout_leader((1, 0), (0, 2), (0, 5), (0, 5), 0.14)
