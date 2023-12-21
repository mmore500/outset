from collections import abc
import copy
import typing
import warnings

import frozendict
from matplotlib import axes as mpl_axes
from matplotlib import patches as mpl_patches
from matplotlib import pyplot as plt
import opytional as opyt
import pandas as pd
import seaborn as sns

from ._auxlib.calc_aspect_ import calc_aspect
from ._auxlib.equalize_aspect_ import equalize_aspect
from ._auxlib.set_aspect_ import set_aspect
from ._marqueeplot import marqueeplot, _prepad_axlim
from .mark._MarkMagnifyingGlass import MarkMagnifyingGlass
from .mark._MarkNumericalBadges import MarkNumericalBadges
from .util._NamedFrames import NamedFrames
from .util._SplitKwarg import SplitKwarg


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

    See Also
    --------
    outset.draw_marquee
        Low-level function for drawing marquee annotations.
    outset.marqueeplot
        Axes-level tidy data interface for creating marquee annotations.
    """

    __data: pd.DataFrame
    _marqueeplot_outset: typing.Callable
    _marqueeplot_source: typing.Callable

    source_axes: typing.Optional[mpl_axes.Axes]
    outset_axes: typing.Sequence[mpl_axes.Axes]

    def add_legend(self: "OutsetGrid", *args, **kwargs) -> None:
        for ax in self.axes.flat:
            ax.legend().set_visible(False)
        if not self._legend_data and self._colors and self.hue_names:
            super().add_legend(
                title=self._hue_var,
                handles=[
                    mpl_patches.Patch(color=c, label=l)
                    for c, l in zip(self._colors, self.hue_names)
                ],
                labels=self.hue_names,
            )
        else:
            super().add_legend(*args, **kwargs)

    def tight_layout(self: "OutsetGrid") -> None:
        self.figure.tight_layout()

    def _finalize_grid(
        self: "OutsetGrid", axlabels: typing.Sequence[str]
    ) -> None:
        """Finalize the annotations and layout."""
        self.tight_layout()

    def _is_inset(self: "OutsetGrid") -> bool:
        """Are outset axes inset over source axes?"""
        return (
            self.source_axes is not None
            and len(self.outset_axes)
            and self.outset_axes[0].get_position().x0
            < self.source_axes.get_position().corners()[-1][0]
        )

    def __init__(
        self: "OutsetGrid",
        data: typing.Union[
            pd.DataFrame,
            typing.Sequence[typing.Tuple[float, float, float, float]],
            NamedFrames,
        ],
        *,
        x: typing.Optional[str] = None,
        y: typing.Optional[str] = None,
        col: typing.Union[str, bool, None] = None,
        col_order: typing.Optional[typing.Sequence[str]] = None,
        col_wrap: typing.Optional[int] = None,
        hue: typing.Union[str, bool, None] = None,
        hue_order: typing.Optional[typing.Sequence[str]] = None,
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
        of four-element tuples as "extents" `(x0, y0, x1, y1)` or  "boundary
        points" `((x0, y0), (x1, y1))`. In this case, each frame will get its
        own hue and outset plot. For more elaborate manually-specified frame
        layouts, prepare a DataFrame with columns for `x`, `y`, `hue`, and `col`
        with two rows per frame (i.e., one row per boundary point) and pass
        the `frame_inner_pad=0` as a marqueeplot kwarg.

        Marquee annotation creation must be dispatched manually after
        initialization through `marqueeplot`, `marqueeplot_outset`, and/or
        `marqueeplot_source`.

        Parameters
        ----------
        data : pd.DataFrame or Sequence of Tuple[float, float, float, float] or
        outset.util.NamedFrames
            A DataFrame containing the data for plotting, or as a sequence of
            "extents" `(x0, y0, x1, y1)` or  "boundary points" `((x0, y0), (x1,
            y1))` specifying the bounds of outset frames.

            If NamedFrames, underlying data should map frame names to frame
            coordinates.
        x : Optional[str], default None
            Column name to be used for x-axis values.

            If `data` specifies outset frames directly, this kwarg is not
            required. If provided in this case, it will be used as an axis
            label.
        y : Optional[str], default None
            Column name to be used for y-axis values.

            If `data` specifies outset frames directly, this kwarg is not
            required. If provided in this case, it will be used as an axis
            label.
        col : Union[str, bool, None], default None
            Column name for categorical variable to facet across subaxes.

            If None or True, set to match `hue` if provided. If False, no faceting is performed.

            If `data` specifies outset frames directly, this kwarg is not
            required. If provided in this case, it will be used to title
            subplots label.
        col_order : Optional[Sequence[str]], default None
            The order to arrange the columns in the grid.
        col_wrap : Optional[int], default None
            Number of columns where axes grid should wrap to a new row.
        hue : Optional[str], default None
            Column name for categorical variable to determine rendered color of
            data's rendered marquee annotations.

            Will also facet across subaxes if `col` is not set `False`.

            If `data` specifies outset frames directly, this kwarg is not
            required. If provided in this case, it will be used to title legend
            created by `.add_legend()`, if any.
        hue_order : Optional[Sequence[str]], default None
            The to assign palette colors to `hue` categorical values.

            May contain all or a subset of `data[hue]` values.
        color : Optional[str], default None
            Color for all outset annotations. Overrides the palette.
        include_sourceplot : bool, default True
            Whether to include the original source plot in the grid.
        marqueeplot_kwargs : Dict, default frozendict()
            Keyword arguments to adjust marquee placement and styling over all
            plots.

            See `outset.marqueeplot` for available options.
        marqueeplot_outset_kwargs : Dict, default frozendict()
            Keyword arguments to adjust marquee placement and styling over
            outset plots.

            See `outset.marqueeplot` for available options.
        marqueeplot_source_kwargs : Dict, default frozendict()
            Keyword arguments to adjust marquee placement and styling over
            source plot, if present.

            See `outset.marqueeplot` for available options.
        palette : Optional[Sequence], default None
            Color palette for the outset hue sequence.
        zorder : float, default 0.0
            The z-order for plotting elements.
        **kwargs : dict
            Additional keyword arguments forward to seaborn's `FacetGrid`.

            See <https://seaborn.pydata.org/generated/seaborn.FacetGrid.html>
            for details.
        """

        if col is None and col_order is not None:
            raise ValueError("col_order must be None if col not specified")
        if hue is None and hue_order is not None:
            raise ValueError("hue_order must be None if hue not specified")

        for a in "frame_inner_pad":
            if a in marqueeplot_outset_kwargs or a in marqueeplot_source_kwargs:
                warnings.warn(
                    f"Specifying {a} independently for only source or "
                    "outset may cause discrepancies in frame placement",
                )

        default_frame_outer_pad_outset = 0.1
        default_frame_outer_pad_source = 0.1
        default_frame_inner_pad = 0.1

        # spoof data frame if outset frames are specified directly
        if isinstance(data, (pd.DataFrame, abc.Mapping)) and not isinstance(
            data, NamedFrames
        ):
            if x is None or y is None:
                raise ValueError(
                    "x and y kwargs must be provided from column names in data",
                )
            if col is None:
                col = hue
                if (
                    col_order is None
                    and hue is not None
                    and hue_order is not None
                ):
                    col_order = hue_order

        else:
            if col is None:
                col = True
            if hue is None and color is None:
                hue = True

            if hue and isinstance(data, NamedFrames):
                hue_order = data.keys()
            if col and isinstance(data, NamedFrames):
                col_order = data.keys()

            x, y = opyt.or_value(x, "_x"), opyt.or_value(y, "_y")
            if col is True:
                col = "outset"
            if hue is True:
                hue = col
            data = pd.DataFrame.from_records(
                [
                    {
                        x: x_,
                        y: y_,
                        col: i,
                        hue: i,
                    }
                    for i, boundary_points in (
                        data.items()
                        if isinstance(data, NamedFrames)
                        else enumerate(data, start=1)
                    )
                    for x_, y_ in (
                        boundary_points
                        if len(boundary_points) == 2
                        else (boundary_points[:2], boundary_points[2:])
                    )
                ],
            )
            default_frame_inner_pad = 0
            default_frame_outer_pad_source = 0

            if len(data) == 0:
                data = pd.DataFrame({x: [], y: [], col: [], hue: []})

        if not x in data.columns:
            raise ValueError(f"kwarg x={x} must be provided as column in data")
        if not y in data.columns:
            raise ValueError(f"kwarg x={y} must be provided as column in data")

        if col is True:
            if hue is None:
                raise ValueError("hue must be provided if col is True")
            col = hue
        elif col is False:
            col = None

        if hue is True:
            if col is None:
                raise ValueError("col must be provided if hue is True")
            hue = col
        elif hue is False:
            hue = None

        if col is not None and not col in data.columns:
            raise ValueError("if provided, col must be a column in data")

        if hue is not None and not hue in data.columns:
            raise ValueError("if provided, hue must be a column in data")

        self.__data = data

        if hue is not None and hue_order is None:
            hue_order = sorted(data[hue].unique())

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
            col_order = [None] + [*col_order]

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
                "legend_out": True,
                "sharex": False,
                "sharey": False,
                **kwargs,
            },
        )

        if "_dummy_col" in data.columns:
            self.set_titles(col_template="")

        if "_x" in data.columns:
            self.set_axis_labels(x_var="")
        else:
            self.set_axis_labels(x_var=x)

        if "_y" in data.columns:
            self.set_axis_labels(y_var="")
        else:
            self.set_axis_labels(y_var=y)

        if include_sourceplot:
            self.outset_axes = self.axes.flat[1:]
            self.source_axes = self.axes.flat[0]
        else:
            self.source_axes = None
            self.outset_axes = self.axes.flat[:]

        # draw sourceplot
        #######################################################################
        default_draw_glyph_functor_class = (
            MarkMagnifyingGlass
            if len(self.outset_axes) == 1
            else MarkNumericalBadges
        )

        def marqueeplot_source(self_: "OutsetGrid") -> None:
            if self_.source_axes is None:
                return
            marqueeplot(
                data,
                x=x,
                y=y,
                hue=hue,
                hue_order=hue_order,
                outset=col,
                outset_order=col_order,
                ax=self_.source_axes,
                **{
                    "color": color,
                    "palette": palette,
                    "frame_inner_pad": default_frame_inner_pad,
                    "frame_outer_pad": default_frame_outer_pad_source,
                    "mark_glyph": default_draw_glyph_functor_class,
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
                        "zorder": zorder + 1.01,
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

            needs_prepad = not (hue is None or hue == col)
            if needs_prepad:
                # need to prepad without split by hue
                prepad_kwargs = {
                    "frame_inner_pad": default_frame_inner_pad,
                    "frame_outer_pad": default_frame_outer_pad_outset,
                    "frame_outer_pad_unit": "axes",
                }
                fil = data[col].isin(col_order)
                if hue is not None:
                    assert hue_order is not None
                    fil &= data[hue].isin(hue_order)
                self.broadcast_outset(
                    _prepad_axlim,
                    data=data[fil],
                    x=x,
                    y=y,
                    hue=hue,
                    outset=col,
                    tight_axlim=True,
                    **{
                        **prepad_kwargs,
                        **{
                            k: v
                            for k, v in marqueeplot_kwargs.items()
                            if k in prepad_kwargs
                        },
                        **{
                            k: v
                            for k, v in marqueeplot_outset_kwargs.items()
                            if k in prepad_kwargs
                        },
                    },
                )

            self_.map_dataframe_outset(
                marqueeplot,
                x=x,
                y=y,
                **{
                    "color": color,
                    "palette": palette,
                    "frame_inner_pad": default_frame_inner_pad,
                    "frame_outer_pad": default_frame_outer_pad_outset,
                    "frame_outer_pad_unit": "axes",
                    "leader_stretch": 0.2,
                    "leader_stretch_unit": "inchesfrom",
                    "mark_glyph": default_draw_glyph_functor_class(),
                    "tight_axlim": not needs_prepad,
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
                        **({"markersize": 16} if self_._is_inset() else {}),
                        "zorder": zorder + 1.01,
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
        self: "OutsetGrid",
        equalize_aspect: bool = True,
        preserve_aspect: bool = False,
    ) -> "OutsetGrid":
        """Dispatch marquee annotation rendering for all subplots --- outset as
        well as source, if included.

        Parameters
        ----------
        equalize_aspect : bool, optional, default: True
            If True, adjusts axes limits to enforce equal ylim height to xlim
            width ratio.
        preserve_aspect : bool, optional, default: False
            If True, restore initial aspect ratio after plotting..

        Returns
        -------
        OutsetGrid
            Returns self.
        """
        self.marqueeplot_source(
            equalize_aspect=False, preserve_aspect=preserve_aspect
        )
        self.marqueeplot_outset(
            equalize_aspect=False, preserve_aspect=preserve_aspect
        )
        if equalize_aspect:
            self.equalize_aspect()
        return self

    def marqueeplot_outset(
        self: "OutsetGrid",
        *,
        equalize_aspect: bool = True,
        preserve_aspect: bool = False,
    ) -> "OutsetGrid":
        """Dispatch marquee annotation rendering for outset plots only

        Parameters
        ----------
        equalize_aspect : bool, optional, default: True
            If True, adjusts axes limits to enforce equal ylim height to xlim
            width ratio.
        preserve_aspect : bool, optional, default: False
            If True, restore initial aspect ratio after plotting..

        Returns
        -------
        OutsetGrid
            Returns self.
        """
        if preserve_aspect and equalize_aspect:
            raise ValueError(
                "may only specify one of {preserve,equalize}_aspect",
            )

        aspects = [calc_aspect(ax) for ax in self.outset_axes]
        self._marqueeplot_outset(self)
        if preserve_aspect:
            for ax, aspect in zip(self.outset_axes, aspects):
                set_aspect(ax, aspect)
        self._marqueeplot_outset = lambda self_: warnings.warn(
            "Redundant call to marqueeplot_outset, marquees were already drawn",
        )
        if equalize_aspect:
            self.equalize_aspect()
        return self

    def marqueeplot_source(
        self: "OutsetGrid",
        *,
        equalize_aspect: bool = True,
        preserve_aspect: bool = False,
    ) -> "OutsetGrid":
        """Dispatch marquee annotation rendering for the source plot only, if
        included.

        Parameters
        ----------
        equalize_aspect : bool, optional, default: True
            If True, adjusts axes limits to enforce equal ylim height to xlim
            width ratio.
        preserve_aspect : bool, optional, default: False
            If True, restore initial aspect ratio after plotting..

        Returns
        -------
        OutsetGrid
            Returns self.
        """
        if preserve_aspect and equalize_aspect:
            raise ValueError(
                "may only specify one of {preserve,equalize}_aspect",
            )

        if self.source_axes is not None:
            aspect = calc_aspect(self.source_axes)
        self._marqueeplot_source(self)
        if preserve_aspect and self.source_axes is not None:
            set_aspect(self.source_axes, aspect)
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
        self.map_dataframe_outset(
            plotter,
            *[
                arg.outset if isinstance(arg, SplitKwarg) else arg
                for arg in args
            ],
            **{
                k: v.outset if isinstance(v, SplitKwarg) else v
                for k, v in kwargs.items()
            },
        )
        self.map_dataframe_source(
            plotter,
            *[
                arg.source if isinstance(arg, SplitKwarg) else arg
                for arg in args
            ],
            **{
                k: v.source if isinstance(v, SplitKwarg) else v
                for k, v in kwargs.items()
            },
        )
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

        xlabels = [ax.get_xlabel() for ax in self.axes.flat]
        ylabels = [ax.get_ylabel() for ax in self.axes.flat]
        super().map_dataframe(plotter, *args, **kwargs)
        if kwargs.get("x", None) == self._x_var and self._x_var is not None:
            for ax, xlabel in zip(self.axes.flat, xlabels):
                ax.set_xlabel(xlabel)
        if kwargs.get("y", None) == self._y_var and self._y_var is not None:
            for ax, ylabel in zip(self.axes.flat, ylabels):
                ax.set_ylabel(ylabel)
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
            xlabel, ylabel = (
                self.source_axes.get_xlabel(),
                self.source_axes.get_ylabel(),
            )
            plotter(self.__data, *args, ax=self.source_axes, **kwargs)
            if kwargs.get("x", None) == self._x_var and self._x_var is not None:
                self.source_axes.set_xlabel(xlabel)
            if kwargs.get("y", None) == self._y_var and self._y_var is not None:
                self.source_axes.set_ylabel(ylabel)
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
        self.broadcast_outset(
            plotter,
            *[
                arg.outset if isinstance(arg, SplitKwarg) else arg
                for arg in args
            ],
            **{
                k: v.outset if isinstance(v, SplitKwarg) else v
                for k, v in kwargs.items()
            },
        )
        self.broadcast_source(
            plotter,
            *[
                arg.source if isinstance(arg, SplitKwarg) else arg
                for arg in args
            ],
            **{
                k: v.source if isinstance(v, SplitKwarg) else v
                for k, v in kwargs.items()
            },
        )
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
        xlabels = [ax.get_xlabel() for ax in self.axes.flat]
        ylabels = [ax.get_ylabel() for ax in self.axes.flat]
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
        if kwargs.get("x", None) == self._x_var and self._x_var is not None:
            for ax, xlabel in zip(self.axes.flat, xlabels):
                ax.set_xlabel(xlabel)
        if kwargs.get("y", None) == self._y_var and self._y_var is not None:
            for ax, ylabel in zip(self.axes.flat, ylabels):
                ax.set_ylabel(ylabel)
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
        if self.source_axes is None:
            return self
        xlabel, ylabel = (
            self.source_axes.get_xlabel(),
            self.source_axes.get_ylabel(),
        )
        ax = self.source_axes
        try:
            plotter(*args, ax=ax, **kwargs)
        except (TypeError, AttributeError):
            plt.sca(ax)
            plotter(*args, **kwargs)
        self.tight_layout()
        if kwargs.get("x", None) == self._x_var and self._x_var is not None:
            self.source_axes.set_xlabel(xlabel)
        if kwargs.get("y", None) == self._y_var and self._y_var is not None:
            self.source_axes.set_ylabel(ylabel)
        return self
