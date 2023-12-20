import typing

from matplotlib import axes as mpl_axes
import numpy as np


def compose_callout_leader(
    frame_xlim: typing.Tuple[float, float],
    frame_ylim: typing.Tuple[float, float],
    ax: mpl_axes.Axes,
    stretch: float,
    stretch_unit: typing.Literal["axes", "figure", "inches", "inchesfrom"],
) -> typing.List[typing.Tuple[float, float]]:
    """Decide shape, size, and position of callout leader triangle.

    Outer leader vertex placement is calculated relative to the upper right
    frame vertex.

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
    ax : mpl_axes.Axes
        The axes object where the callout leader will be drawn.
    stretch : float
        The stretch factor for the zoom effect.
    stretch_unit : {"axes", "figure", "inches", "inchesfrom"}, default "axes"
        How should stretch be specified?

    Returns
    -------
    list
        A list of tuples representing the sequence of vertices of the trapezoid, arranged to minimize the perimeter.
    """
    if any(float.__gt__(*map(float, lim)) for lim in [frame_xlim, frame_ylim]):
        raise ValueError("Limits must be provided as (min, max).")

    if stretch < 0.0:
        raise ValueError("Leader stretch must be non-negative.")

    ax_width, ax_height = np.ptp(ax.get_xlim()), np.ptp(ax.get_ylim())
    frame_width, frame_height = np.ptp(frame_xlim), np.ptp(frame_ylim)
    (
        (frame_lower_left, frame_upper_right),
        (frame_upper_left, frame_lower_right),
    ) = zip(frame_xlim, frame_ylim), zip(frame_xlim, reversed(frame_ylim))

    if frame_width:
        theta = np.arctan(
            frame_height
            / frame_width
            * np.ptp(ax.get_xlim())
            / np.ptp(ax.get_ylim())
        )
    elif frame_height:
        theta = np.pi / 2
    else:
        theta = 0

    stretch_y, stretch_x = np.sin(theta) * stretch, np.cos(theta) * stretch
    if stretch_unit == "axes":
        height, width = stretch_y * ax_height, stretch_x * ax_width
    elif stretch_unit == "figure":
        fig_width, fig_height = ax.figure.get_size_inches()
        pixel_width, pixel_height = ax.transData.transform(
            [fig_width * stretch_x, fig_height * stretch_y],
        )
        # Convert display coordinates back to data coordinates
        height, width = ax.transData.inverted().transform(
            [(pixel_width, pixel_height)],
        )[0]
    elif stretch_unit == "inches":
        axwidth_inches = ax.get_position().width * ax.figure.get_figwidth()
        axheight_inches = ax.get_position().height * ax.figure.get_figheight()
        stretch_x_axfrac = stretch_x / axwidth_inches
        stretch_y_axfrac = stretch_y / axheight_inches
        height, width = (
            stretch_y_axfrac * ax_height,
            stretch_x_axfrac * ax_width,
        )
    elif stretch_unit == "inchesfrom":
        axwidth_inches = ax.get_position().width * ax.figure.get_figwidth()
        axheight_inches = ax.get_position().height * ax.figure.get_figheight()
        stretch_x_axfrac = stretch_x / axwidth_inches
        stretch_y_axfrac = stretch_y / axheight_inches
        width, height = (
            stretch_x_axfrac * ax_width,
            stretch_y_axfrac * ax_height,
        )
        minimum_lower_left = np.array(frame_lower_left) + np.array(
            [width, height],
        )
        width, height = np.maximum(
            minimum_lower_left - np.array(frame_upper_right),
            np.zeros(2),
        )
    else:
        raise ValueError(
            f"stretch_unit must be 'axes', 'figure', 'inches', or 'inchesfrom' "
            "not {stretch_unit}",
        )
    offsets = np.array([width, height])

    leader_outer_vertex = tuple(np.array(frame_upper_right) + offsets)

    leader_vertices = [
        frame_upper_left,
        frame_upper_right,
        frame_lower_right,
        leader_outer_vertex,
    ]

    return leader_vertices
