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
    hue: typing.Optional[str] = None,
    hue_order: typing.Optional[typing.Sequence] = None,
    ax: typing.Optional[mpl_Axes] = None,
    frame_inner_pad: float = 0.1,
    palette: typing.Optional[typing.Sequence] = None,
    **kwargs,
) -> typing.Tuple[mpl_Axes, typing.List[typing.Tuple[float, float]]]:
    """Creates outset annotation(s) containing specified x, y points from a
    pandas DataFrame, potentially within-color coded groups determined by a
    categorical column `hue`.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the data to be plotted.
    x : str
        Name of the column in `data` to be used for x-axis values.
    y : str
        Name of the column in `data` to be used for y-axis values.
    hue : str, optional
        Name of the categorical column in `data` to produce different-colored annotated subsets.

        If provided, colors are chosen according to palette.
    hue_order : Sequence, optional
        Order to plot the categorical levels in.

        If None, hues are assigned based on hue column sorted order.
     ax : matplotlib.axes.Axes, optional
        Matplotlib Axes object to draw the plot on. If None, the current axes are used.
    frame_inner_pad : float, default 0.1
        How far from data range should rectangular boundary fall?

        Padding is determined relative to axis viewport.
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

    if hue is not None:
        if hue_order is None:
            hue_order = sorted(data[hue].unique())
        groups = data.groupby(hue, sort=False)
        # adapted from https://stackoverflow.com/a/39275799
    else:
        if hue_order is not None:
            raise ValueError("hue_order cannot be specified without hue")
        hue_order = [None]
        groups = [(None, data)]

    palette_lookup = dict(zip(hue_order, it.cycle(palette)))
    frames = dict()
    for hue_value, subset in groups:
        assert len(subset)
        if hue_value not in palette_lookup:
            continue

        xlim = [subset[x].min(), subset[x].max()]
        ylim = [subset[y].min(), subset[y].max()]
        color = palette_lookup[hue_value]
        __, frame = draw_outset(
            xlim,
            ylim,
            ax,
            color=kwargs.get("color", color),
            frame_inner_pad=frame_inner_pad,
            **kwargs,
        )
        frames[hue_value] = frame

    return ax, [frames[hue_value] for hue_value in hue_order]
