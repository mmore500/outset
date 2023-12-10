import typing

import numpy as np

from .minimal_perimeter_permutation_ import minimal_perimeter_permutation


def compose_zoom_trapezoid(
    rect_xlim: typing.Tuple[float, float],
    rect_ylim: typing.Tuple[float, float],
    ax_xlim: typing.Tuple[float, float],
    ax_ylim: typing.Tuple[float, float],
    stretch: float = 0.14,
):
    """Decide shape, size, and position of trapezoidal zoom effect decoration.

    Uses reflected right triangles similar to the proportions of the rectangle
    to pick the upper points for the trapezoid, relative to the upper right
    corner of the rectangle. The trapezoid is then constructed to include
    the upper left corner of the rectangle and the lower right corner of the rectangle.

    The distance of the upper vertices of the zoom annotation from the
    rectangle are controlled by scaling the similar triangles. Scaling is
    adjusted by relative size of the rectangle within the axis viewport,
    with smaller rectangles given proportionally larger stretch factors to
    prevent overlap of decorations applied to the upper vertices with the
    rectangle.

    This can be tweaked through the "stretch" parameter, with higher stretch
    factors resulting in upper vertices further from the rectangle.

    Note that a portion of the trapezoid falls behind the rectangle.

    Limits should be provided in ascending order.

    Parameters
    ----------
    rect_xlim : typing.Tuple[float, float]
        The x-axis limits (min, max) of the rectangle.
    rect_ylim : typing.Tuple[float, float]
        The y-axis limits (min, max) of the rectangle.
    ax_xlim : typing.Tuple[float, float]
        The x-axis limits (min, max) of the axis.
    ax_ylim : typing.Tuple[float, float]
        The y-axis limits (min, max) of the axis.
    stretch : float, optional
        The stretch factor for the zoom effect, by default 0.14.

    Returns
    -------
    list
        A list of tuples representing the sequence of vertices of the trapezoid, arranged to minimize the perimeter.

    """
    if any(
        float.__gt__(*map(float, lim))
        for lim in [rect_xlim, rect_ylim, ax_xlim, ax_ylim]
    ):
        raise ValueError("Limits must be provided as (min, max).")

    ax_width, ax_height = (
        ax_xlim[1] - ax_xlim[0],
        ax_ylim[1] - ax_ylim[0],
    )
    rect_width, rect_height = (
        rect_xlim[1] - rect_xlim[0],
        rect_ylim[1] - rect_ylim[0],
    )
    (
        (_rect_lower_left, rect_upper_right),
        (rect_upper_left, rect_lower_right),
    ) = zip(rect_xlim, rect_ylim), zip(rect_xlim, reversed(rect_ylim))

    rel_width = rect_width / ax_width
    rel_height = rect_height / ax_height
    mx = stretch / np.sqrt(rel_width**2 + rel_height**2)
    offsets = np.array([mx * rect_height, mx * rect_width])

    trapezoid_top_left = np.array(rect_upper_right) + offsets
    trapezoid_top_right = np.array(rect_upper_right) + np.flip(offsets)

    trapezoid_points = [
        rect_upper_left,
        rect_lower_right,
        trapezoid_top_right,
        trapezoid_top_left,
    ]
    # ensure no "bow-tie" self intersection
    trapezoid_sequence = minimal_perimeter_permutation(trapezoid_points)

    return trapezoid_sequence
