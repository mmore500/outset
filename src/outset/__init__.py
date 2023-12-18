"""Outset Python Package"""
from __future__ import annotations

__version__ = "0.0.0"

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
from .resize_clip_outliers_ import resize_clip_outliers
from .stub_all_clipped_values_ import stub_all_clipped_values
from .stub_edge_mark_ import stub_edge_mark

__all__ = [
    "draw_marquee",
    "inset_outsets",
    "layout_corner_insets",
    "mark_arrow",
    "mark_inlaid_asterisk",
    "mark_magnifying_glass",
    "MarkAlphabeticalBadges",
    "MarkInlaidAsterisk",
    "MarkNumericalBadges",
    "MarkRomanBadges",
    "marqueeplot",
    "OutsetGrid",
    "resize_clip_outliers",
    "stub_all_clipped_values",
    "stub_edge_mark",
]
