import typing

import pandas as pd


def robust_groupby(
    data: pd.DataFrame,
    by: typing.List[typing.Optional[str]],
    **kwargs,
) -> typing.Iterable[
    typing.Tuple[typing.Union[typing.Tuple, str, None], pd.DataFrame]
]:
    """Perform a grouping operation on a pandas DataFrame that is robust to
    `by` sequences that are empty or contain None values.

    Extends the standard pandas groupby functionality by handling cases
    where grouping keys may contain None values.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame to be grouped.
    by : typing.List[typing.Optional[str]]
        A list of column names to group by. None values in the list are ignored.
    **kwargs
        Additional keyword arguments to be passed to pandas.DataFrame.groupby.

    Returns
    -------
    typing.Iterable[typing.Tuple[typing.Union[typing.Tuple, str, None], pd.DataFrame]]
        An iterable of tuples, each containing contains the group key(s) and
        the corresponding grouped DataFrame.

        If 'by' is empty after filtering None, returns a tuple with
        None as the key and the original DataFrame.
    """
    by = list(filter(bool, by))
    if by:
        return data.groupby(by=by, **kwargs)
    else:
        return [(None, data)]
