import numbers
import typing

import frozendict
import numpy as np
from matplotlib import axes as mpl_axes
from matplotlib import patches as mpl_patches
from matplotlib import pyplot as plt
import seaborn as sns

from ._auxlib.draw_callout_ import draw_callout
from ._auxlib.draw_frame_ import draw_frame
from .mark_magnifying_glass_ import mark_magnifying_glass


def draw_outset(
    frame_xlim: typing.Tuple[float, float],
    frame_ylim: typing.Tuple[float, float],
    ax: typing.Optional[mpl_axes.Axes] = None,
    *,
    color: typing.Optional[str] = "blue",
    frame_facealpha: float = 0.1,
    frame_linewidth: float = 1,
    clip_on: bool = False,
    despine: bool = True,
    frame_inner_pad: typing.Union[float, typing.Tuple[float, float]] = 0.0,
    label: typing.Optional[str] = None,
    leader_linestyle: str = ":",
    leader_linewidth: int = 2,
    leader_stretch: float = 0.1,
    mark_glyph: typing.Optional[typing.Callable] = mark_magnifying_glass,
    mark_glyph_kwargs: typing.Dict = frozendict.frozendict(),
    mark_retract: float = 0.1,
    zorder: float = 0,
) -> typing.Tuple[mpl_axes.Axes, typing.Tuple[float, float, float, float]]:
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
    color : typing.Optional[str], default "blue"
        Color for the frame's edge and the lines of the zoom indication.

        If None, the first color of the seaborn color palette is used.
    clip_on : bool, default False
        Determines if drawing elements should be clipped to the axes bounding
        box.
    despine : bool, default True
        Remove the top and right spines from the plots.
    frame_facealpha : float, default 0.1
        Alpha value for the frame's fill color, controlling its transparency.
    frame_inner_pad : Union[float, Tuple[float, float]], default 0.0
        How far from data range should rectangular boundary fall?

        If specified as a float value, horizontal and vertical padding is
        determined relative to axis viewport. If specified as a tuple, the first
        value specifies absolute horizontal padding in axis units and the second
        specifies absolute vertical padding in axis units.
    frame_linewidth : float, default 1
        Line width of the frame's edge.
    label : Optional[str], optional
        Used for legend creation.
    leader_linestyle : str, default ":"
        Line style for the zoom indication (e.g., solid, dashed, dotted).
    leader_linewidth : int, default 2
        Line width for the zoom indication's edges.
    leader_stretch : float, default 0.1
        Stretch factor for the callout leader extending from the frame.

        Set `leader_stretch` 0 to collapse away the leader.
    mark_glyph : Optional[Callable], optional
        A callable to draw a glyph at the end of the callout.

        Defaults to a magnifying glass. Outset also provides implementations
        for arrow, asterisk, and letter/number glyphs.
    mark_glyph_kwargs : Dict, default frozendict.frozendict()
        Keyword arguments for the mark_glyph callable.
    mark_retract : float, default 0.1
        Retraction factor for the glyph placement from the outer vertex of the
        callout.
    zorder : float, default 0
        Z-order for layering plot elements; higher values are drawn on top.

    Returns
    -------
    Tuple[mpl_axes.Axes, Tuple[float, float, float, float]]
        The axes object with the outset and annotations added.
    """
    if ax is None:
        ax = plt.gca()
    if color is None:
        color = sns.color_palette()[0]

    # pad frame coordinates out from data
    if isinstance(frame_inner_pad, tuple):
        pad_x, pad_y = frame_inner_pad
    elif isinstance(frame_inner_pad, numbers.Number):
        pad_x = np.ptp(ax.get_xlim()) * frame_inner_pad
        pad_y = np.ptp(ax.get_ylim()) * frame_inner_pad
    else:
        raise ValueError(
            f"frame_inner_pad must be float or tuple, not {frame_inner_pad}",
        )
    frame_xlim = np.array(frame_xlim) + np.array([-pad_x, pad_x])
    frame_ylim = np.array(frame_ylim) + np.array([-pad_y, pad_y])

    # pad axis viewport out from frame
    ax_xlim, ax_ylim = ax.get_xlim(), ax.get_ylim()
    # RE , see
    # https://matplotlib.org/stable/users/faq.html#check-whether-a-figure-is-empty
    if (
        len(ax.get_children()) > 11  # 11 objs in empty ax
        or ax.get_xlim() != (0.0, 1.0)  # in case axlim are already set...
        or ax.get_ylim() != (0.0, 1.0)
    ):  # if axes not empty or axlim already set, ensure no viewport shrink
        ax.set_xlim(
            min(frame_xlim[0] - pad_x, ax_xlim[0]),
            max(frame_xlim[1] + pad_x, ax_xlim[1]),
        )
        ax.set_ylim(
            min(frame_ylim[0] - pad_y, ax_ylim[0]),
            max(frame_ylim[1] + pad_y, ax_ylim[1]),
        )
    else:  # ... axes are empty, so ignore current axis viewport
        if pad_x or np.ptp(frame_xlim):
            ax.set_xlim(frame_xlim[0] - pad_x, frame_xlim[1] + pad_x)
        if pad_y or np.ptp(frame_ylim):
            ax.set_ylim(frame_ylim[0] - pad_y, frame_ylim[1] + pad_y)

    # tweak zorder to ensure multiple outset annotations layer properly
    ax_width, ax_height = np.ptp(ax.get_xlim()), np.ptp(ax.get_ylim())
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
    if despine:
        ax.spines[["right", "top"]].set_visible(False)
    if label is not None:
        ax.legend(handles=[mpl_patches.Patch(color=color, label=label)])

    return ax, (*frame_xlim, *frame_ylim)  # unpacks into tuple ctor
