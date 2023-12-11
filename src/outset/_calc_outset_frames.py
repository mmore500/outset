import typing

from matplotlib import pyplot as plt

from .outsetplot_ import outsetplot


def calc_outset_frames(
    *args, **kwargs
) -> typing.List[typing.Tuple[float, float, float, float]]:
    if "ax" in kwargs:
        raise ValueError("as cannot be passed to _calc_outset_frames")
    dummy_fig = plt.figure()
    dummy_ax = dummy_fig.add_subplot(111)
    _ax, res = outsetplot(*args, ax=dummy_ax, **kwargs)
    plt.close(dummy_fig)

    return res
