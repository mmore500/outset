import numbers
import typing
import warnings

import numpy as np
from matplotlib import axes as mpl_axes

# for several implementations, we need to calculate the padding size that will
# create the correct proportions AFTER padding has been set
# here's the math:
# because pad_axfrac * end_axdatawidth = end_paddatawidth
# so pad_axfrac = end_paddatawidth / end_axdatawidth
# and end_axdatawidth = start_axdatawidth + end_paddatawidth * 2
# so ...
# pad_axfrac = end_paddatawidth / (start_axdatawidth + end_paddatawidth * 2)
# paf = epdw / (sadw + epdw * 2)
# paf = 1 / (sadw / epdw + 2)
# paf * (sadw / epdw + 2) = 1
# paf * sadw / epdw + paf * 2 = 1
# paf * sadw / epdw = 1 - paf * 2
# paf * sadw = epdw * (1 - paf * 2)
# which provides
# epdw = paf * sadw / (1 - paf * 2)


def _calc_outer_pad_axes(
    ax: mpl_axes.Axes, frame_outer_pad: float
) -> typing.Tuple[float, float]:
    """Calculate width in data units necessary for pad to be a fraction
    `frame_outer_pad` of axes size."""
    if frame_outer_pad >= 0.5:
        warnings.warn("axes-proportional pad exceeds half axes size")
    pad_x = frame_outer_pad * np.ptp(ax.get_xlim()) / (1 - frame_outer_pad * 2)
    pad_y = frame_outer_pad * np.ptp(ax.get_ylim()) / (1 - frame_outer_pad * 2)
    assert np.isclose(
        (np.ptp(ax.get_xlim()) + 2 * pad_x) * frame_outer_pad, pad_x
    )
    assert np.isclose(
        (np.ptp(ax.get_ylim()) + 2 * pad_y) * frame_outer_pad, pad_y
    )
    return pad_x, pad_y


def _calc_outer_pad_figure(
    ax: mpl_axes.Axes, frame_outer_pad: float
) -> typing.Tuple[float, float]:
    """Calculate width in data units necessary for pad to be a fraction
    `frame_outer_pad` of figure size."""
    if frame_outer_pad >= 0.5:
        raise ValueError(
            "frame_outer_pad must be less than 0.5 when "
            "frame_outer_pad_unit='figure'",
        )
    pad_x_axfrac = frame_outer_pad / ax.get_position().width
    pad_y_axfrac = frame_outer_pad / ax.get_position().height
    if pad_x_axfrac >= 0.5:
        warnings.warn("figure-proportional x pad exceeds half axes size")
    if pad_y_axfrac >= 0.5:
        warnings.warn("figure-proportional y pad exceeds half axes size")

    # same padding proportion after application math as for axes
    pad_x = pad_x_axfrac * np.ptp(ax.get_xlim()) / (1 - pad_x_axfrac * 2)
    pad_y = pad_y_axfrac * np.ptp(ax.get_ylim()) / (1 - pad_y_axfrac * 2)
    assert np.isclose((np.ptp(ax.get_xlim()) + 2 * pad_x) * pad_x_axfrac, pad_x)
    assert np.isclose((np.ptp(ax.get_ylim()) + 2 * pad_y) * pad_y_axfrac, pad_y)

    return pad_x, pad_y


def _calc_outer_pad_inches(
    ax: mpl_axes.Axes, frame_outer_pad: float
) -> typing.Tuple[float, float]:
    """Calculate width in data units necessary for pad to be rendered as `frame_outer_pad` inches."""
    axwidth_inches = ax.get_position().width * ax.figure.get_figwidth()
    axheight_inches = ax.get_position().height * ax.figure.get_figheight()
    pad_x_axfrac = frame_outer_pad / axwidth_inches
    pad_y_axfrac = frame_outer_pad / axheight_inches
    if pad_x_axfrac >= 0.5:
        warnings.warn("inch-specified x pad exceeds half axes size")
    if pad_y_axfrac >= 0.5:
        warnings.warn("inch-specified y pad exceeds half axes size")

    # same padding proportion after application math as for axes
    pad_x = pad_x_axfrac * np.ptp(ax.get_xlim()) / (1 - pad_x_axfrac * 2)
    pad_y = pad_y_axfrac * np.ptp(ax.get_ylim()) / (1 - pad_y_axfrac * 2)
    assert np.isclose((np.ptp(ax.get_xlim()) + 2 * pad_x) * pad_x_axfrac, pad_x)
    assert np.isclose((np.ptp(ax.get_ylim()) + 2 * pad_y) * pad_y_axfrac, pad_y)

    return pad_x, pad_y


def calc_outer_pad(
    ax: mpl_axes.Axes, frame_outer_pad: float, frame_outer_pad_unit: str
) -> typing.Tuple[float, float]:
    """Calculate pad width in data units."""
    if isinstance(frame_outer_pad, numbers.Number):
        try:
            return {
                "axes": _calc_outer_pad_axes,
                "figure": _calc_outer_pad_figure,
                "inches": _calc_outer_pad_inches,
            }[frame_outer_pad_unit](ax, frame_outer_pad)
        except KeyError:
            raise ValueError(
                "frame_outer_pad_unit must be 'axes', 'figure', or 'inches',"
                f"not '{frame_outer_pad_unit}'",
            )
    else:
        return frame_outer_pad
