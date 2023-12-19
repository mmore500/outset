"""Top-level package for outset."""

__version__ = "0.0.0"

from ._CalcBoundsIQR import CalcBoundsIQR
from ._draw_marquee import draw_marquee
from ._inset_outsets import inset_outsets
from ._layout_corner_insets import layout_corner_insets
from ._MarkArrow import mark_arrow, MarkArrow
from ._MarkInlaidAsterisk import mark_inlaid_asterisk, MarkInlaidAsterisk
from ._MarkMagnifyingGlass import mark_magnifying_glass, MarkMagnifyingGlass
from ._MarkAlphabeticalBadges import MarkAlphabeticalBadges
from ._MarkNumericalBadges import MarkNumericalBadges
from ._MarkRomanBadges import MarkRomanBadges
from ._OutsetGrid import OutsetGrid
from ._marqueeplot import marqueeplot
from ._rescale_clip_outliers import rescale_clip_outliers
from ._stub_all_clipped_values import stub_all_clipped_values
from ._stub_edge_mark import stub_edge_mark
from ._TweakReflect import TweakReflect
from ._TweakSpreadArea import TweakSpreadArea

__all__ = [
    "CalcBoundsIQR",
    "draw_marquee",
    "inset_outsets",
    "layout_corner_insets",
    "mark_arrow",
    "mark_inlaid_asterisk",
    "mark_magnifying_glass",
    "MarkAlphabeticalBadges",
    "MarkArrow",
    "MarkInlaidAsterisk",
    "MarkMagnifyingGlass",
    "MarkNumericalBadges",
    "MarkRomanBadges",
    "marqueeplot",
    "OutsetGrid",
    "rescale_clip_outliers",
    "stub_all_clipped_values",
    "stub_edge_mark",
    "TweakReflect",
    "TweakSpreadArea",
]
