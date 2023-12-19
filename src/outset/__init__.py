"""Outset Python Package"""
from __future__ import annotations

__version__ = "0.0.0"

from .CalcBoundsIQR_ import CalcBoundsIQR
from .draw_marquee_ import draw_marquee
from .inset_outsets_ import inset_outsets
from .layout_corner_insets_ import layout_corner_insets
from .MarkArrow_ import mark_arrow, MarkArrow
from .MarkInlaidAsterisk_ import mark_inlaid_asterisk, MarkInlaidAsterisk
from .MarkMagnifyingGlass_ import mark_magnifying_glass, MarkMagnifyingGlass
from .MarkAlphabeticalBadges_ import MarkAlphabeticalBadges
from .MarkNumericalBadges_ import MarkNumericalBadges
from .MarkRomanBadges_ import MarkRomanBadges
from .OutsetGrid_ import OutsetGrid
from .marqueeplot_ import marqueeplot
from .rescale_clip_outliers_ import rescale_clip_outliers
from .stub_all_clipped_values_ import stub_all_clipped_values
from .stub_edge_mark_ import stub_edge_mark
from .TweakReflect_ import TweakReflect
from .TweakSpreadArea_ import TweakSpreadArea

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
