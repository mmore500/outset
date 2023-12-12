import matplotlib.pyplot as plt

from outset import stub_edge_mark


def test_stub_edge_mark_up():
    plt.clf()  # Clear the current figure
    ax = plt.gca()  # Get the current axes=
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Call the function with test values
    stub_edge_mark(x=0.5, y=5, ax=ax)

    # Save and print the path of the output image
    outpath = "/tmp/test_stub_edge_mark_up.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
    plt.close()  # Close the plot after saving


def test_stub_edge_mark_down():
    plt.clf()  # Clear the current figure
    ax = plt.gca()  # Get the current axes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Call the function with test values
    stub_edge_mark(x=0.5, y=-5, ax=ax)

    # Save and print the path of the output image
    outpath = "/tmp/test_stub_edge_mark_down.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
    plt.close()  # Close the plot after saving


def test_stub_edge_mark_left():
    plt.clf()  # Clear the current figure
    ax = plt.gca()  # Get the current axes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Call the function with test values
    stub_edge_mark(x=5, y=0.85, ax=ax)

    # Save and print the path of the output image
    outpath = "/tmp/test_stub_edge_mark_left.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
    plt.close()  # Close the plot after saving


def test_stub_edge_mark_right():
    plt.clf()  # Clear the current figure
    ax = plt.gca()  # Get the current axes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Call the function with test values
    stub_edge_mark(x=-5, y=0.25, ax=ax)

    # Save and print the path of the output image
    outpath = "/tmp/test_stub_edge_mark_right.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
    plt.close()  # Close the plot after saving
