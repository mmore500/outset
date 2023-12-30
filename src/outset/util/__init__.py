"""Utility functions."""

from .._auxlib.calc_aspect_ import calc_aspect
from .._auxlib.set_aspect_ import set_aspect
from ._layout_corner_insets import layout_corner_insets
from ._NamedFrames import NamedFrames
from ._SplitKwarg import SplitKwarg

__all__ = [
    "calc_aspect",
    "layout_corner_insets",
    "NamedFrames",
    "set_aspect",
    "SplitKwarg",
]
