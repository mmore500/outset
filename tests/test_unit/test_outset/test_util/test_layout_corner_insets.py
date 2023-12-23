import numpy as np
import pytest

from outset.util import layout_corner_insets


@pytest.mark.parametrize("transpose", [False, True])
@pytest.mark.parametrize(
    "num_insets, corner, expected_result",
    [
        (1, "NW", [(0.10, 0.70, 0.20, 0.20)]),
        (
            3,
            "NE",
            [
                (0.60, 0.80, 0.10, 0.10),
                (0.80, 0.80, 0.10, 0.10),
                (0.80, 0.60, 0.10, 0.10),
            ],
        ),
        (
            2,
            "SW",
            [
                (0.10, 0.10, 0.10, 0.10),
                (0.30, 0.10, 0.10, 0.10),
            ],
        ),
        (
            4,
            "SE",
            [
                (0.60, 0.30, 0.10, 0.10),
                (0.80, 0.30, 0.10, 0.10),
                (0.60, 0.10, 0.10, 0.10),
                (0.80, 0.10, 0.10, 0.10),
            ],
        ),
    ],
)
def test_layout_corner_insets(num_insets, corner, expected_result, transpose):
    result = layout_corner_insets(
        num_insets,
        corner,
        inset_grid_size=0.40,
        inset_margin_size=0.10,
        inset_pad_ratio=0.50,
        transpose=transpose,
    )
    if transpose and corner in ("NE", "SW"):
        expected_result = [
            (*reversed(coord[:2:]), *coord[2:]) for coord in expected_result
        ]
        expected_result = [*reversed(expected_result)]
    elif transpose:
        pass  # too complicated, not worth testing directly
    assert np.allclose(result, expected_result)


@pytest.mark.parametrize(
    "num_insets, corner, expected_result",
    [
        (1, "NW", [(0.10, 0.70, 0.20, 0.20)]),
        (
            3,
            "NE",
            [
                (0.60, 0.80, 0.10, 0.10),
                (0.80, 0.80, 0.10, 0.10),
                (0.80, 0.60, 0.10, 0.10),
            ],
        ),
        (
            2,
            "SW",
            [
                (0.10, 0.10, 0.10, 0.10),
                (0.30, 0.10, 0.10, 0.10),
            ],
        ),
        (
            4,
            "SE",
            [
                (0.60, 0.30, 0.10, 0.10),
                (0.80, 0.30, 0.10, 0.10),
                (0.60, 0.10, 0.10, 0.10),
                (0.80, 0.10, 0.10, 0.10),
            ],
        ),
    ],
)
def test_layout_corner_insets_tuple(num_insets, corner, expected_result):
    result = layout_corner_insets(
        num_insets,
        corner,
        inset_grid_size=(0.40, 0.40),
        inset_margin_size=(0.10, 0.10),
        inset_pad_ratio=(0.50, 0.50),
    )
    assert np.allclose(result, expected_result)
