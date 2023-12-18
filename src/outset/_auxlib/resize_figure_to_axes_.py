from matplotlib.axes import Axes as mpl_Axes
from matplotlib.figure import Figure as mpl_Figure


def resize_figure_to_axes(fig: mpl_Figure, ax: mpl_Axes) -> None:
    """Resize a matplotlib figure to fit an axes, preserving the scale and
    position of the axes.

    Parameters
    ----------
    fig : mpl_Figure
        The matplotlib figure object to be resized.
    ax : mpl_Axes
        The matplotlib axes object the figure should be resized to fit.

    Notes
    -----
    If axis labels or titles are getting cut off, you may need to call
    `Figure.tight_layout()` before running this function.
    """
    # Save the original position of the axis in inches
    original_pos = ax.get_position()
    original_pos_in_inches = [
        original_pos.x0 * fig.get_figwidth(),
        original_pos.y0 * fig.get_figheight(),
        original_pos.width * fig.get_figwidth(),
        original_pos.height * fig.get_figheight(),
    ]

    # Get the bounding box of the axis in inches
    bbox = ax.get_tightbbox(
        renderer=fig.canvas.get_renderer(),
    ).transformed(
        fig.dpi_scale_trans.inverted(),
    )

    # Set the figure size to match the axis size
    fig.set_size_inches(
        bbox.width + 2 * bbox.x0, bbox.height + 2 * bbox.y0, forward=True
    )

    # Adjust the position of the axis back to original
    new_pos = [
        original_pos_in_inches[0] / fig.get_figwidth(),
        original_pos_in_inches[1] / fig.get_figheight(),
        original_pos_in_inches[2] / fig.get_figwidth(),
        original_pos_in_inches[3] / fig.get_figheight(),
    ]
    ax.set_position(new_pos)
