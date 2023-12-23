from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


def scatterplot(
    data: pd.DataFrame,
    *args: list,
    **kwargs: dict,
) -> plt.Axes:
    """Wrapper around sns.scatterplot patching seaborn issue #3601.

    See https://github.com/mwaskom/seaborn/issues/3601.
    """

    filter = data.index == data.index
    if "hue" in kwargs and "hue_order" in kwargs:
        filter &= data[kwargs["hue"]].isin(kwargs["hue_order"])

    if "style" in kwargs and "style_order" in kwargs:
        filter &= data[kwargs["style"]].isin(kwargs["style_order"])

    data = data[filter].reset_index()

    return sns.scatterplot(data, *args, **kwargs)
