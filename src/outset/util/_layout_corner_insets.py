import itertools as it
import math
import typing


def layout_corner_insets(
    num_insets: int,
    corner: typing.Literal["NE", "NW", "SE", "SW"] = "NE",
    *,
    inset_grid_size: float = 0.50,
    inset_pad_ratio: float = 0.1,
) -> typing.List[typing.Tuple[float, float, float, float]]:
    """Lay out positions for `n` inset plots in a specified corner.

    The frames are filled from the chosen corner outwards, filling successive diagonals perpendicular to the cornder. Inset subfigure positions are
    ordered so that inset number increases left-to-right, top-to-bottom.

    Parameters
    ----------
    num_insets : int
        The number of inset plots to be generated.
    corner : Literal["NE", "NW", "SE", "SW"], default "NE"
        The corner of the grid where the insets will be positioned.
    inset_grid_size : float, default 0.4
        The size of the grid of inset plots relative to the source plot.
    inset_pad_ratio : float, default 0.33
        Pad size between inset plots as a fraction of inset plot size.

    Returns
    -------
    List[Tuple[float, float, float, float]]
        A list of tuples, each representing `(x, y, width, height)` of an inset
        plot fractionally relative to source plot axes.

    See Also
    --------
    outset.util.inset_outsets
        Manipulates plot structure to apply corner inset layout calculated by
        `layout_corner_insets`, placing outset plots in specified positions over
        the source plot axes.
    """
    dimension = int(math.ceil(math.sqrt(num_insets)))
    grid_size = inset_grid_size / dimension
    ax_size = grid_size * (1 - inset_pad_ratio)
    assert ax_size < grid_size

    # generate frame coordinates from the corner out, along diagonals
    # https://mmore500.com/2023/12/16/zigzag-traversal.html
    frame_coordinates = []
    for row, col in sorted(
        sorted(it.product(range(dimension), repeat=2), key=sum)[:num_insets],
    ):
        # Calculate the top-left corner of each frame
        x = 1.0 - grid_size - col * grid_size
        y = 1.0 - grid_size - row * grid_size
        assert 1 - inset_grid_size <= x + 1e-6
        assert x <= 1.0 - grid_size + 1e-6
        assert 1 - inset_grid_size <= y + 1e-6
        assert y <= 1.0 - grid_size + 1e-6

        if corner == "NW" or corner == "SW":
            x = grid_size * col + (grid_size - ax_size)
            assert grid_size - ax_size <= x + 1e-6
            assert x <= inset_grid_size - ax_size + 1e-6
        if corner == "SE" or corner == "SW":
            y = grid_size * row + (grid_size - ax_size)
            assert grid_size - ax_size <= y + 1e-6
            assert y <= inset_grid_size - ax_size + 1e-6

        # Add the frame to the list
        frame_coordinates.append((x, y, ax_size, ax_size))

    # take the first `num_insets` frames from corner out and then sort them
    # so that frames are ordered left-to-right, top-to-bottom
    return sorted(frame_coordinates[:num_insets], key=lambda c: (-c[1], c[0]))
