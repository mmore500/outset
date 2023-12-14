import copy
import typing
import warnings

import frozendict
from matplotlib import axes as mpl_axes
from matplotlib import pyplot as plt
import opytional as opyt
import pandas as pd
import seaborn as sns

from ._auxlib.calc_aspect_ import calc_aspect
from ._auxlib.equalize_aspect_ import equalize_aspect
from ._auxlib.set_aspect_ import set_aspect
from .MarkNumericalBadges_ import MarkNumericalBadges
from .marqueeplot_ import marqueeplot


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
    _marqueeplot_outset: typing.Callable
    _marqueeplot_source: typing.Callable

    sourceplot_axes: typing.Optional[mpl_axes.Axes]
    marqueeplot_axes: typing.Sequence[mpl_axes.Axes]

    def __init__(
        self: "OutsetGrid",
        data: typing.Union[
            pd.DataFrame,
            typing.Sequence[typing.Tuple[float, float, float, float]],
        ],
        *,
        x: typing.Optional[str] = None,
        y: typing.Optional[str] = None,
        col: typing.Union[str, bool, None] = None,
        col_order: typing.Optional[typing.Sequence[str]] = None,
        col_wrap: typing.Optional[int] = None,
        hue: typing.Union[str, bool, None] = None,
        hue_order: typing.Optional[typing.Sequence[str]] = None,
        outset: typing.Optional[str] = None,
        outset_order: typing.Optional[typing.Sequence[str]] = None,
        color: typing.Optional[str] = None,  # pass to override outset hues
        include_sourceplot: bool = True,
        marqueeplot_kwargs: typing.Dict = frozendict.frozendict(),
        marqueeplot_outset_kwargs: typing.Dict = frozendict.frozendict(),
        marqueeplot_source_kwargs: typing.Dict = frozendict.frozendict(),
        palette: typing.Optional[typing.Sequence] = None,
        zorder: float = 0.0,
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
        marqueeplot_kwargs : dict, default frozendict.frozendict()
            Additional keyword arguments for marqueeplot function over outset
            plots.
        palette : Optional[Sequence], default None
            Color palette for the outset hue sequence.
        sourceplot : bool, default True
            If True, includes the source plot that outset plots are excerpted
            from as the first axis in the grid.
        sourceplot_kwargs : dict, default frozendict.frozendict()
            Additional keyword arguments for marqueeplot function over the
            source plot.
        sourceplot_{x,y}lim : Optional[Tuple[float, float]], default None
            The x and y limits for the source plot.
        **kwargs : dict
            Additional keyword arguments passed to seaborn's FacetGrid.
        """

        if col is None and col_order is not None:
            raise ValueError("col_order must be None if col not specified")
        if hue is None and hue_order is not None:
            raise ValueError("hue_order must be None if hue not specified")
        if outset is None and outset_order is not None:
            raise ValueError(
                "outset_order must be None if outset not specified"
            )

        for a in "frame_inner_pad", "frame_outer_pad":
            if a in marqueeplot_outset_kwargs or a in marqueeplot_source_kwargs:
                warnings.Warn(
                    f"Specifying {a} for only outset or source may cause "
                    "discrepancies in frame placement",
                )

        frame_inner_pad, frame_outer_pad = 0.2, 0.1

        # spoof data frame if outset frames are specified directly
        if isinstance(data, pd.DataFrame):
            if x is None or y is None:
                raise ValueError(
                    "x and y kwargs must be provided from column names in data",
                )
            if col is None:
                col = outset or hue
                if (
                    col_order is None
                    and outset is not None
                    and outset_order is not None
                ):
                    col_order = outset_order
                elif (
                    col_order is None
                    and outset is None
                    and hue is not None
                    and hue_order is not None
                ):
                    col_order = hue_order

        else:
            if x is not None or y is not None or outset is not None:
                raise ValueError(
                    "x, y, and outset must not be specified if outset frames "
                    "are specified directly",
                )
            if hue not in (None, True, False):
                raise ValueError(
                    "hue must be None or boolean if outset frames are "
                    "specified directly",
                )
            if col not in (None, True, False):
                raise ValueError(
                    "col must be None or boolean if outset frames are "
                    "specified directly",
                )

            if hue is None:
                hue = True
            if col is None:
                col = True

            x, y, outset = "x", "y", "outset"
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

        if not x in data.columns:
            raise ValueError(f"kwarg x={x} must be provided as column in data")
        if not y in data.columns:
            raise ValueError(f"kwarg x={y} must be provided as column in data")
        if outset is not None and not outset in data.columns:
            raise ValueError("if provided, outset must be a column in data")

        if col is True:
            if outset is None:
                raise ValueError("outset must be provided if col is True")
            col = outset
        elif col is False:
            col = None
        if hue is True:
            if outset is None:
                raise ValueError("outset must be provided if hue is True")
            hue = outset
        elif hue is False:
            hue = None

        if col is not None and not col in data.columns:
            raise ValueError("if provided, col must be a column in data")

        if hue is not None and not hue in data.columns:
            raise ValueError("if provided, hue must be a column in data")

        self.__data = data

        if outset is not None and outset_order is None:
            outset_order = sorted(data[outset].unique())

        if col is None:
            assert "_dummy_col" not in data.columns
            col = "_dummy_col"
            data[col] = 0

        if col_order is None:
            col_order = sorted(data[col].unique())

        if include_sourceplot:
            # SentryType entry ensures no outset data maps to sourceplot
            col_order = [_SentryType()] + col_order

        # initialize axes
        #######################################################################
        super().__init__(  # initialize parent FacetGrid
            data,
            col=col,
            col_order=col_order,
            col_wrap=col_wrap,
            hue=hue,
            hue_order=hue_order,
            palette=palette,
            **{
                "legend_out": False,
                "sharex": False,
                "sharey": False,
                **kwargs,
            },
        )

        if include_sourceplot:
            self.marqueeplot_axes = self.axes.flat[1:]
            self.sourceplot_axes = self.axes.flat[0]
        else:
            self.sourceplot_axes = None
            self.marqueeplot_axes = self.axes.flat[:]

        # draw sourceplot
        #######################################################################
        def marqueeplot_source(self_: "OutsetGrid") -> None:
            if self_.sourceplot_axes is None:
                return
            marqueeplot(
                data,
                x=x,
                y=y,
                hue=hue,
                hue_order=hue_order,
                outset=outset,
                outset_order=outset_order,
                ax=self_.sourceplot_axes,
                **{
                    "color": color,
                    "palette": palette,
                    "frame_inner_pad": frame_inner_pad,
                    "frame_outer_pad": frame_outer_pad,
                    "mark_glyph": MarkNumericalBadges,
                    "tight_axlim": False,
                    "zorder": zorder,
                    **copy.deepcopy(marqueeplot_kwargs),  # for mark_glyph
                    **marqueeplot_source_kwargs,
                    "frame_edge_kwargs": {
                        **marqueeplot_kwargs.get("frame_edge_kwargs", {}),
                        **marqueeplot_source_kwargs.get(
                            "frame_edge_kwargs", {}
                        ),
                    },
                    "frame_face_kwargs": {
                        **marqueeplot_kwargs.get("frame_face_kwargs", {}),
                        **marqueeplot_source_kwargs.get(
                            "frame_face_kwargs", {}
                        ),
                    },
                    "leader_edge_kwargs": {
                        **marqueeplot_kwargs.get("leader_edge_kwargs", {}),
                        **marqueeplot_source_kwargs.get(
                            "leader_edge_kwargs", {}
                        ),
                    },
                    "leader_face_kwargs": {
                        **marqueeplot_kwargs.get("leader_face_kwargs", {}),
                        **marqueeplot_source_kwargs.get(
                            "leader_face_kwargs", {}
                        ),
                    },
                    "mark_glyph_kwargs": {
                        "markersize": 16,
                        **marqueeplot_kwargs.get("mark_glyph_kwargs", {}),
                        **marqueeplot_source_kwargs.get(
                            "mark_glyph_kwargs", {}
                        ),
                    },
                },
            )
            self_.sourceplot_axes.set_title("")

        self._marqueeplot_source = marqueeplot_source

        # draw outplots
        #######################################################################
        def marqueeplot_outset(self_: "OutsetGrid") -> None:
            # setup
            for d in marqueeplot_kwargs, marqueeplot_outset_kwargs:
                for k, v in d.items():
                    if k == "mark_glyph" and isinstance(v, type):
                        d[k] = v()

            self_.map_dataframe_outset(
                marqueeplot,
                x=x,
                y=y,
                outset=outset,
                outset_order=outset_order,
                **{
                    "color": color,
                    "palette": palette,
                    "frame_inner_pad": frame_inner_pad,
                    "frame_outer_pad": frame_outer_pad,
                    "leader_stretch": 0.0,
                    "mark_glyph": MarkNumericalBadges(),
                    "tight_axlim": True,
                    "zorder": zorder,
                    **marqueeplot_kwargs,
                    **marqueeplot_outset_kwargs,
                    "frame_edge_kwargs": {
                        **marqueeplot_kwargs.get("frame_edge_kwargs", {}),
                        **marqueeplot_outset_kwargs.get(
                            "frame_edge_kwargs", {}
                        ),
                    },
                    "frame_face_kwargs": {
                        **marqueeplot_kwargs.get("frame_face_kwargs", {}),
                        **marqueeplot_outset_kwargs.get(
                            "frame_face_kwargs", {}
                        ),
                    },
                    "leader_edge_kwargs": {
                        **marqueeplot_kwargs.get("leader_edge_kwargs", {}),
                        **marqueeplot_outset_kwargs.get(
                            "leader_edge_kwargs", {}
                        ),
                    },
                    "leader_face_kwargs": {
                        **marqueeplot_kwargs.get("leader_face_kwargs", {}),
                        **marqueeplot_outset_kwargs.get(
                            "leader_face_kwargs", {}
                        ),
                    },
                    "mark_glyph_kwargs": {
                        **marqueeplot_kwargs.get("mark_glyph_kwargs", {}),
                        **marqueeplot_outset_kwargs.get(
                            "mark_glyph_kwargs", {}
                        ),
                    },
                },
            )

        self._marqueeplot_outset = marqueeplot_outset

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

    def marqueeplot(
        self: "OutsetGrid", equalize_aspect: bool = True
    ) -> "OutsetGrid":
        self.marqueeplot_source(equalize_aspect=False)
        self.marqueeplot_outset(equalize_aspect=False)
        if equalize_aspect:
            self.equalize_aspect()
        return self

    def marqueeplot_outset(
        self: "OutsetGrid", equalize_aspect: bool = True
    ) -> "OutsetGrid":
        self._marqueeplot_outset(self)
        self._marqueeplot_source = lambda self_: warnings.Warn(
            "redundant call to marqueeplot_outset, marquees were already drawn",
        )
        if equalize_aspect:
            self.equalize_aspect()
        return self

    def marqueeplot_source(
        self: "OutsetGrid", equalize_aspect: bool = True
    ) -> "OutsetGrid":
        self._marqueeplot_source(self)
        self._marqueeplot_source = lambda self_: warnings.Warn(
            "redundant call to marqueeplot_source, marquees were already drawn",
        )
        if equalize_aspect:
            self.equalize_aspect()
        return self

    def map(self) -> None:
        raise NotImplementedError()

    def map_outset(self) -> None:
        raise NotImplementedError()

    def map_source(self) -> None:
        raise NotImplementedError()

    def map_dataframe(self: "OutsetGrid", *args, **kwargs) -> "OutsetGrid":
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
        self.map_dataframe_outset(*args, **kwargs)
        self.map_dataframe_source(*args, **kwargs)
        return self

    def map_dataframe_outset(self, *args, **kwargs) -> "OutsetGrid":
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
        if "hue" in kwargs and self._hue_var is not None:
            raise ValueError("Cannot map `hue` if FacetGrid `hue` set.")
        elif "hue" in kwargs and kwargs.get("hue_order", None) is None:
            assert self.hue_names is None
            kwargs["hue_order"] = sorted(self.__data[kwargs["hue"]].unique())
        super().map_dataframe(*args, **kwargs)
        return self

    def map_dataframe_source(
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
        if self._hue_var is not None and "hue" in kwargs:
            raise ValueError("Cannot map `hue` if FacetGrid `hue` set.")
        if "hue_order" in kwargs and not (
            "hue" in kwargs or self._hue_var is not None
        ):
            raise ValueError("Cannot map `hue_order` if `hue` unset.")
        elif "hue_order" in kwargs and self.hue_names is None:
            raise ValueError(
                "Cannot map `hue_order` if FacetGrid `hue_order` set.",
            )

        hue = opyt.or_value(self._hue_var, kwargs.pop("hue", None))
        hue_order = opyt.or_value(self.hue_names, kwargs.pop("hue_order", None))
        if hue is not None:
            kwargs["hue"] = hue
        if hue_order is not None:
            kwargs["hue_order"] = hue_order
        if self.sourceplot_axes is not None:
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
        Does not use data stored from initialization. Data should be provided
        via argument to this method.

        Preserves axis limits for all axes except the sourceplot, if present.
        """
        self.broadcast_outset(plotter, *args, **kwargs)
        self.broadcast_source(plotter, *args, **kwargs)
        return self

    def broadcast_outset(
        self: "OutsetGrid",
        plotter: typing.Callable,
        *args,
        **kwargs,
    ) -> "OutsetGrid":
        """Map a plotting function over the sourceplot axes, if present.

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
        Does not use data stored from initialization. Data should be provided
        via argument to this method.

        Preserves axis limits.
        """
        for ax in self.marqueeplot_axes:
            # store and restore axis limits, except for sourceplot if present
            xlim, ylim = ax.get_xlim(), ax.get_ylim()
            try:
                plotter(*args, ax=ax, **kwargs)
            except (TypeError, AttributeError):
                plt.sca(ax)
                plotter(*args, **kwargs)
            ax.set_xlim(*xlim)
            ax.set_ylim(*ylim)
        return self

    def broadcast_source(
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
        Does not use data stored from initialization. Data should be provided
        via argument to this method.

        Doesn't preserve axis limits.
        """
        if self.sourceplot_axes is not None:
            ax = self.sourceplot_axes
            try:
                plotter(*args, ax=ax, **kwargs)
            except (TypeError, AttributeError):
                plt.sca(ax)
                plotter(*args, **kwargs)
        return self
