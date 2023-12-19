import typing

import numpy as np
import pytest

from outset.tweak import TweakSpreadArea


def test_tweak_spread_area_init():
    # Test initialization with default parameters
    tsa_default = TweakSpreadArea()
    assert tsa_default._spread_factor == (2.0, 2.0)
    assert tsa_default._xlim is None
    assert tsa_default._ylim is None

    # Test initialization with custom parameters
    tsa_custom = TweakSpreadArea(
        spread_factor=(1.5, 2.5), xlim=(0, 10), ylim=(0, 5)
    )
    assert tsa_custom._spread_factor == (1.5, 2.5)
    assert tsa_custom._xlim == (0, 10)
    assert tsa_custom._ylim == (0, 5)


@pytest.mark.parametrize(
    "outer_vertex_and_result",
    zip([(-1, 0), (5, 2), (9, 4)], [(-1, -2.5), (5, 1.5), (13, 5.5)]),
)
def test_tweak_spread_area_call(
    outer_vertex_and_result: typing.Tuple[typing.Tuple[float, float]]
):
    tsa = TweakSpreadArea(spread_factor=(2, 2), xlim=(0, 10), ylim=(0, 5))
    leader_vertices = [(-1, 0), (4, 7), (10, 15), outer_vertex_and_result[0]]
    expected_result = [(-1, 0), (4, 7), (10, 15), outer_vertex_and_result[1]]

    modified_vertices = tsa(leader_vertices)
    assert np.allclose(modified_vertices, expected_result)
