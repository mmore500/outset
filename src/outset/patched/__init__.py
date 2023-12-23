"""External functions patched or extended for outset compatibility."""

from ._regplot import regplot
from ._scatterplot import scatterplot

__all__ = [
    "regplot",
    "scatterplot",
]
