import math

from outset._auxlib.find_intersection_ import find_intersection


def test_intersection_typical():
    # Test a typical case where two lines intersect
    assert find_intersection((0, 0), (1, 1), (0, 1), (1, 0)) == (0.5, 0.5)


def test_intersection_parallel():
    # Test a case where two lines are parallel and don't intersect
    assert math.isnan(find_intersection((0, 0), (1, 1), (0, 1), (1, 2))[0])
    assert math.isnan(find_intersection((0, 0), (1, 1), (0, 1), (1, 2))[1])


def test_intersection_collinear():
    # Test a case where two lines are collinear
    assert math.isnan(find_intersection((0, 0), (1, 1), (2, 2), (3, 3))[0])
    assert math.isnan(find_intersection((0, 0), (1, 1), (2, 2), (3, 3))[1])


def test_intersection_points_underspecified():
    # Test a case where lines are underspecified (e.g., points are identical)
    assert math.isnan(find_intersection((0, 0), (0, 0), (1, 1), (1, 1))[0])
    assert math.isnan(find_intersection((0, 0), (0, 0), (1, 1), (1, 1))[1])
