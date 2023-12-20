import typing

from matplotlib import axes as mpl_axes

_color_t = typing.Union[typing.Tuple, str]

from ._MarkAlphabeticalBadges import MarkAlphabeticalBadges


class MarkRomanBadges:
    """Functor to mark roman numeral badges numbered by itertools-like count.

    This class renders markers as roman numerals overlaid onto a circular badge
    with a slightly larger circular underlay. Both lower and uppercase numerals
    are supported.

    Notes
    -----
    Due to unicode limitations values greater than twelve will not display
    correctly. Numeral representation for zero is not supported.
    """

    _ftor: MarkAlphabeticalBadges

    def __init__(
        self: "MarkRomanBadges",
        start: int = 1,
        step: int = 1,
        *,
        upper: bool = False,
        **kwargs,
    ) -> None:
        """Initialize functor.

        Parameters
        ----------
        start : int, default 1
            The starting number for the numerical badges.

            Must be between 1 and 12, inclusive.
        step : int, default 1
            The step size for the numerical badges.
        upper : bool, default False
            Should numerals be uppercase?
        kwwargs : dict
            Additional kwargs forward to `__call__`.
        """
        if start < 1 or start > 12:
            raise ValueError(f"Start value {start} outside supported range.")
        # RE unicode roman numerals, see
        # https://www.johndcook.com/blog/2020/10/07/roman-numerals/ and
        # https://en.wikipedia.org/wiki/Numerals_in_Unicode#Roman_numerals
        base = 0x215F if upper else 0x216F
        self._ftor = MarkAlphabeticalBadges(
            start=chr(base + start), step=step, **kwargs
        )

    ftor = MarkAlphabeticalBadges()

    def __call__(
        self: "MarkRomanBadges",
        x: float,
        y: float,
        ax: typing.Optional[mpl_axes.Axes] = None,
        *,
        color: str = "black",
        color_accent: str = "white",
        color_numeral: _color_t = "color_accent",
        color_badge: _color_t = "color",
        color_underlay: _color_t = "color_accent",
        marker_badge: str = "o",
        marker_underlay: str = "o",
        markersize: float = 22,
        numeral_edgewidth: float = 0,
        scale_numeral: float = 0.4,
        scale_badge: float = 0.8,
        **kwargs,
    ) -> None:
        """Draw roman numeral badge marker at specified location.

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
        self._ftor(
            x=x,
            y=y,
            ax=ax,
            color=color,
            color_accent=color_accent,
            color_letter=color_numeral,
            color_badge=color_badge,
            color_underlay=color_underlay,
            letter_edgewidth=numeral_edgewidth,
            marker_badge=marker_badge,
            marker_underlay=marker_underlay,
            markersize=markersize,
            scale_letter=scale_numeral,
            scale_badge=scale_badge,
            **{
                "linecolor": "none",
                **kwargs,
            },
        )
