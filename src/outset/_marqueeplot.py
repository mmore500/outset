import itertools as it
import numbers
import typing

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes as mpl_Axes

from ._auxlib.calc_aspect_ import calc_aspect
from ._auxlib.calc_outer_pad_ import calc_outer_pad
from ._auxlib.is_axes_unset_ import is_axes_unset
from ._auxlib.robust_groupby_ import robust_groupby
from ._auxlib.set_aspect_ import set_aspect
from ._draw_marquee import draw_marquee
from .mark._MarkNumericalBadges import MarkNumericalBadges


def marqueeplot(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    hue: typing.Optional[str] = None,
    hue_order: typing.Optional[typing.Sequence[str]] = None,
    outset: typing.Optional[str] = None,
    outset_order: typing.Optional[typing.Sequence[str]] = None,
    ax: typing.Optional[mpl_Axes] = None,
    color: typing.Optional[str] = None,
    frame_inner_pad: typing.Union[float, typing.Tuple[float, float]] = 0.1,
    frame_outer_pad: typing.Union[float, typing.Tuple[float, float]] = 0.1,
    frame_outer_pad_unit: typing.Literal["axes", "figure", "inches"] = "axes",
    leader_tweak: typing.Union[
        typing.Callable, typing.Type
    ] = lambda x, *args, **kwargs: x,
    mark_glyph: typing.Union[
        typing.Callable, typing.Type, None
    ] = MarkNumericalBadges,
    palette: typing.Optional[typing.Sequence] = None,
    preserve_aspect: typing.Optional[bool] = False,
    tight_axlim: bool = False,
    **kwargs,
) -> mpl_Axes:
    """Plot marquee annotations to contain subsets of data from a pandas
    DataFrame.

    Provides a seaborn-like axis-level interface for `draw_marquee`. Details on
    marquee annotation structure and configuration can be found in that
    function's docstring.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the data to be marquee-annotated.
    x : str
        Column name in `data` for x-coordinate values of data positions.
    y : str
        Column name in `data` for y-coordinate values of data positions.
    hue : str, optional
        Column name in `data` for grouping data by color.

        If provided, colors are chosen according to palette.
    hue_order : Sequence[str], optional
        Order for plotting the categorical levels of `hue`.
    outset : str, optional
        Column name in `data` for producing different-colored annotated subsets.
    outset_order : Sequence[str], optional
        Order for plotting the categorical levels of `outset`.
    ax : mpl_axes.Axes, optional
        Matplotlib Axes object to draw the plot on.
    color : str, optional
        Color for all elements in the plot, overriding the `palette`.
    frame_inner_pad : Union[float, Tuple[float, float]], default 0.1
        Padding from data range to rectangular boundary.
    frame_outer_pad : Union[float, Tuple[float, float]], default 0.1
        Padding from frame boundary to axis viewport.
    frame_outer_pad_unit : Literal["axes", "figure", "inches"], default "axes"
        How should outer padding be specified?

        If 'axes' or 'figure', padding is specified as a fraction of the axes
        or figure size, respectively. If 'inches', padding is specified in
        inches.
    leader_tweak : Callable, default identity
        Callable or functor type to modify the callout leader vertices before
        drawing.
    mark_glyph : Union[Callable, Type, None], optional
        Callable or functor type to draw a glyph at the end of the callout.
    palette : Sequence, optional
        Color palette for plotting elements.
    preserve_aspect: bool, default False
        If True, finalizing by applying initial axes aspect. If None, restore initial axes aspect unless axes are unset.
    tight_axlim : bool, default False
        Whether to shrink axes limits to fit data range.
    **kwargs : dict
        Keyword arguments to adjust marquee sizing and styling.

        See `outset.draw_marquee` for available options.

    Returns
    -------
    matplotlib.axes.Axes
        The Matplotlib axes containing the plot with annotated regions.

    See Also
    --------
    outset.OutsetGrid
        Figure-level interface for creating plots with marquee annotations.
    outset.draw_marquee
        Low-level function for drawing marquee annotations.
    """
    if ax is None:
        ax = plt.gca()

    initial_axlim = ax.get_xlim(), ax.get_ylim()
    if preserve_aspect or (preserve_aspect is None and not is_axes_unset(ax)):
        initial_aspect = calc_aspect(ax)
    else:
        initial_aspect = None

    if palette is None:
        palette = sns.color_palette()

    if hue is not None and color is not None:
        raise ValueError(f"cannot specify both hue={hue} and color={color}")

    if isinstance(mark_glyph, type):
        mark_glyph = mark_glyph()

    if isinstance(leader_tweak, type):
        leader_tweak = leader_tweak()

    data = data.copy()

    # assemble data groups
    if hue is None:
        hue = "_dummy_hue"
        assert hue not in data.columns
        data[hue] = 0
        palette = [color]

    if hue_order is None:
        hue_order = sorted(data[hue].unique())

    color_lookup = dict(
        zip(
            hue_order,
            it.cycle(palette) if color is None else it.repeat(color),
        )
    )

    if outset is None:
        outset = "_dummy_outset"
        assert outset not in data.columns
        data[outset] = 0

    if outset_order is None:
        outset_order = sorted(data[outset].unique())

    data = data[
        data[hue].isin(hue_order) & data[outset].isin(outset_order)
    ].copy()

    assert "_dummy_hue_key" not in data.columns
    assert "_dummy_outset_key" not in data.columns
    data["_dummy_hue_key"] = data[hue].map([*hue_order].index)
    data["_dummy_outset_key"] = data[outset].map([*outset_order].index)
    data.sort_values(["_dummy_outset_key", "_dummy_hue_key"], inplace=True)

    # need to solve for and apply outer padding prior to plotting to ensure
    # consistency...
    _prepad_axlim(
        data=data,
        x=x,
        y=y,
        hue=hue,
        outset=outset,
        ax=ax,
        frame_inner_pad=frame_inner_pad,
        frame_outer_pad=frame_outer_pad,
        frame_outer_pad_unit=frame_outer_pad_unit,
        tight_axlim=tight_axlim,
    )

    for (_outset_value, hue_value), subset in data.groupby(
        [outset, hue],
        sort=False,
    ):
        assert len(subset)
        xlim = [subset[x].min(), subset[x].max()]
        ylim = [subset[y].min(), subset[y].max()]
        selected_color = color_lookup[hue_value]
        draw_marquee(
            frame_xlim=xlim,
            frame_ylim=ylim,
            ax=ax,
            color=selected_color,
            frame_inner_pad=frame_inner_pad,
            frame_outer_pad=(0, 0),  # already padded by prepad_axlim...
            leader_tweak=leader_tweak,
            mark_glyph=mark_glyph,
            **kwargs,
        )

    if initial_aspect is not None and not np.allclose(
        np.array(initial_axlim),
        np.array(
            (
                ax.get_xlim(),
                ax.get_ylim(),
            )
        ),
    ):
        set_aspect(ax, initial_aspect)

    return ax


