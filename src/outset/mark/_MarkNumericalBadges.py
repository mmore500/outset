import typing

from matplotlib import axes as mpl_axes

from ._MarkInlaidAsterisk import mark_inlaid_asterisk

_color_t = typing.Union[typing.Tuple, str]


class MarkNumericalBadges:
    """Functor to mark badges numbered by itertools-like count.

    This class renders markers as numbers overlaid onto a circular badge with a
    slightly larger circular underlay.
    """

    _counter: int
    _step: int
    _kws: dict

    def __init__(
        self: "MarkNumericalBadges", start: int = 1, step: int = 1, **kwargs
    ) -> None:
        """Initialize functor.

        Parameters
        ----------
        start : int, default 1
            The starting number for the numerical badges.
        step : int, default 1
            The step size for the numerical badges.
        kwargs : dict
            Additional kwargs will forward to `__call_`.
        """
        self._counter = start
        self._step = step
        self._kws = kwargs

    def __call__(
        self: "MarkNumericalBadges",
        x: float,
        y: float,
        ax: typing.Optional[mpl_axes.Axes] = None,
        *,
        color: str = "black",
        color_accent: typing.Optional[str] = None,
        color_numeral: _color_t = "color_accent",
        color_badge: _color_t = "color",
        color_underlay: _color_t = "color_accent",
        marker_badge: str = "o",
        marker_underlay: str = "o",
        markersize: float = 22,
        numeral_edgewidth: float = 1,
        scale_numeral: float = 0.4,
        scale_badge: float = 0.8,
        **kwargs,
    ) -> None:
        """Draw numbered badge marker at specified location.

        Numeral values increment with each call to this functor.

        Parameters
        ----------
        x : float
            The x-coordinate where the numerical badge will be placed.
        y : float
            The y-coordinate where the numerical badge will be placed.
        ax : mpl_axes.Axes, optional
            The axes object on which to draw the marker. If None, plt.gca()
            will be used.
        color : str, default "black"
            The primary color for the glyph.
        color_accent : Optional[str], optional
            The default accent color for the glyph.

            If `color` is "white", defaults "black". Otherwise, defaults
            "white".
        color_numeral : Union[str, tuple], default "white"
            The color of the numeral.
        color_badge : Union[str, tuple], default "color"
            The color of the badge.

            If "color", primary color will be substituted.
        color_underlay : Union[str, tuple], default "color_accent"
            The color of the underlay.

            If "color_accent", accent color will be substituted.
        marker_badge : str, default "o"
            The marker style for the badge.
        marker_underlay : str, default "o"
            The marker style for the underlay.
        markersize : float, default 22
            Size for glyph's largest marker element.
        numeral_edgewidth : float, default 1
            The edge width of the numeral marker.
        scale_numeral : float, default 0.4
            The scaling factor for the numeral size.
        scale_badge : float, default 0.8
            The scaling factor for the badge size.
        **kwargs : dict, optional
            Additional keyword arguments forward to matplotlib `plot`.

        Returns
        -------
        None
        """
        mark_inlaid_asterisk(
            **{
                "linecolor": "none",
                **self._kws,
                **dict(
                    x=x,
                    y=y,
                    ax=ax,
                    asterisk_edgewidth=numeral_edgewidth,
                    color=color,
                    color_accent=color_accent,
                    color_asterisk_edge=color_numeral,
                    color_asterisk_face=color_numeral,
                    color_badge=color_badge,
                    color_underlay=color_underlay,
                    marker=f"${self._counter}$",
                    marker_badge=marker_badge,
                    marker_underlay=marker_underlay,
                    markersize=markersize,
                    scale_asterisk=scale_numeral,
                    scale_badge=scale_badge,
                ),
                **kwargs,
            },
        )
        self._counter += self._step
