import typing


def get_vertices_extent(
    vertices: typing.Iterable[typing.Tuple[float, float]]
) -> typing.Tuple[float, float, float, float]:
    """Get the extent of a set of vertices.

    Parameters
    ----------
    vertices : iterable of (float, float)
        The vertices to find the extent of.

    Returns
    -------
    tuple of float
        The extent of the vertices in the form (xmin, xmax, ymin, ymax).

    """
    x, y = zip(*vertices)
    return (min(x), max(x), min(y), max(y))
