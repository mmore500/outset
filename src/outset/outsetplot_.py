import itertools as it
import typing

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes as mpl_Axes

from .draw_outset_ import draw_outset


def outsetplot(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    outset: typing.Optional[str] = None,
    outset_order: typing.Optional[typing.Sequence] = None,
    ax: typing.Optional[mpl_Axes] = None,
    frame_inner_pad: typing.Union[float, typing.Tuple[float, float]] = 0.1,
    palette: typing.Optional[typing.Sequence] = None,
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
        Name of the categorical column in `data` to produce different-colored annotated subsets.

        If provided, colors are chosen according to palette.
    outset_order : Sequence, optional
        Order to plot the categorical levels in.

        If None, outsets are assigned based on outset column sorted order.
    ax : matplotlib.axes.Axes, optional
        Matplotlib Axes object to draw the plot on. If None, the current axes are used.
    frame_inner_pad : Union[float, Tuple[float, float]], default 0.1
        How far from data range should rectangular boundary fall?

        If specified as a float value, horizontal and vertical padding is
        determined relative to axis viewport. If specified as a tuple, the first
        value specifies absolute horizontal padding in axis units and the second
        specifies absolute vertical padding in axis units.
    palette : Sequence, optional
        Color palette for plotting.

        If None, the default seaborn color palette is used. Passing `color`
        kwarg overrides `palette`.
    **kwargs
        Additional keyword arguments forward to `draw_outset`.

    Returns
    -------
    Tuple[matplotlib.axes.Axes, List[Tuple[float, float, float, float]]]
            The matplotlib axes containing the plot.
    """
    if ax is None:
        ax = plt.gca()

    if palette is None:
        palette = sns.color_palette()

    # grow axis limits to data, ensuring no shrink
    if len(data) and outset is not None:
        ax_xlim, ax_ylim = ax.get_xlim(), ax.get_ylim()
        ax.set_xlim(
            min(data[x].min(), ax_xlim[0]),
            max(data[x].max(), ax_xlim[1]),
        )
        ax.set_ylim(
            min(data[y].min(), ax_ylim[0]),
            max(data[y].max(), ax_ylim[1]),
        )

    # assemble data groups
    if outset is not None:
        if outset_order is None:
            outset_order = sorted(data[outset].unique())
        groups = data.groupby(outset, sort=False)
        # adapted from https://stackoverflow.com/a/39275799
    else:
        if outset_order is not None:
            raise ValueError("outset_order cannot be specified without outset")
        outset_order = [None]
        groups = [(None, data)]

    palette_lookup = dict(zip(outset_order, it.cycle(palette)))
    frames = dict()
    for outset_value, subset in groups:
        assert len(subset)
        if outset_value not in palette_lookup:
            continue

        xlim = [subset[x].min(), subset[x].max()]
        ylim = [subset[y].min(), subset[y].max()]
        color = palette_lookup[outset_value]
        __, frame = draw_outset(
            xlim,
            ylim,
            ax,
            color=kwargs.pop("color", color),
            frame_inner_pad=frame_inner_pad,
            **kwargs,
        )
        frames[outset_value] = frame

    return ax, [frames[outset_value] for outset_value in outset_order]
