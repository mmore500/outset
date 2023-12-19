import warnings

from matplotlib import axes as mpl_axes
import numpy as np

from .calc_aspect_ import calc_aspect


def set_aspect(ax: mpl_axes.Axes, aspect: float) -> None:
    """Adjust the ratio between ylim span length and xlim span length.

    The function calculates the current aspect ratio of the Axes object and
    adjusts its x-axis or y-axis limits to match the desired aspect ratio.
    If the desired aspect ratio is less than the current, the function
    increases the width of the x-axis. If it is greater, the height of the
    y-axis is increased.

    Note that axes limits are only ever widened. Axes widening is performed
    symmetrically.
    """
    before_aspect = calc_aspect(ax)
    if 0.99 < aspect / before_aspect < 1.01:
        return

    (x0_, x1_), (y0_, y1_) = ax.get_xlim(), ax.get_ylim()
    before_width, before_height = np.ptp(ax.get_xlim()), np.ptp(ax.get_ylim())

    before_ratio = before_height / before_width
    ax.set_aspect(aspect, adjustable="datalim")
    after_ratio = np.ptp(ax.get_ylim()) / np.ptp(ax.get_xlim())

    # manual touch-up to ensure growth (not shrink) that is symmetrical
    if before_ratio == after_ratio:
        # The current aspect ratio matches the targeted one, no action needed
        # just need to ensure matplotlib didn't arbitrarily move axis limits
        ax.set_xlim(x0_, x1_)
        ax.set_ylim(y0_, y1_)
        assert ax.get_xlim() == (x0_, x1_) and ax.get_ylim() == (y0_, y1_)
    elif after_ratio < before_ratio:
        # plot is too tall so we need to increase the width.
        # in this case, before_height == after_height
        after_width = before_height / after_ratio
        assert after_width >= before_width
        pad = (after_width - before_width) / 2
        assert pad >= 0
        ax.set_xlim(x0_ - pad, x1_ + pad)
        ax.set_ylim(y0_, y1_)
    elif after_ratio > before_ratio:
        # plot is too wide so we need to increase the height.
        # in this case, before_width == after_width
        after_height = before_width * after_ratio
        assert after_height >= before_height
        pad = (after_height - before_height) / 2
        assert pad >= 0
        ax.set_xlim(x0_, x1_)
        ax.set_ylim(y0_ - pad, y1_ + pad)
    else:
        assert False

    # check postconditions...
    # ...targeted aspect ratio was achieved
    # ...axes limit pad-out was outwards and symmetrical
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    aspect_err = aspect / calc_aspect(ax) - 1
    info = (
        f"aspect={aspect}, aspect_err={aspect_err}, "
        f"before_ratio == after_ratio {before_ratio == after_ratio}, "
        f"before_ratio={before_ratio}, after_ratio={after_ratio}, "
        f"x0_={x0_}, x1_={x1_}, y0_={y0_}, y1_={y1_}, "
        f"x0={x0}, x1={x1}, y0={y0}, y1={y1}"
    )
    assert (x0, x1) == (x0_, x1_) or (y0, y1) == (y0_, y1_), info
    assert x0 <= x0_, info
    assert y0 <= y0_, info
    assert x1 >= x1_, info
    assert y1 >= y1_, info
    assert np.isclose(x0 - x0_, x1_ - x1)
    assert np.isclose(y0 - y0_, y1_ - y1)
    if aspect_err > 0.05:
        warnings.warn(f"set_aspect {aspect_err * 100}% error")
