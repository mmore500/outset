import typing

from matplotlib import axes as mpl_axes
from matplotlib import patches as mpl_patches
from matplotlib import pyplot as plt
from matplotlib import colors as mpl_colors
import numpy as np

from ._auxlib.compose_zoom_trapezoid_ import compose_zoom_trapezoid
from ._auxlib.get_vertices_extent_ import get_vertices_extent
from ._auxlib.find_intersection_ import find_intersection
from ._auxlib.make_radial_gradient_ import make_radial_gradient
from ._auxlib.minimal_perimeter_permutation_ import (
    minimal_perimeter_permutation,
)


def draw_outset(
    xlim: typing.Tuple[float, float],
    ylim: typing.Tuple[float, float],
    ax: typing.Optional[mpl_axes.Axes] = None,
    color: str = "blue",
    box_facecolor: str = "white",
    box_linewidth: float = 0.5,
    clip_on: bool = False,
    hide_outer_spines: bool = True,
    markersize: float = 15,
    zoom_linestyle: str = ":",
    zoom_linewidth: int = 2,
    stretch: float = 0.14,
) -> mpl_axes.Axes:
    """Mark the boundary of a rectangular region and annotate with a flyout
    "zoom" indication upwards and to the right.

    Parameters
    ----------
    xlim : Tuple[float, float]
        The x-limits of the rectangular boundary in the form (xmin, xmax).
    ylim : Tuple[float, float]
        The y-limits of the rectangular boundary in the form (ymin, ymax).
    ax : matplotlib.axes.Axes, optional
        The axes object on which to draw. If None, the current active axes will
        be used.
    color : str, default "blue"
        The color of the box's edge and the zoom indication's lines.
    box_facecolor : str, default "white"
        The fill color of the rectangular boundary.
    box_linewidth : float, default 0.5
        The line width of the rectangular boundary's edge.
    clip_on : bool, default False
        If True, the drawing elements are clipped to the axes bounding box.
    hide_outer_spines : bool, default True
        If True, hides the right and top spines of the axes.
    markersize : float, default 15
        The size of the marker at the intersection of the zoom indication's
        edges.
    zoom_linestyle : str, default ":"
        The line style for the zoom indication (e.g., solid, dashed, dotted).
    zoom_linewidth : int, default 2
        The line width of the zoom indication's edges.
    stretch : float, default 0.14
        How far should zoom indication stretch upwards and to the right?

    Returns
    -------
    mpl_axes.Axes
        The modified matplotlib axes object with the drawing elements added.
    """
    if ax is None:
        ax = plt.gca()

    # Outline zoom regions with rectangle
    ###########################################################################
    rect = mpl_patches.Rectangle(
        (xlim[0], ylim[0]),  # lower left corner
        xlim[1] - xlim[0],  # width
        ylim[1] - ylim[0],  # height
        linewidth=box_linewidth,
        edgecolor=color,
        facecolor=box_facecolor,
        clip_on=clip_on,
    )
    ax.add_patch(rect)

    # Draw zoom trapezoid...
    ###########################################################################
    trapezoid_vertices = compose_zoom_trapezoid(
        xlim, ylim, ax.get_xlim(), ax.get_ylim(), stretch=stretch
    )
    trapezoid_vertices = minimal_perimeter_permutation(trapezoid_vertices)
    # ... outline
    trapezoid = mpl_patches.Polygon(
        trapezoid_vertices,
        closed=True,
        facecolor="none",
        edgecolor=color,
        linestyle=zoom_linestyle,
        linewidth=zoom_linewidth,
        zorder=-3,
        clip_on=clip_on,
    )
    ax.add_patch(trapezoid)

    # ... gradient fill, clipped insidetrapezoid
    img = ax.imshow(
        make_radial_gradient(),
        extent=get_vertices_extent(trapezoid_vertices),
        interpolation="nearest",
        aspect="auto",
        cmap=mpl_colors.LinearSegmentedColormap.from_list(
            "gradient",
            ["white", color],
        ),
    )
    if not clip_on:
        img.set_clip_box(ax.bbox.shrunk(10, 10))  # grow axis clipping box
    img.set_clip_path(trapezoid)

    # Add circle and asterisk at point where trapezoid edges meet...
    ###########################################################################
    rotated_vertices = _rotate_vertices(trapezoid_vertices)
    center = find_intersection(*rotated_vertices)

    plt.plot(  # ...white underlay for asterisk
        *center,
        marker="o",
        markeredgecolor="none",
        markerfacecolor="white",
        markersize=markersize * 1.66,
        clip_on=clip_on,
    )
    plt.plot(  # ...asterisk
        *center,
        marker=(6, 2, 0),  # six-pointed asterisk
        markeredgecolor=color,
        markerfacecolor="none",
        markersize=markersize,
        clip_on=clip_on,
    )

    # Finalize
    ###########################################################################
    ax.set_axisbelow(True)  # ensure annotations above if outside bounds
    if hide_outer_spines:
        ax.spines[["right", "top"]].set_visible(False)


def _rotate_vertices(trapezoid_vertices: np.ndarray) -> np.ndarray:
    # need to roll trapezoid_vertices so that the rectangle-corner vertices
    # are in first and last positions
    assert len(trapezoid_vertices) == 4

    xs = np.array(trapezoid_vertices)[:, 0]
    ys = np.array(trapezoid_vertices)[:, 1]
    rect_upper_left_idx, rect_lower_right_idx = np.argmin(xs), np.argmin(ys)

    gap = (rect_lower_right_idx - rect_upper_left_idx) % 4
    if gap == 1:
        rotated = np.roll(trapezoid_vertices, -rect_lower_right_idx, axis=0)
    elif gap == 3:
        rotated = np.roll(trapezoid_vertices, -rect_upper_left_idx, axis=0)
    else:
        assert False, (gap, trapezoid_vertices)

    assert np.argmin(np.array(rotated)[:, 0]) in (0, 3)
    assert np.argmin(np.array(rotated)[:, 1]) in (0, 3)

    return rotated