def _prepad_axlim(
    data: pd.DataFrame,
    x: str,
    y: str,
    hue: typing.Optional[str],
    outset: typing.Optional[str],
    frame_inner_pad: typing.Union[float, typing.Tuple[float, float]],
    frame_outer_pad: typing.Union[float, typing.Tuple[float, float]],
    frame_outer_pad_unit: typing.Literal["axes", "figure", "data"],
    tight_axlim: bool,
    ax: typing.Optional[mpl_Axes] = None,
) -> None:
    """Calculate padded frame bounds and, if necessary, grow axes limits to
    include them."""
    if ax is None:
        ax = plt.gca()

    # precalculate frames with inner padding
    framex_values, framey_values = [], []
    for _, subset in robust_groupby(data, by=[outset, hue], sort=False):
        assert len(subset)

        is_number = isinstance(frame_inner_pad, numbers.Number)
        if is_number:
            # convert to absolute units to prevent weird effects from
            # successive calls to draw_marquee
            frame_inner_pad_x, frame_inner_pad_y = (
                frame_inner_pad * (np.ptp(subset[x]) or np.ptp(ax.get_xlim())),
                frame_inner_pad * (np.ptp(subset[y]) or np.ptp(ax.get_ylim())),
            )
        else:
            frame_inner_pad_x, frame_inner_pad_y = frame_inner_pad

        framex_values.extend(
            [
                subset[x].min() - frame_inner_pad_x,
                subset[x].max() + frame_inner_pad_x,
            ],
        )
        framey_values.extend(
            [
                subset[y].min() - frame_inner_pad_y,
                subset[y].max() + frame_inner_pad_y,
            ],
        )

    if is_axes_unset(ax) or tight_axlim:
        if framex_values and np.ptp(framex_values):
            ax.set_xlim(min(framex_values), max(framex_values))
        if framey_values and np.ptp(framey_values):
            ax.set_ylim(min(framey_values), max(framey_values))
    else:
        (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
        ax.set_xlim(min(*framex_values, x0), max(*framex_values, x1))
        ax.set_ylim(min(*framey_values, y0), max(*framey_values, y1))

    pad_x, pad_y = calc_outer_pad(ax, frame_outer_pad, frame_outer_pad_unit)
    if len(data):
        lowerx, upperx = (
            np.min(framex_values) - pad_x,
            np.max(framex_values) + pad_x,
        )
        lowery, uppery = (
            np.min(framey_values) - pad_y,
            np.max(framey_values) + pad_y,
        )
    else:
        lowerx, upperx = ax.get_xlim()
        lowery, uppery = ax.get_ylim()

    if tight_axlim or is_axes_unset(ax):
        pass
    else:
        lowerx = min(lowerx, ax.get_xlim()[0])
        lowery = min(lowery, ax.get_ylim()[0])
        upperx = max(upperx, ax.get_xlim()[1])
        uppery = max(uppery, ax.get_ylim()[1])

    # apply axis limit to incorporate outer padding
    ax.set_xlim(lowerx, upperx)
    ax.set_ylim(lowery, uppery)
