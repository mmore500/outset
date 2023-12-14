import itertools as it
import numbers
import typing

import matplotlib.pyplot as plt
import numpy as np
import opytional as opyt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes as mpl_Axes

from ._auxlib.is_axes_unset_ import is_axes_unset
from .draw_marquee_ import draw_marquee
from .MarkNumericalBadges_ import MarkNumericalBadges


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
    mark_glyph: typing.Union[
        typing.Callable, typing.Type, None
    ] = MarkNumericalBadges,
    palette: typing.Optional[typing.Sequence] = None,
    tight_axlim: bool = False,
    **kwargs,
) -> typing.Tuple[mpl_Axes, typing.List[typing.Tuple[float, float]]]:
    """Creates outset annotation(s) containing specified x, y points from a
    pandas DataFrame, potentially within-color coded groups determined by a
    categorical column `outset`.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the data to be plotted.
    x : str
        Name of the column in `data` to be used for x-axis values.
    y : str
        Name of the column in `data` to be used for y-axis values.
    outset : str, optional
        Name of the categorical column in `data` to produce different-colored
        annotated subsets.

        If provided, colors are chosen according to palette.
    outset_order : Sequence, optional
        Order to plot the categorical levels in.

        If None, outsets are assigned based on outset column sorted order.
    ax : matplotlib.axes.Axes, optional
        Matplotlib Axes object to draw the plot on. If None, the current axes
        are used.
    color :
    frame_inner_pad : Union[float, Tuple[float, float]], default 0.1
        How far from data range should rectangular boundary fall?

        If specified as a float value, horizontal and vertical padding is
        determined relative to data extent. If specified as a tuple, the first
        value specifies absolute horizontal padding in axis units and the second
        specifies absolute vertical padding in axis units.
    frame_outer_pad : Union[float, Tuple[float, float]], default 0.1
        How far from frame boundary should axis viewport fall?

        If specified as a float value, horizontal and vertical padding is
        determined relative to axis viewport. If specified as a tuple, the first
        value specifies absolute horizontal padding in axis units and the second
        specifies absolute vertical padding in axis units.
    mark_glyph : Union[Callable, Type, None], optional
        A callable to draw a glyph at the end of the callout.

        Defaults to a magnifying glass. Outset also provides implementations
        for arrow, asterisk, and letter/number glyphs. If a type is provided,
        it will be default initialized prior to being called as a functor. If
        None is provided, no glyph will be drawn.
    palette : Sequence, optional
        Color palette for plotting.

        If None, the default seaborn color palette is used. Passing `color`
        kwarg overrides `palette`.
    **kwargs
        Additional keyword arguments forward to `draw_marquee`.

    Returns
    -------
    Tuple[matplotlib.axes.Axes, List[Tuple[float, float, float, float]]]
            The matplotlib axes containing the plot.
    """
    if ax is None:
        ax = plt.gca()

    if palette is None:
        palette = sns.color_palette()

    if hue is not None and color is not None:
        raise ValueError(f"cannot specify both hue={hue} and color={color}")

    if isinstance(mark_glyph, type):
        mark_glyph = mark_glyph()

    # pad axes out from data to ensure consistent outplot annotation sizing
    if len(data):
        plotted_data = (
            data[data[outset].isin(outset_order)]
            if outset is not None and outset_order is not None
            else data
        )
        if tight_axlim or is_axes_unset(ax):  # disregard existing axlim
            if np.ptp(plotted_data[x]):
                ax.set_xlim(plotted_data[x].min(), plotted_data[x].max())
            if np.ptp(plotted_data[y]):
                ax.set_ylim(plotted_data[y].min(), plotted_data[y].max())
        else:  # ensure no shrink of existing axlim
            ax_xlim, ax_ylim = ax.get_xlim(), ax.get_ylim()
            ax.set_xlim(
                min(plotted_data[x].min(), ax_xlim[0]),
                max(plotted_data[x].max(), ax_xlim[1]),
            )
            ax.set_ylim(
                min(plotted_data[y].min(), ax_ylim[0]),
                max(plotted_data[y].max(), ax_ylim[1]),
            )

    if isinstance(frame_outer_pad, numbers.Number):
        # convert to absolute units to prevent weird effects from
        # successive calls to draw_marquee
        frame_outer_pad = (
            frame_outer_pad * np.ptp(ax.get_xlim()),
            frame_outer_pad * np.ptp(ax.get_ylim()),
        )

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

    assert "_dummy_hue_key" not in data.columns
    assert "_dummy_outset_key" not in data.columns
    data["_dummy_hue_key"] = data[hue].map(hue_order.index)
    data["_dummy_outset_key"] = data[outset].map(outset_order.index)
    data.sort_values(["_dummy_hue_key", "_dummy_outset_key"], inplace=True)

    for (_outset_value, hue_value), subset in data[
        data[outset].isin(outset_order) & data[hue].isin(hue_order)
    ].groupby([outset, hue], sort=False):
        assert len(subset)

        if isinstance(frame_inner_pad, numbers.Number):
            # convert to absolute units to prevent weird effects from
            # successive calls to draw_marquee
            frame_inner_pad_ = (
                frame_inner_pad * (np.ptp(subset[x]) or np.ptp(ax.get_xlim())),
                frame_inner_pad * (np.ptp(subset[y]) or np.ptp(ax.get_ylim())),
            )
        else:
            frame_inner_pad_ = frame_inner_pad

        xlim = [subset[x].min(), subset[x].max()]
        ylim = [subset[y].min(), subset[y].max()]
        selected_color = color_lookup[hue_value]
        draw_marquee(
            frame_xlim=xlim,
            frame_ylim=ylim,
            ax=ax,
            color=selected_color,
            frame_inner_pad=frame_inner_pad_,
            frame_outer_pad=frame_outer_pad,
            mark_glyph=mark_glyph,
            **kwargs,
        )

    return ax
