import matplotlib.pyplot as plt

from outset.mark._MarkNumericalBadges import MarkNumericalBadges


def test_MarkNumericalBadges():
    ax = plt.gca()  # Get the current axes

    ftor = MarkNumericalBadges()
    # Call the function with test values
    ftor(x=0.5, y=0.5, ax=ax, color="red")
    ftor(
        x=1.5,
        y=1.5,
        ax=ax,
        color="red",
        scale_numeral=0.6,
    )

    # Save and print the path of the output image
    outpath = "/tmp/test_MarkNumericalBadges.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
