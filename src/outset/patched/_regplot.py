import itertools as it
import typing

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from typing import Optional, Any, Dict


def regplot(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    hue: Optional[str] = None,
    hue_order: Optional[Any] = None,
    ax: Optional[plt.Axes] = None,
    **kwargs: Dict[str, Any],
) -> plt.Axes:
    """Plot regressions with seaborn's regplot on a pandas DataFrame.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the data to plot.
    x : str
        The name of the column in `data` to use for the x-axis values.
    y : str
        The name of the column in `data` to use for the y-axis values.
    hue : Optional[str], default None
        The name of the column in `data` to use for color encoding.
    hue_order : Optional[Any], default None
        The order to plot the `hue` levels, if `hue` is not None.
    ax : Optional[plt.Axes], default None
        The matplotlib Axes object to draw the plot onto, if provided.
    **kwargs
        Additional keyword arguments forward to seaborn's regplot.

    Returns
    -------
    plt.Axes
        The matplotlib Axes containing the plot.

    Notes
    -----
    This function extends seaborn's regplot functionality by adding support for
    hue-based grouping and customizing plot aesthetics.
    """
    data = data.copy()
    if ax is None:
        ax = plt.gca()
    palette = kwargs.pop("palette", sns.color_palette())
    if hue is None:
        hue = "_dummy_hue"
        data[hue] = 0

    if hue_order is None:
        hue_order = sorted(data[hue].unique())

    data["_hue_order"] = data[hue].map(hue_order.index)
    data.sort_values("_hue_order")

    for color, (_value, group) in zip(
        it.cycle(palette),
        data.groupby(hue, sort=False),
    ):
        sns.regplot(
            data=group,
            x=x,
            y=y,
            ax=ax,
            **{
                "color": color,
                **kwargs,
            },
        )
    return ax
