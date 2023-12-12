import typing

import frozendict
from matplotlib import axes as mpl_axes
import numpy as np
import pandas as pd
import seaborn as sns

from ._auxlib.calc_aspect_ import calc_aspect
from ._auxlib.equalize_aspect_ import equalize_aspect
from ._auxlib.set_aspect_ import set_aspect
from ._calc_outset_frames import calc_outset_frames
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
        data: pd.DataFrame,
        *,
        x: str,
        y: str,
        outset: str,
        outset_order: typing.Optional[typing.Sequence[str]] = None,
        equalize_aspect: bool = True,
        col_wrap: typing.Optional[int] = None,
        color: typing.Optional[str] = None,  # pass to override outset hues
        frame_inner_pad: float = 0.1,
        leader_stretch_outplots: float = 0,
        outsetplot_kwargs: typing.Dict = frozendict.frozendict(),
        palette: typing.Optional[typing.Sequence] = None,
        sourceplot: bool = True,
        sourceplot_kwargs: typing.Dict = frozendict.frozendict(),
        **kwargs,
    ) -> None:
        """Create an OutsetGrid with specified configuration.

        Parameters
        ----------
        data : pd.DataFrame
            The data frame containing the data to be plotted.
        x : str
            The name of the column in `data` to be used for the x-axis values.
        y : str
            The name of the column in `data` to be used for the y-axis values.
        outset : str, optional
            Name of the categorical column in `data` to produce different-colored annotated subsets.

            If provided, colors are chosen according to palette.
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
        leader_stretch_outplots : float, default 0
            Scales callout annotation in outplots, default collapsed.
        outsetplot_kwargs : dict, default frozendict.frozendict()
            Additional keyword arguments for outsetplot function over outset
            plots.
        palette : Optional[Sequence], default None
            Color palette for the outset hue sequence.
        sourceplot : bool, default True
            If True, includes the source plot that outset plots are excerpted
            from as the first axis in the grid.
        sourceplot_kwargs : dict, default frozendict.frozendict()
            Additional keyword arguments for outsetplot function over the source plot.
        **kwargs : dict
            Additional keyword arguments passed to seaborn's FacetGrid.
        """

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
            hue=outset if color is None else None,
            hue_order=outset_order if color is None else None,
            col_wrap=col_wrap,
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
            outsetplot(
                data,
                x=x,
                y=y,
                outset=outset,
                outset_order=outset_order,
                ax=self.sourceplot_axes,
                frame_inner_pad=absolute_pads,
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
