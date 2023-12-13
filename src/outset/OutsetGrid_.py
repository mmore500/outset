import copy
import typing

import frozendict
from matplotlib import axes as mpl_axes
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from ._auxlib.calc_aspect_ import calc_aspect
from ._auxlib.equalize_aspect_ import equalize_aspect
from ._auxlib.set_aspect_ import set_aspect
from ._calc_outset_frames import calc_outset_frames
from .MarkNumericalBadges_ import MarkNumericalBadges
from .outsetplot_ import outsetplot


class _SentryType:
    def __hash__(self: "_SentryType") -> int:
        return 0


class OutsetGrid(sns.axisgrid.FacetGrid):
    """Facilitates co-display of zoomed-in axis insets transplanted outside the
     source plot ("outsets"), optionally with or without the original source
    plot.

    Mirrors the API of seaborn's FacetGrid.

    Attributes
    ----------
    sourceplot_axes : Optional[mpl_axes.Axes]
        The axes object for the source plot, if present.
    """

    __data: pd.DataFrame
    sourceplot_axes: typing.Optional[mpl_axes.Axes]

    def __init__(
        self: "OutsetGrid",
        data: typing.Union[
            pd.DataFrame,
            typing.Sequence[typing.Tuple[float, float, float, float]],
        ],
        *,
        x: str = "x",
        y: str = "y",
        outset: str = "outset",
        outset_order: typing.Optional[typing.Sequence[str]] = None,
        equalize_aspect: bool = True,
        col_wrap: typing.Optional[int] = None,
        color: typing.Optional[str] = None,  # pass to override outset hues
        frame_inner_pad: float = 0.1,
        frame_outer_pad: float = 0.1,
        leader_stretch_outplots: float = 0,
        mark_glyph: typing.Union[
            typing.Callable, typing.Type, None
        ] = MarkNumericalBadges,
        outsetplot_kwargs: typing.Dict = frozendict.frozendict(),
        palette: typing.Optional[typing.Sequence] = None,
        sourceplot: bool = True,
        sourceplot_kwargs: typing.Dict = frozendict.frozendict(),
        sourceplot_xlim: typing.Optional[typing.Tuple[float, float]] = None,
        sourceplot_ylim: typing.Optional[typing.Tuple[float, float]] = None,
        **kwargs,
    ) -> None:
        """Create an OutsetGrid with specified configuration.

        Parameters
        ----------
        data : pd.DataFrame
            The data frame containing the data to be faceted per outplot or a
            sequence of outest frames specified as (xmin, xmax, ymin, ymax)
            tuples.
        x : str, default "x"
            The name of the column in `data` to be used for the x-axis values.

            Should not be provided if outset frames are specified directly.
        y : str, default "y"
            The name of the column in `data` to be used for the y-axis values.

            Should not be provided if outset frames are specified directly.
        outset : str, default "outset"
            Name of the categorical column in `data` to produce
            different-colored annotated subsets.

            If provided, colors are chosen according to palette. Should not be
            provided if outset frames are specified directly.
        outset_order : Sequence, optional
            Order to plot the categorical levels in.

            If None, outsets are assigned based on outset column sorted order.
        equalize_aspect : bool, default True
            If True, adjusts axis limits to enforce equal ylim height to xlim
            width ration.
        col_wrap : Optional[int], default None
            The number of columns to wrap the grid into.
        color : Optional[str], default None
            Color for all outset annotations, overrides palette.
        frame_inner_pad : float, default 0.1
            Inner padding for the frame.

            Set as zero if outset frames are specified directly.
        frame_outer_pad : float, default 0.1
            Outer padding for the frame.
        leader_stretch_outplots : float, default 0
            Scales callout annotation in outplots, default collapsed.
        mark_glyph : Union[Callable, Type, None], optional
            A callable to draw a glyph at the end of the callout.

            Defaults to a magnifying glass. Outset also provides implementations
            for arrow, asterisk, and letter/number glyphs. If a type is
            provided, it will be default initialized prior to being called as a
            functor. If None is provided, no glyph will be drawn.

            If a functor with state is provided, it should provide semantic
            deep copy support.
        outsetplot_kwargs : dict, default frozendict.frozendict()
            Additional keyword arguments for outsetplot function over outset
            plots.
        palette : Optional[Sequence], default None
            Color palette for the outset hue sequence.
        sourceplot : bool, default True
            If True, includes the source plot that outset plots are excerpted
            from as the first axis in the grid.
        sourceplot_kwargs : dict, default frozendict.frozendict()
            Additional keyword arguments for outsetplot function over the
            source plot.
        sourceplot_{x,y}lim : Optional[Tuple[float, float]], default None
            The x and y limits for the source plot.
        **kwargs : dict
            Additional keyword arguments passed to seaborn's FacetGrid.
        """

        if isinstance(mark_glyph, type):
            mark_glyph = mark_glyph()

        # spoof data frame if outset frames are specified directly
        if not isinstance(data, pd.DataFrame):
            if x != "x" or y != "y" or outset != "outset":
                raise ValueError(
                    "x, y, and outset must be 'x', 'y', and 'outset' if outest "
                    "frames are specified directly",
                )
            if outset_order is not None:
                raise ValueError(
                    "outset_order should not be provided if outset frames are "
                    "specified directly",
                )
            data = pd.DataFrame.from_records(
                [
                    {
                        "x": x,
                        "y": y,
                        "outset": i,
                    }
                    for i, (xmin, xmax, ymin, ymax) in enumerate(data)
                    for x, y in [(xmin, ymin), (xmax, ymax)]
                ],
            )
            frame_inner_pad = 0

        self.__data = data

        assert "_outset" not in data.columns
        if outset_order is None:
            outset_order = sorted(data[outset].unique())
        # adapted from https://stackoverflow.com/a/39275799

        col_order = [*outset_order]
        if sourceplot:
            # SentryType entry ensures no outset data maps to sourceplot
            col_order = [_SentryType()] + col_order

        super().__init__(  # initialize parent FacetGrid
            data,
            col=outset,
            col_order=col_order,
            col_wrap=col_wrap,
            hue=outset if color is None else None,
            hue_order=outset_order if color is None else None,
            **{
                "legend_out": False,
                "sharex": False,
                "sharey": False,
                **kwargs,
            },
        )

        # direct pads to ensure consistency between sourceplot and outsetplot
        absolute_pads = (
            np.ptp(data[x] * frame_inner_pad),
            np.ptp(data[y] * frame_inner_pad),
        )

        # draw sourceplot
        #######################################################################
        if sourceplot:
            self.sourceplot_axes = self.axes.flat[0]
            if sourceplot_xlim is not None:
                self.sourceplot_axes.set_xlim(*sourceplot_xlim)
            if sourceplot_ylim is not None:
                self.sourceplot_axes.set_ylim(*sourceplot_ylim)
            outsetplot(
                data,
                x=x,
                y=y,
                outset=outset,
                outset_order=outset_order,
                ax=self.sourceplot_axes,
                frame_inner_pad=absolute_pads,
                frame_outer_pad=frame_outer_pad,
                mark_glyph=copy.deepcopy(mark_glyph),
                **{
                    "color": color,
                    "palette": palette,
                    **sourceplot_kwargs,
                },
            )
            self.sourceplot_axes.set_title(None)
        else:
            self.sourceplot_axes = None

        # draw outplots
        #######################################################################
        self.map_dataframe(
            outsetplot,
            x=x,
            y=y,
            frame_inner_pad=absolute_pads,
            frame_outer_pad=frame_outer_pad,
            mark_glyph=mark_glyph,
            **{
                "color": color,
                "leader_stretch": leader_stretch_outplots,
                "palette": palette,
                **outsetplot_kwargs,
            },
        )

        # finalize
        #######################################################################
        if equalize_aspect:
            self.equalize_aspect()

    def equalize_aspect(self: "OutsetGrid") -> "OutsetGrid":
        """Adjust axes {x,y}lims to ensure an equal xlim-to-ylim ratio across
        all axes.

        Returns
        -------
        OutsetGrid
            Returns self.
        """
        if self.sourceplot_axes is not None:
            aspect = calc_aspect(self.sourceplot_axes)
            for ax in self.axes.flat[1:]:
                set_aspect(ax, aspect)
        else:
            equalize_aspect(self.axes.flat)
        return self

    def map_dataframe(self, *args, **kwargs) -> "OutsetGrid":
        """Map a plotting function over only the outset axes excerpted from
        the sourceplot.

        Parameters
        ----------
        *args : tuple
            Positional arguments passed to the plotting function.
        **kwargs : dict
            Keyword arguments passed to the plotting function.

        Returns
        -------
        OutsetGrid
            Returns self.
        """
        # explicitly include instead of inheriting in order to document
        super().map_dataframe(*args, **kwargs)
        return self

    def map_dataframe_all(
        self: "OutsetGrid", plotter: typing.Callable, *args, **kwargs
    ) -> "OutsetGrid":
        """Map a plotting function over all axes, including the source plot
        axis (if present).

        Parameters
        ----------
        plotter : Callable
            The plotting function to be applied to each axis.
        *args : tuple
            Positional arguments passed to the plotting function.
        **kwargs : dict
            Keyword arguments passed to the plotting function.

        Returns
        -------
        OutsetGrid
            Returns self.
        """
        self.map_dataframe(plotter, *args, **kwargs)
        if self.sourceplot_axes is not None:
            kwargs.pop("_outset_preserve_axlim", None)
            plotter(self.__data, *args, ax=self.sourceplot_axes, **kwargs)
        return self

    def broadcast(
        self: "OutsetGrid",
        plotter: typing.Callable,
        *args,
        **kwargs,
    ) -> "OutsetGrid":
        """Map a plotting function over all axes, including the source plot
        axis (if present), but with the same data and arguments for all.

        Parameters
        ----------
        plotter : Callable
            The plotting function to be applied to each axis.
        *args : tuple
            Positional arguments passed to the plotting function.
        **kwargs : dict
            Keyword arguments passed to the plotting function.

        Returns
        -------
        OutsetGrid
            Returns self.

        Notes
        -----
        Does not use data stored from initialization. Data should be provided via argument to this method.

        Preserves axis limits for all axes except the sourceplot, if present.
        """
        for i, ax in enumerate(self.axes.flat):
            # store and restore axis limits, except for sourceplot if present
            xlim, ylim = ax.get_xlim(), ax.get_ylim()
            try:
                plotter(*args, ax=ax, **kwargs)
            except TypeError:
                plt.sca(ax)
                plotter(*args, **kwargs)
            if i or self.sourceplot_axes is None:
                ax.set_xlim(*xlim)
                ax.set_ylim(*ylim)
        return self
