import itertools as it
import typing

from adjustText import adjust_text
from frozendict import frozendict
import pandas as pd
from matplotlib import pyplot as plt


def annotateplot(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    text: str,
    ax: typing.Optional[plt.Axes] = None,
    adjusttext_kws: typing.Mapping = frozendict(),
    **kwargs: dict,
) -> plt.Axes:
    """Annotate a plot coordinates with text labels, then apply adjustText to
    rearrange the labels to avoid overlaps.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the data to plot.
    x : str
        The name of the column in `data` to use for the x-axis values.
    y : str
        The name of the column in `data` to use for the y-axis values.
    text : Optional[str], default None
        The name of the column in `data` to use for text values.
    ax : Optional[plt.Axes], default None
        The matplotlib Axes object to draw the plot onto, if provided.
    adjusttext_kws : Mapping, default {}
        Additional keyword arguments forward to adjustText.
    **kwargs : dict
        Additional keyword arguments forward to seaborn's regplot.

    Returns
    -------
    plt.Axes
        The matplotlib Axes containing the plot.

    Notes
    -----
    This functionality is not provided by seaborn.
    """
    if ax is None:
        ax = plt.gca()

    kwargs.pop("legend", None)
    kwargs.pop("label", None)

    texts = [
        ax.text(row[x], row[y], row[text], **kwargs)
        for _idx, row in data.iterrows()
    ]
    adjust_text(texts, ax=ax, **adjusttext_kws)

    return ax
