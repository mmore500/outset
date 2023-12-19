import itertools as it
import math
import typing

from matplotlib.transforms import Bbox as mpl_Bbox

from ._auxlib.resize_figure_to_axes_ import resize_figure_to_axes
from ._OutsetGrid import OutsetGrid
from .util._layout_corner_insets import layout_corner_insets


def inset_outsets(
    outset_grid: OutsetGrid,
    insets: typing.Union[
        typing.Literal["NE", "NW", "SE", "SW"],
        typing.Sequence[typing.Tuple[float, float, float, float]],
    ] = "NE",
    *,
    equalize_aspect: bool = True,
    strip_axes: bool = False,
    strip_labels: bool = True,
    strip_spines: bool = False,
    strip_ticks: bool = True,
    strip_titles: bool = True,
) -> None:
    """Rearrange OutsetGrid figure to superimpose outset axes over source axes.

    Parameters
    ----------
    outset_grid : OutsetGrid
        OutsetGrid to transform.
    insets : Union[Literal["NE", "NW", "SE", "SW"], Sequence[Tuple[float,
    float, float, float]]], deefault "NW"
        Where to place outset plots over source plot.

        If "NE", "NW", "SE", or "SW", the outset plots will be inset in the
        specified corner of the grid. Alternately, inset positioning can be
        specified directly by providing a sequence of tuples `(x0, y0, width, height)` for the position of each plot in fractional coordinates of
        sourceplot.
    equalize_aspect : bool, default True
        Should the aspect ratio of the inset plots be equalized?
    strip_label : bool, default True
        Should x and y labels be stripped from inset plots.
    strip_spines : bool, default False
        Should removes the spines of the inset plots.
    strip_ticks : bool, default True
        If True, removes the ticks from the inset plots.
    strip_titles : bool, default True
        If True, removes the title from the inset plots.

    Returns
    -------
    None

    See Also
    --------
    outset.util.layout_corner_insets
        Underlying engine implementing corner inset layout when "NE", "NW",
        "SE", or "SW" is passed to `inset_outsets`. The function
        `layout_corner_insets` can be called directly to provide the `insets`
        kwarg to tweak corner inset layouts.
    """
    if outset_grid.source_axes is None:
        raise ValueError("OutsetGrid missing source axes to inset outset axes")

    if isinstance(insets, str):
        insets = layout_corner_insets(outset_grid._ncol - 1, insets)

    outset_grid.figure.tight_layout()

    # Shrink axes to fit the source axes
    resize_figure_to_axes(outset_grid.figure, outset_grid.source_axes)

    # Get position and size of the source axes
    source_pos = outset_grid.source_axes.get_position()

    # Create and customize inset subplots based on the provided rectangles
    for ax, (rel_x0, rel_y0, rel_w, rel_h) in zip(
        outset_grid.outset_axes,
        insets,
        strict=True,
    ):
        # Calculate absolute position and size of each inset subplot
        abs_x0 = source_pos.x0 + rel_x0 * source_pos.width
        abs_y0 = source_pos.y0 + rel_y0 * source_pos.height
        abs_w = rel_w * source_pos.width
        abs_h = rel_h * source_pos.height

        assert -0.01 <= abs_x0 <= 1.01, abs_x0
        assert -0.01 <= abs_y0 <= 1.01, abs_y0
        assert -0.01 <= abs_w <= 1.01, abs_w
        assert -0.01 <= abs_h <= 1.01, abs_h
        assert -0.01 <= abs_x0 + abs_w <= 1.01, abs_x0 + abs_w
        assert -0.01 <= abs_y0 + abs_h <= 1.01, abs_y0 + abs_h

        # Set position of each inset subplot
        ax.set_position(mpl_Bbox.from_bounds(abs_x0, abs_y0, abs_w, abs_h))

        # Additional customization (removing labels, spines, etc.)
        if strip_axes:
            ax.set_axis_off()
        if strip_labels:
            ax.set_xlabel("")
            ax.set_ylabel("")
        if strip_spines:
            for spine in ax.spines.values():
                spine.set_visible(False)
        if strip_ticks:
            ax.tick_params(
                left=False, bottom=False, labelleft=False, labelbottom=False
            )
        if strip_titles:
            ax.set_title("")

    # Equalize aspect ratios
    if equalize_aspect:
        outset_grid.equalize_aspect()
