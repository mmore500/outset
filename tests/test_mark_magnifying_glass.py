import matplotlib.pyplot as plt

from outset import mark_magnifying_glass


def test_mark_magnifying_glass_single():
    plt.clf()  # Clear the current figure
    ax = plt.gca()  # Get the current axes

    # Call the function with test values
    mark_magnifying_glass(x=0.5, y=0.5, ax=ax, color="red")

    # Save and print the path of the output image
    outpath = "/tmp/test_mark_magnifying_glass_single.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
    plt.close()  # Close the plot after saving


def test_mark_magnifying_glass_multiple():
    plt.clf()
    # Multiple calls to the function with different parameters
    mark_magnifying_glass(x=0.3, y=0.3)
    mark_magnifying_glass(x=0.7, y=0.7, color="blue", color_accent="orange")

    # Save and print the path of the output image
    outpath = "/tmp/test_mark_magnifying_glass_multiple.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
    plt.close()
