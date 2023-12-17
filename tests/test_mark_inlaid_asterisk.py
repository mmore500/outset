import matplotlib.pyplot as plt

from outset import mark_inlaid_asterisk


def test_mark_inlaid_asterisk_single():
    ax = plt.gca()  # Get the current axes

    # Call the function with test values
    mark_inlaid_asterisk(x=0.5, y=0.5, ax=ax, color="red")

    # Save and print the path of the output image
    outpath = "/tmp/test_mark_inlaid_asterisk_single.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_mark_inlaid_asterisk_multiple():
    # Multiple calls to the function with different parameters
    mark_inlaid_asterisk(x=0.3, y=0.3, color_accent="lavender")
    mark_inlaid_asterisk(x=0.7, y=0.7, color="blue", color_badge="orange")

    # Save and print the path of the output image
    outpath = "/tmp/test_mark_inlaid_asterisk_multiple.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
