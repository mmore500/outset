import typing

import matplotlib.pyplot as plt
import pytest

import outset


@pytest.mark.parametrize(
    "impl", [outset.MarkInlaidAsterisk(), outset.mark_inlaid_asterisk]
)
def test_mark_inlaid_asterisk_single(impl: typing.Callable):
    ax = plt.gca()  # Get the current axes

    # Call the function with test values
    impl(x=0.5, y=0.5, ax=ax, color="red")

    # Save and print the path of the output image
    outpath = "/tmp/test_mark_inlaid_asterisk_single.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


@pytest.mark.parametrize(
    "impl", [outset.MarkInlaidAsterisk(), outset.mark_inlaid_asterisk]
)
def test_mark_inlaid_asterisk_multiple(impl: typing.Callable):
    # Multiple calls to the function with different parameters
    impl(x=0.3, y=0.3, color_accent="lavender")
    impl(x=0.7, y=0.7, color="blue", color_badge="orange")

    # Save and print the path of the output image
    outpath = "/tmp/test_mark_inlaid_asterisk_multiple.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")