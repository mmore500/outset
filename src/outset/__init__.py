"""Outset Python Package"""
from __future__ import annotations

__version__ = "0.0.0"

from .draw_outset_ import draw_outset
from .mark_arrow_ import mark_arrow
from .mark_inlaid_asterisk_ import mark_inlaid_asterisk
from .mark_magnifying_glass_ import mark_magnifying_glass

__all__ = [
    "draw_outset",
    "mark_arrow",
    "mark_inlaid_asterisk",
    "mark_magnifying_glass",
]
