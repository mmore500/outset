import numpy as np

from outset.stub import CalcBoundsIQR


def test_empty_dataset():
    data = np.array([])
    lower_bound_empty, upper_bound_empty = CalcBoundsIQR()(data)
    assert lower_bound_empty == 0.0
    assert upper_bound_empty == 0.0


def test_singleton_dataset():
    data = np.array([3])
    lower_bound_same, upper_bound_same = CalcBoundsIQR()(data)
    assert lower_bound_same == 3.0
    assert upper_bound_same == 3.0


def test_same_value_dataset():
    data_same_value = np.array([3] * 10)
    lower_bound_same, upper_bound_same = CalcBoundsIQR()(data_same_value)
    assert lower_bound_same == 3.0
    assert upper_bound_same == 3.0


def test_typical_dataset():
    data = np.array([1, 2, 3, 4, 5, 100])
    assert CalcBoundsIQR(iqr_multiplier=2.0)(data) == (-2.75, 9.75)


def test_zero_multiplier():
    data = np.array([1, 2, 3, 4, 5, 100])
    assert CalcBoundsIQR(iqr_multiplier=0.0)(data) == (2.25, 4.75)
