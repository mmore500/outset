import typing
import matplotlib.pyplot as plt
from matplotlib import axes as mpl_axes
import numpy as np


class TweakSpreadArea:
    """Functor to spread apart a crowded axes area.

    The adjustment is applied by moving the vertex away from the centroid of the parametrized x/y limits, scaled by a spread factor.
    """

    _spread_factor: typing.Tuple[float, float]
    _xlim: typing.Optional[typing.Tuple[float, float]]
    _ylim: typing.Optional[typing.Tuple[float, float]]

    def __init__(
        self: "TweakSpreadArea",
        spread_factor: typing.Union[float, typing.Tuple[float, float]] = 2.0,
        *,
        xlim: typing.Optional[typing.Tuple[float, float]] = None,
        ylim: typing.Optional[typing.Tuple[float, float]] = None,
    ) -> None:
        """
        Initialize the TweakSpreadArea functor.

        Parameters
        ----------
        spread_factor : Union[float, Tuple[float, float]], optional
            How aggressively to spread apart x and/or y coordinates.

            If a tuple is provided, the first element is used for x-coordinate
            spread and the second for y-coordinate spread. If a single float is
            provided, it is used for both.
        xlim : Optional[Tuple[float, float]], optional
            If provided, outer vertices falling within the x-coordinate range will be spread horizontally away from the range's centroid.
        ylim : Optional[Tuple[float, float]], optional
            If provided, outer vertices falling within the y-coordinate range will be spread vertically away from the range's centroid.
        """

        if isinstance(spread_factor, tuple):
            self._spread_factor = spread_factor
        else:
            self._spread_factor = (spread_factor, spread_factor)
        self._xlim = xlim
        self._ylim = ylim

    def __call__(
        self: "TweakSpreadArea",
        leader_vertices: typing.Sequence[typing.Tuple[float, float]],
        ax: typing.Optional[mpl_axes.Axes] = None,
    ) -> typing.List[typing.Tuple[float, float]]:
        """Spread outer vertex of leader polygon out from specied area.

        Parameters
        ----------
        leader_vertices : Sequence[Tuple[float, float]]
            A sequence of tuples representing the `(x, y)` coordinates of the
            leader vertices.
        ax : mpl_axes.Axes
            The matplotlib Axes object on which the leader vertices are plotted.

            Not used for this tweak.
        Returns
        -------
        List[Tuple[float, float]]
            The modified sequence of leader vertices with the outer vertex
            position adjusted.
        """
        x, y = leader_vertices[-1]

        if self._xlim is not None and np.clip(x, *self._xlim) == x:
            x_centroid = np.mean(self._xlim)
            x = x_centroid + (x - x_centroid) * self._spread_factor[0]

        if self._ylim is not None and np.clip(y, *self._ylim) == y:
            y_centroid = np.mean(self._ylim)
            y = y_centroid + (y - y_centroid) * self._spread_factor[1]

        return [*leader_vertices[:-1], (x, y)]
