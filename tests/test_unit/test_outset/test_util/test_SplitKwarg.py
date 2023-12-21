from outset.util import SplitKwarg


def test_split_kwarg_initialization():
    source_val = "source_data"
    outset_val = "outset_data"

    split_kwarg = SplitKwarg(source=source_val, outset=outset_val)

    assert split_kwarg.source == source_val
    assert split_kwarg.outset == outset_val
