"""Create margin annotations for data outside axes viewport."""

from ._CalcBoundsIQR import CalcBoundsIQR
from ._rescale_clip_outliers import rescale_clip_outliers
from ._stub_all_clipped_values import stub_all_clipped_values
from ._stub_edge_mark import stub_edge_mark

__all__ = [
    "CalcBoundsIQR",
    "rescale_clip_outliers",
    "stub_all_clipped_values",
    "stub_edge_mark",
]
