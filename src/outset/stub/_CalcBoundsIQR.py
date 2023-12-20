import typing

import numpy as np


class CalcBoundsIQR:
    """Functor to set outlier bounds a fixed ratio above/below interquartile
    range.

    Bounds are calculated as (`q1` - `iqr_multiplier` * `iqr`, `q3 +
    iqr_multiplier` * `iqr`), where `q1` and `q3` are the first and third
    quartiles, respectively, and `iqr` is the interquartile range (`q3` - `q1`).
    """

    _iqr_multiplier: float

    def __init__(self: "CalcBoundsIQR", iqr_multiplier: float = 1.5) -> None:
        """Initialize functor.

        Parameters
        ----------
        iqr_multiplier : float, default 1.5
            The multiplier applied to the IQR to determine the bounds.
        """
        self._iqr_multiplier = iqr_multiplier

    def __call__(
        self: "CalcBoundsIQR", data: typing.Sequence[float]
    ) -> typing.Tuple[float, float]:
        """Calculate the lower and upper bounds of the input data using the IQR
        method.

        Parameters
        ----------
        data : np.ndarray
            The input data for which the bounds are calculated.

        Returns
        --------
        bounds : Tuple[float, float]
            Lower and upper calculated bounds.
        """
        if not any(data):
            return 0.0, 0.0
        quartile1, quartile3 = np.percentile(data, [25, 75])
        iqr = quartile3 - quartile1
        lower_bound = quartile1 - (self._iqr_multiplier * iqr)
        upper_bound = quartile3 + (self._iqr_multiplier * iqr)
        return lower_bound, upper_bound
