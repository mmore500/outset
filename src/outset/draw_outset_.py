import typing

import frozendict
import numpy as np
from matplotlib import axes as mpl_axes
from matplotlib import pyplot as plt

from ._auxlib.draw_callout_ import draw_callout
from ._auxlib.draw_frame_ import draw_frame
from .mark_magnifying_glass_ import mark_magnifying_glass


def draw_outset(
    frame_xlim: typing.Tuple[float, float],
    frame_ylim: typing.Tuple[float, float],
    ax: typing.Optional[mpl_axes.Axes] = None,
    *,
    color: str = "blue",
    frame_facealpha: float = 0.1,
    frame_linewidth: float = 1,
    clip_on: bool = False,
    hide_outer_spines: bool = True,
    mark_glyph: typing.Optional[typing.Callable] = mark_magnifying_glass,
    mark_glyph_kwargs: typing.Dict = frozendict.frozendict(),
    mark_retract: float = 0.1,
    frame_inner_pad: float = 0.0,
    leader_linestyle: str = ":",
    leader_linewidth: int = 2,
    leader_stretch: float = 0.1,
    zorder: float = 0,
) -> mpl_axes.Axes:
    """Mark a rectangular region as outset, framing it and adding a
    "zoom"-effect callout up and to the right.

    The callout is capped by a customizable glyph, default as a magnifying
    glass.

    Parameters
    ----------
    frame_xlim : Tuple[float, float]
        The x-limits (xmin, xmax) of the area to be marked outset.
    frame_ylim : Tuple[float, float]
        The y-limits (ymin, ymax) of the area to be marked outset.
    ax : matplotlib.axes.Axes, optional
        The axes object on which to draw the outset.

        Defaults to `plt.gca()`.
    color : str, default "blue"
        Color for the frame's edge and the lines of the zoom indication.
    frame_facealpha : float, default 0.1
        Alpha value for the frame's fill color, controlling its transparency.
    frame_linewidth : float, default 1
        Line width of the frame's edge.
    clip_on : bool, default False
        Determines if drawing elements should be clipped to the axes bounding
        box.
    hide_outer_spines : bool, default True
        If True, hides the top and right spines of the axes.
    mark_glyph : Optional[Callable], optional
        A callable to draw a glyph at the end of the callout.

        Defaults to a magnifying glass. Outset also provides implementations
        for arrow, asterisk, and letter/number glyphs.
    mark_glyph_kwargs : Dict, default frozendict.frozendict()
        Keyword arguments for the mark_glyph callable.
    mark_retract : float, default 0.1
        Retraction factor for the glyph placement from the outer vertex of the
        callout.
    frame_inner_pad : float, default 0.0
        Padding factor for the inner margin of the frame.
    leader_linestyle : str, default ":"
        Line style for the zoom indication (e.g., solid, dashed, dotted).
    leader_linewidth : int, default 2
        Line width for the zoom indication's edges.
    leader_stretch : float, default 0.1
        Stretch factor for the callout leader extending from the frame.

        Set `leader_stretch` 0 to collapse away the leader.
    zorder : float, default 0
        Z-order for layering plot elements; higher values are drawn on top.

    Returns
    -------
    mpl_axes.Axes
        The axes object with the outset and annotations added.
    """
    if ax is None:
        ax = plt.gca()

    pad_x = (ax.get_xlim()[1] - ax.get_xlim()[0]) * frame_inner_pad
    frame_xlim = np.array(frame_xlim) + np.array([-pad_x, pad_x])
    pad_y = (ax.get_ylim()[1] - ax.get_ylim()[0]) * frame_inner_pad
    frame_ylim = np.array(frame_ylim) + np.array([-pad_y, pad_y])

    # tweak zorder to ensure multiple outset annotations layer properly
    ax_width = ax.get_xlim()[1] - ax.get_xlim()[0]
    ax_height = ax.get_ylim()[1] - ax.get_ylim()[0]
    ax_diag = np.sqrt(ax_width**2 + ax_height**2)
    upper_right_drop_x = ax.get_ylim()[1] - frame_xlim[1]
    upper_right_drop_y = ax.get_ylim()[1] - frame_ylim[1]
    upper_right_drop = np.sqrt(
        upper_right_drop_x**2 + upper_right_drop_y**2
    )
    zorder += 0.25 * upper_right_drop / ax_diag

    # Frame outset region
    ###########################################################################
    draw_frame(
        frame_xlim,
        frame_ylim,
        ax=ax,
        clip_on=clip_on,
        edgecolor=color,
        facecolor=(color, frame_facealpha),
        linewidth=frame_linewidth,
        zorder=zorder,
    )

    # Draw callout
    ###########################################################################
    draw_callout(
        frame_xlim,
        frame_ylim,
        ax,
        color=color,
        clip_on=clip_on,
        linewidth=leader_linewidth,
        linestyle=leader_linestyle,
        mark_glyph=mark_glyph,
        mark_glyph_kwargs=mark_glyph_kwargs,
        mark_retract=mark_retract,
        leader_stretch=leader_stretch,
        zorder=zorder,
    )

    # Finalize
    ###########################################################################
    ax.set_axisbelow(True)  # ensure annotations above if outside bounds
    if hide_outer_spines:
        ax.spines[["right", "top"]].set_visible(False)
