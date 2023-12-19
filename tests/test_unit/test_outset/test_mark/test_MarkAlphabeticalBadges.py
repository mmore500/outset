import matplotlib.pyplot as plt

from outset import mark as otst_mark


def test_MarkAlphabeticalBadges():
    ax = plt.gca()  # Get the current axes

    ftor = otst_mark.MarkAlphabeticalBadges()
    # Call the function with test values
    ftor(x=0.5, y=0.5, ax=ax, color="red")
    ftor(
        x=1.5,
        y=1.5,
        ax=ax,
        color="red",
        scale_letter=0.6,
    )

    # Save and print the path of the output image
    outpath = "/tmp/test_MarkAlphabeticalBadges.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
