import matplotlib.pyplot as plt

from outset.mark import MarkRomanBadges


def test_MarkRomanBadges_lower():
    ax = plt.gca()  # Get the current axes

    ftor = MarkRomanBadges()
    # Call the function with test values
    ftor(x=0.5, y=0.5, ax=ax, color="red")
    ftor(
        x=1.5,
        y=1.5,
        ax=ax,
        scale_numeral=0.6,
    )

    # Save and print the path of the output image
    outpath = "/tmp/test_MarkRomanBadges_lower.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_MarkRomanBadges_upper():
    ax = plt.gca()  # Get the current axes

    ftor = MarkRomanBadges(upper=True)
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
    outpath = "/tmp/test_MarkRomanBadges_upper.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_MarkRomanBadges_start():
    ax = plt.gca()  # Get the current axes

    ftor = MarkRomanBadges(start=9)
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
    outpath = "/tmp/test_MarkRomanBadges_start.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
