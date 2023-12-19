import typing

import matplotlib.pyplot as plt
import pytest

from outset import mark as otst_mark


@pytest.mark.parametrize(
    "impl", [otst_mark.MarkMagnifyingGlass(), otst_mark.mark_magnifying_glass]
)
def test_mark_magnifying_glass_single(impl: typing.Callable):
    ax = plt.gca()  # Get the current axes

    # Call the function with test values
    impl(x=0.5, y=0.5, ax=ax, color="red")

    # Save and print the path of the output image
    outpath = "/tmp/test_mark_magnifying_glass_single.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


@pytest.mark.parametrize(
    "impl", [otst_mark.MarkMagnifyingGlass(), otst_mark.mark_magnifying_glass]
)
def test_mark_magnifying_glass_multiple(impl: typing.Callable):
    # Multiple calls to the function with different parameters
    impl(x=0.3, y=0.3)
    impl(x=0.7, y=0.7, color="blue", color_accent="orange")

    # Save and print the path of the output image
    outpath = "/tmp/test_mark_magnifying_glass_multiple.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
