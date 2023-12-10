import math
import typing


def find_intersection(
    p1: typing.Tuple[float, float],
    p2: typing.Tuple[float, float],
    p3: typing.Tuple[float, float],
    p4: typing.Tuple[float, float],
) -> typing.Tuple[float, float]:
    """Finds the intersection of two lines (p1 to p2 and p3 to p4).

    Points are represented a tuple of (x, y).

    Returns
    -------
    Tuple[float, float]
        The intersection point, (x, y).

        If lines do not intersect or are underspecified, result is (nan, nan).
    """

    # Unpack points
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        return (math.nan, math.nan)

    # adapted from https://stackoverflow.com/a/51127674
    px = (
        (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    ) / denominator
    py = (
        (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    ) / denominator

    return (px, py)
