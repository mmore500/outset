import pytest

from outset._auxlib.get_vertices_extent_ import get_vertices_extent


def test_get_vertices_extent():
    # Test with a simple rectangle
    vertices = [(0, 0), (2, 0), (2, 3), (0, 3)]
    expected_extent = (0, 2, 0, 3)
    assert get_vertices_extent(vertices) == expected_extent

    # Test with a single point
    vertices = [(1, 1)]
    expected_extent = (1, 1, 1, 1)
    assert get_vertices_extent(vertices) == expected_extent

    # Test with an empty list
    vertices = []
    with pytest.raises(ValueError):
        get_vertices_extent(vertices)
