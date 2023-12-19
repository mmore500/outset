import typing

from frozendict import frozendict
import numpy as np

from matplotlib.axes import Axes as mpl_Axes
from matplotlib.collections import PathCollection as mpl_PathCollection
from matplotlib.container import ErrorbarContainer as mpl_ErrorbarContainer

from .._auxlib.align_marker_ import align_marker
from .._auxlib.rotate_marker_ import rotate_marker


def stub_edge_mark(
    ax: mpl_Axes,
    x: float,
    y: float,
    *,
    marker_kwargs: typing.Dict = frozendict(),
    offset: float = 0.1,
) -> typing.Tuple[float, float]:
    """Draw an edge marker for a single clipped point.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes object to draw markers on.
    x, y : float
        The x and y coordinates of the point.
    marker_kwargs : dict, optional
        Keyword arguments forwarded to matplotlib `plot` for edge markers.
    offset : float, default 0.1
        How far outside axis viewport to draw edge markers, proportional to
        axis viewport height or width.

    Returns
    -------
    edge_x, edge_y : float
        The x and y coordinates of the placed edge marker.

    See Also
    --------
    outset.stub.stub_all_clipped_values :
        Automates out of bounds scatterpoint detection and stub creation.
    """
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    edge_x, edge_y, markers = x, y, list()

    left_marker = lambda amount: align_marker(
        rf"$\langle\!\langle\!\langle | \!\! \leftrightarrow \!\!|{{\times}}{amount}$",
        halign="left",
        pad=1.3,
    )
    right_marker = lambda amount: align_marker(
        rf"$| \!\! \leftrightarrow \!\!|{{\times}}{amount}\rangle\!\rangle\!\rangle$",
        halign="right",
        pad=1.3,
    )

    xwidth = np.ptp(xlim)
    ywidth = np.ptp(ylim)
    xoff = xwidth * offset
    yoff = ywidth * offset
    if x < xlim[0]:
        amount = int((xlim[0] - x) / xwidth)
        edge_x = xlim[0] - xoff
        markers.append(left_marker(amount))
    elif x > xlim[1]:
        amount = int((x - xlim[1]) / xwidth)
        edge_x = xlim[1] + xoff
        markers.append(right_marker(amount))
    if y < ylim[0]:
        amount = int((ylim[0] - y) / ywidth)
        edge_y = ylim[0] - yoff
        markers.append(rotate_marker(right_marker(amount), 270))
    elif y > ylim[1]:
        amount = int((y - ylim[1]) / ywidth)
        edge_y = ylim[1] + yoff
        markers.append(rotate_marker(right_marker(amount), 90))

    for marker in markers:
        ax.plot(
            edge_x,
            edge_y,
            **{
                "color": "none",
                "clip_on": False,
                "linewidth": 0,
                "color": "red",
                "marker": marker,
                "markersize": 100,
                "zorder": 10000,
                **marker_kwargs,
            },
        )

    return edge_x, edge_y
