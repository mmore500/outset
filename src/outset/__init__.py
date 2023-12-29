"""Top-level package for outset."""

__version__ = "0.1.8"

from ._draw_marquee import draw_marquee
from ._inset_outsets import inset_outsets
from ._marqueeplot import marqueeplot
from ._OutsetGrid import OutsetGrid

__all__ = [
    "draw_marquee",
    "inset_outsets",
    "marqueeplot",
    "OutsetGrid",
]
