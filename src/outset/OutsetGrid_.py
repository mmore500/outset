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


class OutsetGrid(sns.axisgrid.FacetGrid):
    """Facilitates co-display of zoomed-in axis regions transplanted across a
    subplot grid.

    Corresponding regions in the original ("source") plot and the zoomed-in,
    "outset" regions are marked with corresponding "marquee" annotations. The
    OutsetGrid may be configured to include the source plot on the first
    subplot axis, or to only display outset regions on subplot axes.

    Marquee annotation creation must be dispatched manually through
    `marqueeplot`, `marqueeplot_outset`, and/or `marqueeplot_source`. This
    mechanism allows for end-user control over plot sequencing (i.e., layering
    order) and for adjustment of axis sizing prior to marquee rendering.
    (Marquee layout dimensions are sensitive to axis rescaling.)

    Inherits from seaborn's FacetGrid, so FacetGrad API components are
    available, see <https://seaborn.pydata.org/generated/seaborn.FacetGrid.html>.

    Attributes
    ----------
    source_axes : Optional[mpl_axes.Axes]
        The axes object for the source plot, if present.
    outset_axes : Sequence[mpl_axes.Axes]
        The axes objects for the outset plots.
    """

    __data: pd.DataFrame
    _marqueeplot_outset: typing.Callable
    _marqueeplot_source: typing.Callable

    source_axes: typing.Optional[mpl_axes.Axes]
    outset_axes: typing.Sequence[mpl_axes.Axes]

    def tight_layout(self) -> None:
        self.figure.tight_layout()

    def _finalize_grid(self, axlabels) -> None:
        """Finalize the annotations and layout."""
        self.tight_layout()

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

        The arguments `data`, `x`, `y`, `col`, `hue`, and `outset` follow
        seaborn-like tidy data API convention. Note that the same value may
        be specified for more than one of `col`, `hue, and `outset`. Marquee
        annotations are created to contain each subset of x, y values with
        identical `col`, `hue`, and `outset` values.

        Marquee frame coordinates may also be specified directly as a sequence
        of four-element tuples `(x0, x1, y0, y1)`. In this case, each frame
        will get its own hue and outset plot.

        Marquee annotation creation must be dispatched manually after
        initialization through `marqueeplot`, `marqueeplot_outset`, and/or
        `marqueeplot_source`.

        Parameters
        ----------
        data : pd.DataFrame or Sequence of Tuple[float, float, float, float]
            A DataFrame containing the data for plotting, or a sequence `(x0,
            x1, y0, y1)` specifying the bounds of outset frames.
        x : Optional[str], default None
            Column name to be used for x-axis values. Not required if data is a sequence of outset frames.
        y : Optional[str], default None
            Column name to be used for y-axis values. Not required if data is a sequence of outset frames.
        col : Union[str, bool, None], default None
            Column name for categorical variable to facet across subaxes.

            If None or True, set to match `outset` or `hue` if provided. If False, no faceting is performed.
        col_order : Optional[Sequence[str]], default None
            The order to arrange the columns in the grid.
        col_wrap : Optional[int], default None
            Number of columns where axes grid should wrap to a new row.
        hue : Union[str, bool, None], default None
            Column name for categorical variable to determine rendered color of
            data's rendered marquee annotations.

            If None or True, set to match `outset` if provided. If False, no faceting is performed.
        hue_order : Optional[Sequence[str]], default None
            The to assign palette colors to `hue` categorical values.

            May contain all or a subset of `data[hue]` values.
        outset : Optional[str], default None
            Column name for categorical variable to segregate data between marquee annotations.
        outset_order : Optional[Sequence[str]], default None
            Order for plotting the outsets.

            May contain all or a subset of `data[outset]` values.
        color : Optional[str], default None
            Color for all outset annotations. Overrides the palette.
        include_sourceplot : bool, default True
            Whether to include the original source plot in the grid.
        marqueeplot_kwargs : Dict, default frozendict()
            Additional marqueeplot keyword arguments  over all plots.
        marqueeplot_outset_kwargs : Dict, default frozendict()
            Additional marqueeplot keyword arguments specific to outset plots.
        marqueeplot_source_kwargs : Dict, default frozendict()
            Additional marqueeplot keyword specific to the source plot, if
            present.
        palette : Optional[Sequence], default None
            Color palette for the outset hue sequence.
        zorder : float, default 0.0
            The z-order for plotting elements.
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

        for a in "frame_inner_pad":
            if a in marqueeplot_outset_kwargs or a in marqueeplot_source_kwargs:
                warnings.warn(
                    f"Specifying {a} independently for only source or "
                    "outset may cause discrepancies in frame placement",
                )

        default_frame_inner_pad, default_frame_outer_pad = 0.2, 0.1

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
            default_frame_inner_pad = 0

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
            if None in data[col].unique():
                raise ValueError(
                    "Cannot include source plot if col data includes None",
                )
            col_order = [None] + col_order

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
            self.outset_axes = self.axes.flat[1:]
            self.source_axes = self.axes.flat[0]
        else:
            self.source_axes = None
            self.outset_axes = self.axes.flat[:]

        # draw sourceplot
        #######################################################################
        def marqueeplot_source(self_: "OutsetGrid") -> None:
            if self_.source_axes is None:
                return
            marqueeplot(
                data,
                x=x,
                y=y,
                hue=hue,
                hue_order=hue_order,
                outset=outset,
                outset_order=outset_order,
                ax=self_.source_axes,
                **{
                    "color": color,
                    "palette": palette,
                    "frame_inner_pad": default_frame_inner_pad,
                    "frame_outer_pad": default_frame_outer_pad,
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
            self_.source_axes.set_title("")

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
                    "frame_inner_pad": default_frame_inner_pad,
                    "frame_outer_pad": default_frame_outer_pad,
                    "leader_stretch": 0.2,
                    "leader_stretch_unit": "inchesfrom",
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
        if self.source_axes is not None:
            aspect = calc_aspect(self.source_axes)
            for ax in self.axes.flat[1:]:
                set_aspect(ax, aspect)
        else:
            equalize_aspect(self.axes.flat)
        return self

    def marqueeplot(
        self: "OutsetGrid", equalize_aspect: bool = True
    ) -> "OutsetGrid":
        """Dispatch marquee annotation rendering for all subplots --- outset as
        well as source, if included.

        Parameters
        ----------
        equalize_aspect : bool, optional, default: True
            If True, adjusts axes limits to enforce equal ylim height to xlim
            width ratio.

        Returns
        -------
        OutsetGrid
            Returns self.
        """
        self.marqueeplot_source(equalize_aspect=False)
        self.marqueeplot_outset(equalize_aspect=False)
        if equalize_aspect:
            self.equalize_aspect()
        return self

    def marqueeplot_outset(
        self: "OutsetGrid", equalize_aspect: bool = True
    ) -> "OutsetGrid":
        """Dispatch marquee annotation rendering for outset plots only

        Parameters
        ----------
        equalize_aspect : bool, optional, default: True
            If True, adjusts axes limits to enforce equal ylim height to xlim
            width ratio.

        Returns
        -------
        OutsetGrid
            Returns self.
        """
        self._marqueeplot_outset(self)
        self._marqueeplot_outset = lambda self_: warnings.warn(
            "Redundant call to marqueeplot_outset, marquees were already drawn",
        )
        if equalize_aspect:
            self.equalize_aspect()
        return self

    def marqueeplot_source(
        self: "OutsetGrid", equalize_aspect: bool = True
    ) -> "OutsetGrid":
        """Dispatch marquee annotation rendering for the source plot only, if
        included.

        Parameters
        ----------
        equalize_aspect : bool, optional, default: True
            If True, adjusts axes limits to enforce equal ylim height to xlim
            width ratio.

        Returns
        -------
        OutsetGrid
            Returns self.
        """
        self._marqueeplot_source(self)
        self._marqueeplot_source = lambda self_: warnings.warn(
            "Redundant call to marqueeplot_source, marquees were already drawn",
        )
        if equalize_aspect:
            self.equalize_aspect()
        return self

    def map(self: "OutsetGrid") -> None:
        """Placeholder, raises NotImplementedError."""
        raise NotImplementedError()

    def map_outset(self: "OutsetGrid") -> None:
        """Placeholder, raises NotImplementedError."""
        raise NotImplementedError()

    def map_source(self: "OutsetGrid") -> None:
        """Placeholder, raises NotImplementedError."""
        raise NotImplementedError()

    def map_dataframe(
        self: "OutsetGrid", plotter: typing.Callable, *args, **kwargs
    ) -> "OutsetGrid":
        """Map a plotting function over all axes, including source plot axes
        (if present).

        Uses data stored at initialization, passed as a first `data=` kwarg. To
        plot other data, use `broadcast`. Complete dataset is used for source
        axes and faceted subsets are used for each outset axes.

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
        self.map_dataframe_outset(plotter, *args, **kwargs)
        self.map_dataframe_source(plotter, *args, **kwargs)
        return self

    def map_dataframe_outset(
        self: "OutsetGrid", plotter: typing.Callable, *args, **kwargs
    ) -> "OutsetGrid":
        """Map a plotting function over outset axes only.

        Uses data stored at initialization, passed as a first `data=` kwarg and
        faceted per subplot axes. To plot other data, use `broadcast_outset`.

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
        if "hue" in kwargs and self._hue_var is not None:
            raise ValueError("Cannot map `hue` if FacetGrid `hue` is set.")
        elif "hue" in kwargs and kwargs.get("hue_order", None) is None:
            assert self.hue_names is None
            kwargs["hue_order"] = sorted(self.__data[kwargs["hue"]].unique())
        super().map_dataframe(plotter, *args, **kwargs)
        return self

    def map_dataframe_source(
        self: "OutsetGrid", plotter: typing.Callable, *args, **kwargs
    ) -> "OutsetGrid":
        """Map a plotting function over the source plot axes only.

        If source plot axes are not enabled, performs no-op.

        Uses data stored at initialization, passed as a first `data=` kwarg.
        To plot other data, use `broadcast_source`.

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
            raise ValueError("Cannot map `hue` if FacetGrid `hue` is set.")
        if "hue_order" in kwargs and not (
            "hue" in kwargs or self._hue_var is not None
        ):
            raise ValueError("Cannot map `hue_order` if `hue` is unset.")
        elif "hue_order" in kwargs and self.hue_names is None:
            raise ValueError(
                "Cannot map `hue_order` if FacetGrid `hue_order` is set.",
            )

        hue = opyt.or_value(self._hue_var, kwargs.pop("hue", None))
        hue_order = opyt.or_value(self.hue_names, kwargs.pop("hue_order", None))
        if hue is not None:
            kwargs["hue"] = hue
        if hue_order is not None:
            kwargs["hue_order"] = hue_order
        if self.source_axes is not None:
            plotter(self.__data, *args, ax=self.source_axes, **kwargs)
        self.tight_layout()
        return self

    def broadcast(
        self: "OutsetGrid",
        plotter: typing.Callable,
        *args,
        **kwargs,
    ) -> "OutsetGrid":
        """Map a plotting function over all axes, including the source plot
        axis (if present).

        Performs call with same data and arguments for all axes. To use faceted
        data stored at initialization, refer to `map_dataframe`.

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

        Preserves axis limits for all axes except the source plot, if present.
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
        """Map a plotting function over only outset axes.

        Performs call with same data and arguments for all axes. To use faceted
        data stored at initialization, refer to `map_dataframe`.

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
        for ax in self.outset_axes:
            # store and restore axis limits, except for source plot if present
            xlim, ylim = ax.get_xlim(), ax.get_ylim()
            try:
                plotter(*args, ax=ax, **kwargs)
            except (TypeError, AttributeError):
                plt.sca(ax)
                plotter(*args, **kwargs)
            ax.set_xlim(*xlim)
            ax.set_ylim(*ylim)
        self.tight_layout()
        return self

    def broadcast_source(
        self: "OutsetGrid",
        plotter: typing.Callable,
        *args,
        **kwargs,
    ) -> "OutsetGrid":
        """Map a plotting function over source plot axes, if present.

        Performs call with same data and arguments for all axes. To use faceted
        data stored at initialization, refer to `map_dataframe`.

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
        if self.source_axes is not None:
            ax = self.source_axes
            try:
                plotter(*args, ax=ax, **kwargs)
            except (TypeError, AttributeError):
                plt.sca(ax)
                plotter(*args, **kwargs)
        self.tight_layout()
        return self
