import itertools as it
import typing

import numpy as np


def minimal_perimeter_permutation(
    points: typing.Iterable[typing.Tuple[float, float]],
) -> typing.List[typing.Tuple[float, float]]:
    """Find the permutation of a sequence of points that minimizes the perimeter
    Euclidean distance.

    Brute force solver for traveling salesman problem

    Parameters
    ----------
    points : List[Tuple[float, float]]
        A list of 2D points where each point is represented as a tuple of (x, y)
        coordinates.

    Returns
    -------
    List[Tuple[float, float]]
        The permutation of points that yields the minimal Euclidean distance.

    Examples
    --------
    >>> points = [(0, 0), (2, 2), (1, 1)]
    >>> minimal_distance_permutation(points)
    [(0, 0), (1, 1), (2, 2)]

    Notes
    -----
    The function uses itertools.permutations to generate all possible orderings
    of the input points, and then calculates the total Euclidean distance for
    each permutation. The permutation with the minimal distance is returned.
    """

    def calc_perimeter_distance(
        perm: typing.Iterable[typing.Tuple[float, float]],
    ) -> float:
        return sum(
            np.linalg.norm(np.array(perm[i - 1]) - np.array(perm[i]))
            for i in range(len(perm))
        )

    min_perm = min(it.permutations(points), key=calc_perimeter_distance)
    return [*min_perm]
