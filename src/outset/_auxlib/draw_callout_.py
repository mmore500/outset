import typing

import frozendict
import numpy as np
from matplotlib import axes as mpl_axes
from matplotlib import colors as mpl_colors
from matplotlib import patches as mpl_patches
from matplotlib import pyplot as plt

from .compose_callout_leader_ import compose_callout_leader
from .get_vertices_extent_ import get_vertices_extent
from .make_radial_gradient_ import make_radial_gradient


def draw_callout(
    frame_xlim: typing.Tuple[float, float],
    frame_ylim: typing.Tuple[float, float],
    ax: typing.Optional[mpl_axes.Axes] = None,
    *,
    color: str = "blue",
    clip_on: bool = False,
    mark_glyph: typing.Optional[typing.Callable] = None,
    mark_glyph_kwargs: typing.Dict = frozendict.frozendict(),
    mark_retract: float = 0.1,
    leader_stretch: float = 0.1,
    zorder: float = 0,
    **kwargs,
) -> mpl_axes.Axes:
    """Annotate a rectangular region with a flyaway "zoom" indication upwards
    and to the right.

    Parameters
    ----------
    frame_xlim : Tuple[float, float]
        The x-limits (xmin, xmax) of the rectangular region to be annotated.
    frame_ylim : Tuple[float, float]
        The y-limits (ymin, ymax) of the rectangular region to be annotated.
    ax : matplotlib.axes.Axes, optional
        The axes object on which to draw the callout.

        Defaults to `plt.gca()`.
    color : str, default "blue"
        Color for the callout leader and glyph.
    clip_on : bool, default False
        Determines if drawing elements should be clipped to the axes bounding box.
    mark_glyph : Optional[Callable], optional
        A callable to draw a glyph at the outer vertex of the callout leader.

        if None, no glyph is drawn.
    mark_retract : float, default 0.1
        Fraction to pull back glyph from outer vertex of the callout.
    leader_stretch : float, default 0.1
        Scale of callout leader relative to axis viewport.
    zorder : float, default 0
        Influences layer order of plot, with higher values in front.
    **kwargs
        Additional keyword arguments for matplotlib Polygon used in the callout.

    Returns
    -------
    mpl_axes.Axes
        The modified matplotlib axes object with the drawing elements added.
    """
    if ax is None:
        ax = plt.gca()

    # Draw callout leader
    ###########################################################################
    leader_vertices = compose_callout_leader(
        frame_xlim,
        frame_ylim,
        ax.get_xlim(),
        ax.get_ylim(),
        stretch=leader_stretch,
    )

    # ... outline
    leader_patch = mpl_patches.Polygon(
        leader_vertices,  # w/ upper right corner
        closed=True,
        facecolor="none",
        edgecolor=color,
        zorder=zorder,
        clip_on=clip_on,
        **kwargs,
    )
    ax.add_patch(leader_patch)

    # ... gradient fill, clipped insideleader_polygon
    img = ax.imshow(
        make_radial_gradient(),
        aspect="auto",
        cmap=mpl_colors.LinearSegmentedColormap.from_list(
            "gradient",
            ["white", color],
        ),
        extent=get_vertices_extent(leader_vertices),
        interpolation="nearest",
        zorder=zorder,
    )
    if not clip_on:
        img.set_clip_box(ax.bbox.shrunk(10, 10))  # grow axis clipping box
    img.set_clip_path(leader_patch)

    # Draw callout glyph
    ###########################################################################
    frame_upper_right = np.array([frame_xlim[1], frame_ylim[1]])
    leader_outer_vertex = tuple(np.max(np.array(leader_vertices), axis=0))
    assert len(leader_outer_vertex) == 2
    assert all(np.array(leader_outer_vertex) >= np.array(frame_upper_right))

    mark_coordinates = np.average(
        np.array([leader_outer_vertex, frame_upper_right]),
        weights=np.array([1.0 - mark_retract, mark_retract]),
        axis=0,
    )
    if mark_glyph is not None:
        mark_glyph(
            *mark_coordinates,
            ax=ax,
            **{
                "color": color,
                "clip_on": clip_on,
                "zorder": zorder,
                **mark_glyph_kwargs,
            },
        )
