import itertools as it
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
    color: str = "black",
    clip_on: bool = False,
    leader_edge_kwargs: typing.Dict = frozendict.frozendict(),
    leader_face_kwargs: typing.Dict = frozendict.frozendict(),
    leader_stretch: float = 0.1,
    leader_stretch_unit: typing.Literal[
        "axes",
        "figure",
        "inches",
        "inchesfrom",
    ] = "axes",
    leader_tweak: typing.Callable = lambda x, *args, **kwargs: x,
    mark_glyph: typing.Optional[typing.Callable] = None,
    mark_glyph_kwargs: typing.Dict = frozendict.frozendict(),
    mark_retract: float = 0.1,
    zorder: float = 0,
    **kwargs,
) -> mpl_axes.Axes:
    """Annotate a rectangular region with a flyaway "zoom" indication upwards
    and to the right.

    Consists of (1) a callout leader and (2) a marked glyph. The leader is a
    gradient fill clipped to angle to a point up and to to the right of the
    framed region. The marked glyph (e.g., a numeral, an asterisk, etc.) is
    drawn at the vertex point of the leader.

    Parameters
    ----------
    frame_xlim : Tuple[float, float]
        The x-limits (xmin, xmax) of the rectangular region to be annotated.
    frame_ylim : Tuple[float, float]
        The y-limits (ymin, ymax) of the rectangular region to be annotated.
    ax : matplotlib.axes.Axes, optional
        The axes object on which to draw the callout. Defaults to `plt.gca()`.
    color : str, default "black"
        Color for the callout leader and glyph.
    clip_on : bool, default False
        Determines if drawing elements should be clipped to the axes bounding box.
    leader_edge_kwargs : Dict, default {}
        Keyword arguments for customizing the leader's edge.
    leader_face_kwargs : Dict, default {}
        Keyword arguments for customizing the leader's face.
    leader_stretch : float, default 0.1
        Size of callout leader in `leader_stretch_unit`.
    leader_stretch_unit : Literal['axes', 'figure', 'inches', 'inchesfrom'] default 'axes'
        How should leader stretch be specified?

        If 'axes' or 'figure', stretch is specified as a fraction of the axes
        or figure size, respectively. If 'inches', stretch is specified in
        inches. If 'inchesfrom', stretch is minimum necessary to place the
        marker `leader_stretch` inches from the lower left corner of the frame.
    mark_glyph : Optional[Callable], optional
        A callable to draw a glyph at the outer vertex of the callout leader.
        If None, no glyph is drawn.
    mark_retract : float, default 0.1
        Fraction to pull back glyph from the outer vertex of the callout.
    tweak : typing.Callable, default identity
        Callable to modify the callout leader vertices before drawing.
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
        ax,
        stretch=leader_stretch,
        stretch_unit=leader_stretch_unit,
    )
    leader_vertices = leader_tweak(leader_vertices, ax)

    # ... outline
    underlay_patch = mpl_patches.Polygon(  # underlay
        leader_vertices,  # w/ upper right corner
        **{
            "closed": True,
            "clip_on": clip_on,
            "linewidth": 2,
            "zorder": zorder,
            **kwargs,
            **leader_edge_kwargs,
            "edgecolor": "white",
            "facecolor": "none",
            "linestyle": "-",
        },
    )
    ax.add_patch(underlay_patch)
    leader_patch = mpl_patches.Polygon(
        leader_vertices,  # w/ upper right corner
        **{
            "closed": True,
            "clip_on": clip_on,
            "linewidth": 2,
            "zorder": zorder,
            **kwargs,
            "edgecolor": color,
            "facecolor": "none",
            "linestyle": ":",
            **leader_edge_kwargs,
        },
    )
    ax.add_patch(leader_patch)

    # ... gradient fill, clipped insideleader_polygon
    img = ax.imshow(
        make_radial_gradient(),
        **{
            "alpha": 0.5,
            "aspect": "auto",
            "cmap": mpl_colors.LinearSegmentedColormap.from_list(
                "gradient",
                ["white", color],
            ),
            "extent": get_vertices_extent(leader_vertices),
            "interpolation": "nearest",
            "zorder": zorder,
            **{
                k: v
                for k, v in it.chain(kwargs.items(), leader_face_kwargs.items())
                if k not in ("linestyle",)
            },
        },
    )
    if not clip_on:
        img.set_clip_box(ax.bbox.shrunk(10, 10))  # grow axis clipping box
    img.set_clip_path(leader_patch)

    # Draw callout glyph
    ###########################################################################
    frame_upper_right = np.array(leader_vertices[1])
    leader_outer_vertex = np.array(leader_vertices[-1])
    assert len(leader_outer_vertex) == 2, leader_outer_vertex

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

    return ax
