from outset._auxlib.minimal_perimeter_permutation_ import (
    minimal_perimeter_permutation,
)


def test_basic_functionality():
    # Test the basic functionality with a simple example
    points = [(0, 0), (1, 1), (2, 2)]
    expected = [(0, 0), (1, 1), (2, 2)]
    assert minimal_perimeter_permutation(points) == expected


def test_single_point():
    # Test the function with a single point
    points = [(1, 1)]
    expected = [(1, 1)]
    assert minimal_perimeter_permutation(points) == expected


def test_empty_input():
    # Test the function with an empty list
    points = []
    expected = []
    assert minimal_perimeter_permutation(points) == expected


def test_non_trivial_case():
    # Test the function with a non-trivial case
    points = [(0, 0), (2, 2), (1, 1), (3, 3)]
    # Expected output should be in the order that minimizes the perimeter
    # The exact expected output might depend on the implementation
    result = minimal_perimeter_permutation(points)
    assert len(result) == len(points)  # Check if all points are included
    # Further checks can be added based on expected behavior


def test_negative_coordinates():
    # Test with negative coordinates
    points = [(-1, -1), (0, 0), (1, 1)]
    expected = [(-1, -1), (0, 0), (1, 1)]
    assert minimal_perimeter_permutation(points) == expected


def test_duplicate_points():
    # Test with duplicate points
    points = [(0, 0), (1, 1), (1, 1)]
    expected = [(0, 0), (1, 1), (1, 1)]
    assert minimal_perimeter_permutation(points) == expected
