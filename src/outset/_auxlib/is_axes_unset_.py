from matplotlib.axes import Axes as mpl_Axes


def is_axes_unset(ax: mpl_Axes) -> bool:
    """Test if axes limits have been set."""
    # see https://matplotlib.org/stable/users/faq.html#check-whether-a-figure-is-empty
    return not (
        len(ax.get_children()) > 10  # 10 objs in empty ax
        or ax.get_xlim() != (0.0, 1.0)  # in case axlim set manually...
        or ax.get_ylim() != (0.0, 1.0)
    )
