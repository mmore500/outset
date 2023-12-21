import dataclasses
import typing


@dataclasses.dataclass
class SplitKwarg:
    """Wraps a kwarg value that should take on distinct values for 'source' and 'outset' axes when maping or broadcasting over an `outset.OutsetGrid`.

    Attributes
    ----------
    source : typing.Any
        The value of the argument to be used in the 'source' context.
    outEDset : typing.Any
        The value of the argument to be used in the 'outset' context.
    """

    source: typing.Any
    outset: typing.Any
