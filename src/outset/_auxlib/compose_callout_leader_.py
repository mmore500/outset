import typing

import numpy as np


def compose_callout_leader(
    frame_xlim: typing.Tuple[float, float],
    frame_ylim: typing.Tuple[float, float],
    ax_xlim: typing.Tuple[float, float],
    ax_ylim: typing.Tuple[float, float],
    stretch: float,
) -> typing.List[typing.Tuple[float, float]]:
    """Decide shape, size, and position of callout leader triangle.

    Outer leader vertex placement is calculated relative to the upper right
    frame vertex. The outer vertex is place

        Uses reflected right triangle similar to the proportions of the rectangle
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
    frame_xlim : typing.Tuple[float, float]
        The x-axis limits (min, max) of the rectangle.
    frame_ylim : typing.Tuple[float, float]
        The y-axis limits (min, max) of the rectangle.
    ax_xlim : typing.Tuple[float, float]
        The x-axis limits (min, max) of the axis.
    ax_ylim : typing.Tuple[float, float]
        The y-axis limits (min, max) of the axis.
    stretch : float
        The stretch factor for the zoom effect.

    Returns
    -------
    list
        A list of tuples representing the sequence of vertices of the trapezoid, arranged to minimize the perimeter.

    """
    if any(
        float.__gt__(*map(float, lim))
        for lim in [frame_xlim, frame_ylim, ax_xlim, ax_ylim]
    ):
        raise ValueError("Limits must be provided as (min, max).")

    if stretch < 0.0:
        raise ValueError("Leader stretch must be non-negative.")

    ax_width, ax_height = (
        ax_xlim[1] - ax_xlim[0],
        ax_ylim[1] - ax_ylim[0],
    )
    frame_width, frame_height = (
        frame_xlim[1] - frame_xlim[0],
        frame_ylim[1] - frame_ylim[0],
    )
    (
        (_frame_lower_left, frame_upper_right),
        (frame_upper_left, frame_lower_right),
    ) = zip(frame_xlim, frame_ylim), zip(frame_xlim, reversed(frame_ylim))

    theta = np.arctan(frame_height / frame_width)
    rel_height, rel_width = np.sin(theta) * stretch, np.cos(theta) * stretch
    height, width = rel_height * ax_height, rel_width * ax_width
    offsets = np.array([width, height])

    leader_outer_vertex = tuple(np.array(frame_upper_right) + offsets)

    leader_vertices = [
        frame_upper_left,
        frame_upper_right,
        frame_lower_right,
        leader_outer_vertex,
    ]

    return leader_vertices
