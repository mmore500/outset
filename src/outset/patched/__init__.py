"""External functions patched or extended for outset compatibility."""

from ._annotateplot import annotateplot
from ._regplot import regplot
from ._scatterplot import scatterplot

__all__ = [
    "annotateplot",
    "regplot",
    "scatterplot",
]
