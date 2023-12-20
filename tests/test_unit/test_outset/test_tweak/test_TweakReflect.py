import numpy as np
import pytest

from outset.tweak import TweakReflect


test_data = [
    # Format: (horizontal, vertical, input_vertices, expected_output)
    (
        True,
        False,
        [(1, 1), (2, 2), (3, 3), (4, 4)],
        [(3, 1), (2, 2), (1, 3), (0, 4)],
    ),  # Horizontal reflection
    (
        False,
        True,
        [(1, 1), (2, 2), (3, 3), (4, 4)],
        [(1, 3), (2, 2), (3, 1), (4, 0)],
    ),  # Vertical reflection
    (
        True,
        True,
        [(1, 1), (2, 2), (3, 3), (4, 4)],
        [(3, 3), (2, 2), (1, 1), (0, 0)],
    ),  # Both reflections
    (
        None,
        None,
        [(1, 1), (2, 2), (3, 3), (4, 4)],
        [(3, 1), (2, 2), (1, 3), (0, 4)],
    ),  # Default (horizontal)
]


@pytest.mark.parametrize(
    "horizontal, vertical, input_vertices, expected_output", test_data
)
def test_TweakReflect(horizontal, vertical, input_vertices, expected_output):
    tweak = TweakReflect(horizontal=horizontal, vertical=vertical)
    result = tweak(input_vertices)
    assert np.allclose(result, expected_output)
