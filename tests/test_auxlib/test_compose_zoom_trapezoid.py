import numpy as np
import pytest

from outset._auxlib.compose_zoom_trapezoid_ import compose_zoom_trapezoid


# smoke test
@pytest.mark.parametrize(
    "rect_xlim, rect_ylim, ax_xlim, ax_ylim, stretch",
    [
        ((0, 1), (0, 1), (0, 5), (0, 5), 0.14),
        ((-1, 0), (-1, 0), (-5, 0), (-5, 0), 0.2),
        ((1, 4), (2, 3), (0, 5), (0, 5), 0.1),
    ],
)
def test_compose_zoom_trapezoid(
    rect_xlim, rect_ylim, ax_xlim, ax_ylim, stretch
):
    result = compose_zoom_trapezoid(
        rect_xlim, rect_ylim, ax_xlim, ax_ylim, stretch
    )
    assert len(result) == 4
    assert all(len(item) == 2 for item in result)

    corner1, corner2 = zip(rect_xlim, reversed(rect_ylim))
    assert corner1 in result
    assert corner2 in result

    for item in result:
        assert (
            np.array_equal(item, corner1)
            or np.array_equal(item, corner2)
            or (item[0] > rect_xlim[1] and item[1] > rect_ylim[1])
        )

    def test_invalid_limits():
        with pytest.raises(ValueError):
            compose_zoom_trapezoid((1, 0), (0, 2), (0, 5), (0, 5), 0.14)
