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
) -> mpl_Axes:
    """Plot marquee annotations to contain subsets of data from a pandas DataFrame.

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
    mark_glyph : Union[Callable, Type, None], optional
        Callable or type to draw a glyph at the end of the callout.
    palette : Sequence, optional
        Color palette for plotting elements.
    tight_axlim : bool, default False
        Whether to shrink axes limits to fit data range.
    **kwargs
        Additional keyword arguments forwarded to `draw_marquee`.

    Returns
    -------
    matplotlib.axes.Axes
        The Matplotlib axes containing the plot with annotated regions.

    See Also
    --------
    OutsetGrid
        Figure-level interface for creating plots with marquee annotations.
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
