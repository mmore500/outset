import itertools as it
import math
import typing

import numpy as np


def layout_corner_insets(
    num_insets: int,
    corner: typing.Literal["NE", "NW", "SE", "SW"] = "NE",
    *,
    inset_grid_size: typing.Union[typing.Tuple[float, float], float] = 0.50,
    inset_margin_size: typing.Union[typing.Tuple[float, float], float] = 0.1,
    inset_pad_ratio: typing.Union[typing.Tuple[float, float], float] = 0.1,
    transpose: bool = False,
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
    inset_margin_size : Union[Tuple[float, float], float], default 0.5
        How far should grid be spaced from source plot boundaries, relative to
        the source plot size?
    inset_grid_size : Union[Tuple[float, float], float], default 0.5
        The size of the grid of inset plots relative to the source plot.
    inset_pad_ratio : Union[Tuple[float, float], float], default 0.1
        Pad size between inset plots as a fraction of inset plot size.
    transpose : bool, default False
        Should inset grid layout be ordered top-to-bottom, left-to-right?

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
    if not isinstance(inset_grid_size, typing.Iterable):
        inset_grid_size = (inset_grid_size, inset_grid_size)

    if not np.allclose(np.clip(inset_grid_size, 0.0, 1.0), inset_grid_size):
        raise ValueError("inset_grid_size values must be within unit scale")

    grid_size_x = inset_grid_size[0] / dimension
    grid_size_y = inset_grid_size[1] / dimension

    if not isinstance(inset_pad_ratio, typing.Iterable):
        inset_pad_ratio = (inset_pad_ratio, inset_pad_ratio)

    if not np.allclose(np.clip(inset_pad_ratio, 0.0, 1.0), inset_pad_ratio):
        raise ValueError("inset_pad_ratio values must be within unit scale")

    ax_size_x = grid_size_x * (1 - inset_pad_ratio[0])
    assert ax_size_x < grid_size_x

    ax_size_y = grid_size_y * (1 - inset_pad_ratio[1])
    assert ax_size_y < grid_size_y

    if not isinstance(inset_margin_size, typing.Iterable):
        inset_margin_size = (inset_margin_size, inset_margin_size)

    if not np.allclose(np.clip(inset_margin_size, 0.0, 1.0), inset_margin_size):
        raise ValueError("inset_margin_size values must be within unit scale")
    margin_x, margin_y = inset_margin_size

    if margin_x + grid_size_x > 1:
        raise ValueError(
            f"x grid size {grid_size_x} with margin {margin_x} "
            "exceeds available space"
        )
    if margin_y + grid_size_y > 1:
        raise ValueError(
            f"y grid size {grid_size_y} with margin {margin_y} "
            "exceeds available space"
        )

    # generate frame coordinates from the corner out, along diagonals
    # https://mmore500.com/2023/12/16/zigzag-traversal.html
    frame_coordinates = []
    for row, col in sorted(
        sorted(it.product(range(dimension), repeat=2), key=sum)[:num_insets],
    ):
        if transpose:
            row, col = col, row
        # Calculate the bottom-left corner of each frame
        x = 1.0 - margin_x - ax_size_x - col * grid_size_x
        y = 1.0 - margin_y - ax_size_y - row * grid_size_y
        assert 1 - inset_grid_size[0] - margin_x <= x + 1e-6
        assert x <= 1.0 - margin_x + 1e-6
        assert 1 - inset_grid_size[1] - margin_y <= y + 1e-6
        assert y <= 1.0 - margin_y + 1e-6

        if corner == "NW" or corner == "SW":
            x = grid_size_x * col + margin_x
            assert margin_x <= x + 1e-6
            assert x <= inset_grid_size[0] - ax_size_x + margin_x + 1e-6
        if corner == "SE" or corner == "SW":
            y = grid_size_y * row + margin_y
            assert margin_y <= y + 1e-6
            assert y <= inset_grid_size[1] - ax_size_y + margin_y + 1e-6

        # Add the frame to the list
        frame_coordinates.append((x, y, ax_size_x, ax_size_y))

    # take the first `num_insets` frames from corner out and then sort them
    # so that frames are ordered left-to-right, top-to-bottom
    return sorted(frame_coordinates[:num_insets], key=lambda c: (-c[1], c[0]))
