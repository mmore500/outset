import typing
import matplotlib.pyplot as plt
from matplotlib import axes as mpl_axes
import numpy as np


class TweakReflect:
    """Functor to change orientation of callout via reflection.

    The adjustment is applied by reflecting the leader vertices about the
    centroid of the frame. Horizontal and/or vertical reflection can be
    specified.
    """

    _horizontal: bool
    _vertical: bool

    def __init__(
        self: "TweakReflect",
        *,
        horizontal: typing.Optional[bool] = None,
        vertical: typing.Optional[bool] = None,
    ) -> None:
        """
        Initialize the TweakReflect functor.

        If neither `horizontal` or `vertical` are specified, a horizontal
        reflection will be performed.

        Parameters
        ----------
        horizontal : Optional[bool]
            Should the callout leader be reflected horizontally?
        vertical : Optional[Tuple[float, float]], optional
            Should the callout leader be reflected vertically?
        """
        if horizontal is None and vertical is None:
            self._horizontal = True
            self._vertical = False
        elif horizontal is None:
            self._horizontal = False
            self._vertical = vertical
        elif vertical is None:
            self._horizontal = horizontal
            self._vertical = False
        else:
            self._horizontal = horizontal
            self._vertical = vertical

    def __call__(
        self: "TweakReflect",
        leader_vertices: typing.Sequence[typing.Tuple[float, float]],
        ax: typing.Optional[mpl_axes.Axes] = None,
    ) -> typing.List[typing.Tuple[float, float]]:
        """Reflect leader vertices about centroid.

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
            The updated leader vertices.
        """
        v0, __, v1, __ = leader_vertices

        cx, cy = np.mean([v0, v1], axis=0)

        if self._horizontal:
            leader_vertices = [(2 * cx - x, y) for x, y in leader_vertices]
        if self._vertical:
            leader_vertices = [(x, 2 * cy - y) for x, y in leader_vertices]

        return leader_vertices
