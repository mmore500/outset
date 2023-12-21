import typing

from frozendict import frozendict
import numpy as np

from matplotlib.axes import Axes as mpl_Axes
from matplotlib.collections import PathCollection as mpl_PathCollection
from matplotlib.container import ErrorbarContainer as mpl_ErrorbarContainer

from ._stub_edge_mark import stub_edge_mark


def stub_all_clipped_values(
    ax: mpl_Axes,
    *,
    marker_kws: typing.Dict = frozendict(),
    offset: float = 0.1,
) -> None:
    """Draw edge markers for points lying outside the plot's bounds.

    The original point and associated error bar (if any) is moved into the
    margin with a note indicating the original location. If the point is out of
    xlim and out of ylim, the point will be retrieved with two edge markers
    (horizontal and vertical).

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes object to draw markers on.
    marker_kws : dict, optional
        Keyword arguments forwarded to matplotlib `plot` for edge markers.
    offset : float, default 0.1
        How far outside axis viewport to draw edge markers, proportional to
        axis viewport height or width.

    Notes
    -----
    Full error bar support for values below lower {x,y}lim remains be
    implemented. Current implementation assumes each error bar is associated
    with a scatter point.
    """
    xlim, ylim = ax.get_xlim(), ax.get_ylim()

    # move out of bounds points, if any
    for collection in ax.collections:
        if isinstance(collection, mpl_PathCollection):
            # Extract points from the line
            new_offsets = []
            for x, y in collection.get_offsets():
                # Draw edge marker if the point is out of bounds
                if x < xlim[0] or x > xlim[1] or y < ylim[0] or y > ylim[1]:
                    x, y = stub_edge_mark(
                        ax,
                        x,
                        y,
                        marker_kws=marker_kws,
                        offset=offset,
                    )
                new_offsets.append((x, y))

            collection.set_offsets(new_offsets)
            collection.set(clip_on=False)

    # move out of bounds error bars, if any
    x_width, y_height = np.ptp(xlim), np.ptp(ylim)
    x_thresh, y_thresh = xlim[1], ylim[1]
    x_offset = x_thresh + x_width * offset
    y_offset = y_thresh + y_height * offset
    for container in ax.containers:
        if isinstance(container, mpl_ErrorbarContainer):
            # Unpack the container
            (
                plotline,  # Line2D instance of x, y plot markers and/or line
                caplines,  # A tuple of Line2D instances of the error bar caps
                # A tuple of LineCollection with the horizontal and vertical
                # error ranges.
                barlinecols,
            ) = container

            # Adjust each error bar
            for barlinecol in barlinecols:
                segments = barlinecol.get_segments()
                new_segments = []
                for segment in segments:
                    (x0, y0), (x1, y1) = segment
                    if x0 > x_thresh:
                        sep = x1 - x0
                        x0, x1 = x_offset - sep / 2, x_offset + sep / 2
                    if y0 > y_thresh:
                        sep = y1 - y0
                        y0, y1 = y_offset - sep / 2, y_offset + sep / 2
                    new_segment = [(x0, y0), (x1, y1)]
                    new_segments.append(new_segment)

                barlinecol.set_segments(new_segments)
                barlinecol.set(clip_on=False)
