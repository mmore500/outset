import typing

from frozendict import frozendict
import numpy as np

from matplotlib.axes import Axes as mpl_Axes
from matplotlib.collections import PathCollection as mpl_PathCollection
from matplotlib.container import ErrorbarContainer as mpl_ErrorbarContainer

from ._auxlib.align_marker_ import align_marker


def stub_edge_mark(
    ax: mpl_Axes,
    x: float,
    y: float,
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
    stub_all_clipped_values : Automates out of bounds scatterpoint detection
        and stub creation.
    """
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    edge_x, edge_y, markers = x, y, list()

    xwidth = np.ptp(xlim)
    ywidth = np.ptp(ylim)
    xoff = xwidth * offset
    yoff = ywidth * offset
    if x < xlim[0]:
        amount = int((xlim[0] - x) / xwidth)
        edge_x = xlim[0] - xoff
        m = rf"$\langle\!\langle\!\langle | \!\! \leftrightarrow \!\!|{{\times}}{amount}$"
        markers.append(align_marker(m, halign="left", pad=1.3))
    elif x > xlim[1]:
        amount = int((x - xlim[1]) / xwidth)
        m = rf"$| \!\! \leftrightarrow \!\!|{{\times}}{amount}\rangle\!\rangle\!\rangle$"
        edge_x = xlim[1] + xoff
        markers.append(align_marker(m, halign="right", pad=1.3))

    if y < ylim[0]:
        edge_y = ylim[0] - yoff
        amount = int((ylim[0] - y) / ywidth)
        m = rf"$\_\_ \!\!\!\!\!\!\!\!{{\widebar{{\updownarrow}}}} \!\! {{\times}}{amount} \!\! \mathbf{{\Downarrow}}\!\!\!\!\mathbf{{\Downarrow}}\!\!\!\!\mathbf{{\Downarrow}}$"
        markers.append(align_marker(m, halign="right", pad=1.3))
        # janky underline
    elif y > ylim[1]:
        amount = int((y - ylim[1]) / ywidth)
        edge_y = ylim[1] + yoff
        m = rf"$\_\_ \!\!\!\!\!\!\!\!{{\widebar{{\updownarrow}}}} \!\! {{\times}}{amount} {{\widehat{{\widehat{{\widehat{{\,\,\,\_\,}}}}}}}}$"
        markers.append(align_marker(m, halign="right", pad=1.3))
        # janky underline

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
