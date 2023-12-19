import pandas as pd

from outset._auxlib.robust_groupby_ import robust_groupby

df = pd.DataFrame({"A": [1, 2, 1, 2], "B": [5, 6, 7, 8], "C": [9, 10, 11, 12]})


def test_groupby_single_column():
    grouped = robust_groupby(df, by=["A"])
    assert list(grouped.groups.keys()) == [1, 2]


def test_groupby_multiple_columns():
    grouped = robust_groupby(df, by=["A", "B"])
    assert list(grouped.groups.keys()) == [(1, 5), (1, 7), (2, 6), (2, 8)]


def test_groupby_with_none():
    grouped = robust_groupby(df, by=[None, "B"])
    assert list(grouped.groups.keys()) == [5, 6, 7, 8]


def test_groupby_empty_list():
    grouped = robust_groupby(df, by=[])
    assert len(grouped) == 1 and grouped[0][0] is None and grouped[0][1] is df


def test_groupby_only_none_list():
    grouped = robust_groupby(df, by=[None])
    assert len(grouped) == 1 and grouped[0][0] is None and grouped[0][1] is df
