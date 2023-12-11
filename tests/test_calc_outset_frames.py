import pandas as pd

from outset._calc_outset_frames import calc_outset_frames

# Sample data for testing
data = pd.DataFrame(
    {"x": [1, 2, 3, 4], "y": [1, 3, 2, 1], "hue": ["A", "B", "A", "B"]}
)


def test_calc_outset_frames():
    res = calc_outset_frames(
        data=data,
        x="x",
        y="y",
        frame_inner_pad=0,
    )
    assert res == [(1, 4, 1, 3)]


def test_calc_outest_frames_with_hue():
    res = calc_outset_frames(
        data=data,
        x="x",
        y="y",
        hue="hue",
        hue_order=["A", "B"],
        frame_inner_pad=0,
    )
    assert res == [(1, 3, 1, 2), (2, 4, 1, 3)]

    res = calc_outset_frames(
        data=data,
        x="x",
        y="y",
        hue="hue",
        hue_order=["B", "A"],
        frame_inner_pad=0,
    )
    assert res == [(2, 4, 1, 3), (1, 3, 1, 2)]

    res = calc_outset_frames(
        data=data,
        x="x",
        y="y",
        hue="hue",
        hue_order=["A"],
        frame_inner_pad=0,
    )
    assert res == [(1, 3, 1, 2)]
