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
from ._auxlib.is_axes_unset_ import is_axes_unset
from .mark._MarkMagnifyingGlass import mark_magnifying_glass


def draw_marquee(
    frame_xlim: typing.Tuple[float, float],
    frame_ylim: typing.Tuple[float, float],
    ax: typing.Optional[mpl_axes.Axes] = None,
    *,
    color: typing.Optional[str] = "blue",
    clip_on: bool = False,
    despine: bool = True,
    frame_edge_kws: typing.Dict = frozendict.frozendict(),
    frame_face_kws: typing.Dict = frozendict.frozendict(),
    frame_inner_pad: typing.Union[float, typing.Tuple[float, float]] = 0.0,
    frame_outer_pad: typing.Union[float, typing.Tuple[float, float]] = 0.1,
    label: typing.Optional[str] = None,
    leader_edge_kws: typing.Dict = frozendict.frozendict(),
    leader_face_kws: typing.Dict = frozendict.frozendict(),
    leader_stretch: float = 0.2,
    leader_stretch_unit: typing.Literal[
        "axes",
        "figure",
        "inches",
        "inchesfrom",
    ] = "inches",
    leader_tweak: typing.Callable = lambda x, *args, **kwargs: x,
    mark_glyph: typing.Optional[typing.Callable] = mark_magnifying_glass,
    mark_glyph_kws: typing.Dict = frozendict.frozendict(),
    mark_retract: float = 0.1,
    zorder: float = 0,
) -> mpl_axes.Axes:
    """Mark a rectangular region on a matplotlib axes object, framing it with a
    zoom-effect callout.

    Consists of (1) a rectangular frame (2) a callout leader, and (3) a marked
    glyph. The rectangular frame consists of an outer of border and an
    underlaid solid color fill. The leader is a gradient fill clipped to angle
    to a point up and to to the right of the framed region. The marked glyph
    (e.g., a numeral, an asterisk, etc.) is drawn at the vertex point of the
    leader.

    The callout is capped by a customizable glyph, default as a magnifying
    glass.

    Parameters
    ----------
    frame_xlim : Tuple[float, float]
        X-limits (xmin, xmax) of the area to be marked as outset.
    frame_ylim : Tuple[float, float]
        Y-limits (ymin, ymax) of the area to be marked as outset.
    ax : matplotlib.axes.Axes, optional
        Axes object to draw the outset on. Defaults to `plt.gca()`.
    color : str, optional
        Color for the frame's edge and zoom indication lines.
    clip_on : bool, default False
        If True, drawing elements are clipped to the axes bounding box.
    despine : bool, default True
        If True, removes top and right spines from the plot.
    frame_edge_kws : Dict, default {}
        Customization arguments for the frame's edge.

        Standard matplotlib styling is supported (`linewidth`, `linestyle`,
        etc.).
    frame_face_kws : Dict, default {}
        Customization arguments for the frame's face.

        Standard matplotlib styling is supported (`facecolor`, `alpha`, etc.).
    frame_inner_pad : Union[float, Tuple[float, float]], default 0.0
        Padding from data extent to frame boundary, calculated relative to data
        extent (float) or in absolute units (tuple).
    frame_outer_pad : Union[float, Tuple[float, float]], default 0.1
        Padding from frame boundary to axis viewport, calculated relative to data extent (float) or in absolute units (tuple).
    label : str, optional
        Label used for legend creation.
    leader_edge_kws : Dict, default {}
        Customization arguments for the leader's edge.

        Standard matplotlib styling is supported (`linewidth`, `linestyle`,
        etc.).
    leader_face_kws : Dict, default {}
        Customization arguments for the leader's face.

        Standard matplotlib styling is supported (`facecolor`, `alpha`, etc.).
    leader_stretch : float, default 0.1
        Size of callout leader in `leader_stretch_unit`.
    leader_stretch_unit : Literal['axes', 'figure', 'inches', 'inchesfrom'], default 'axes'
        How should callout leader placement be determined?

        If 'axes' or 'figure', stretch is specified as a fraction of the axes
        or figure size, respectively. If 'inches', stretch is specified in
        inches. If 'inchesfrom', stretch is minimum necessary to place the
        marker `leader_stretch` inches from the lower left corner of the frame.
    leader_tweak : typing.Callable, default identity
        Callable to modify the callout leader vertices before drawing.
    mark_glyph : Callable, optional
        A callable to draw a glyph at the outer vertex of the callout leader.

        If None, no glyph is drawn.
    mark_glyph_kws : Dict, default frozendict.frozendict()
        Arguments for the mark_glyph callable.

        Standard matplotlib styling is supported (`markersize`, `color`, etc.).
    mark_retract : float, default 0.1
        Fraction to pull back glyph from the outer vertex of the callout.
    zorder : float, default 0
        Z-order for layering plot elements.

    Returns
    -------
    matplotlib.axes.Axes
        Axes with the outset and annotations added.

    Notes
    -----
    Delegates to `_auxlib.draw_callout_.draw_callout` and
    `_auslib.draw_callout_.draw_frame` for drawing.

    See Also
    --------
    outset.marqueeplot
        Axes-level tidy data interface for creating marquee annotations.
    outset.OutsetGrid
        Figure-level interface for creating plots with marquee annotations.
    """
    if ax is None:
        ax = plt.gca()
    if color is None:
        color = sns.color_palette()[0]

    # pad frame coordinates out from data
    if isinstance(frame_inner_pad, tuple):
        pad_x, pad_y = frame_inner_pad
    elif isinstance(frame_inner_pad, numbers.Number):
        pad_x = (np.ptp(frame_xlim) or np.ptp(ax.get_xlim())) * frame_inner_pad
        pad_y = (np.ptp(frame_ylim) or np.ptp(ax.get_ylim())) * frame_inner_pad
    else:
        raise ValueError(
            f"frame_inner_pad must be float or tuple, not {frame_inner_pad}",
        )
    frame_xlim = np.array(frame_xlim) + np.array([-pad_x, pad_x])
    frame_ylim = np.array(frame_ylim) + np.array([-pad_y, pad_y])

    # pad axis viewport out from frame
    ax_xlim, ax_ylim = ax.get_xlim(), ax.get_ylim()
    if isinstance(frame_outer_pad, tuple):
        pad_x, pad_y = frame_outer_pad
    elif isinstance(frame_outer_pad, numbers.Number):
        pad_x = max(np.ptp(ax.get_xlim()), np.ptp(frame_xlim)) * frame_outer_pad
        pad_y = max(np.ptp(ax.get_ylim()), np.ptp(frame_ylim)) * frame_outer_pad
    else:
        raise ValueError(
            f"frame_outer_pad must be float or tuple, not {frame_outer_pad}",
        )
    if is_axes_unset(ax):  # ... axes are empty, so ignore current axis viewport
        if pad_x or np.ptp(frame_xlim):
            ax.set_xlim(frame_xlim[0] - pad_x, frame_xlim[1] + pad_x)
        if pad_y or np.ptp(frame_ylim):
            ax.set_ylim(frame_ylim[0] - pad_y, frame_ylim[1] + pad_y)
    else:  # if axes not empty or axlim already set, ensure no viewport shrink
        ax.set_xlim(
            min(frame_xlim[0] - pad_x, ax_xlim[0]),
            max(frame_xlim[1] + pad_x, ax_xlim[1]),
        )
        ax.set_ylim(
            min(frame_ylim[0] - pad_y, ax_ylim[0]),
            max(frame_ylim[1] + pad_y, ax_ylim[1]),
        )

    # tweak zorder to ensure multiple outset annotations layer properly
    ax_width, ax_height = np.ptp(ax.get_xlim()), np.ptp(ax.get_ylim())
    ax_diag = np.sqrt(ax_width**2 + ax_height**2)
    upper_right_drop_x = (ax.get_ylim()[1] - frame_xlim[1]) / np.ptp(
        ax.get_xlim(),
    )
    upper_right_drop_y = (ax.get_ylim()[1] - frame_ylim[1]) / np.ptp(
        ax.get_ylim(),
    )
    upper_right_drop = np.sqrt(
        upper_right_drop_x**2 + upper_right_drop_y**2
    )
    zorder += 0.01 * upper_right_drop / ax_diag

    # Frame outset region
    ###########################################################################
    draw_frame(
        frame_xlim,
        frame_ylim,
        ax=ax,
        clip_on=clip_on,
        frame_edge_kws=frame_edge_kws,
        frame_face_kws=frame_face_kws,
        edgecolor=color,
        facecolor=color,
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
        leader_edge_kws=leader_edge_kws,
        leader_face_kws=leader_face_kws,
        leader_stretch=leader_stretch,
        leader_stretch_unit=leader_stretch_unit,
        leader_tweak=leader_tweak,
        mark_glyph=mark_glyph,
        mark_glyph_kws=mark_glyph_kws,
        mark_retract=mark_retract,
        zorder=zorder,
    )

    # Finalize
    ###########################################################################
    ax.set_axisbelow(True)  # ensure annotations above if outside bounds
    if despine:
        ax.spines[["right", "top"]].set_visible(False)
    if label is not None:
        ax.legend(handles=[mpl_patches.Patch(color=color, label=label)])

    return ax
