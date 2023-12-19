import matplotlib.pyplot as plt
import seaborn as sns

from outset.stub import stub_all_clipped_values


def test_stub_all_clipped_values_up():
    ax = plt.gca()  # Get the current axes=
    sns.scatterplot(x=[0.5], y=[3], ax=ax)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Call the function with test values
    stub_all_clipped_values(ax)

    # Save and print the path of the output image
    outpath = "/tmp/test_stub_all_clipped_values_up.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_stub_all_clipped_values_down():
    ax = plt.gca()  # Get the current axes=
    sns.scatterplot(x=[0.5], y=[-3], ax=ax)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Call the function with test values
    stub_all_clipped_values(ax)

    # Save and print the path of the output image
    outpath = "/tmp/test_stub_all_clipped_values_down.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_stub_all_clipped_values_left():
    ax = plt.gca()  # Get the current axes=
    sns.scatterplot(y=[0.5], x=[-3], ax=ax)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Call the function with test values
    stub_all_clipped_values(ax)

    # Save and print the path of the output image
    outpath = "/tmp/test_stub_all_clipped_values_left.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_stub_all_clipped_values_right():
    ax = plt.gca()  # Get the current axes
    sns.scatterplot(y=[0.5], x=[3], ax=ax)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Call the function with test values
    stub_all_clipped_values(ax)

    # Save and print the path of the output image
    outpath = "/tmp/test_stub_all_clipped_values_right.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_stub_all_clipped_values_upright():
    ax = plt.gca()  # Get the current axes=
    sns.scatterplot(x=[2], y=[3], ax=ax)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Call the function with test values
    stub_all_clipped_values(ax)

    # Save and print the path of the output image
    outpath = "/tmp/test_stub_all_clipped_values_upright.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")


def test_stub_all_clipped_values_with_error_bar():
    ax = plt.gca()  # Get the current axes

    # Plot a point with an error bar
    x, y = [2.5], [0.5]
    x_err, y_err = [0.01], [0.02]  # Large vertical error bar
    sns.scatterplot(x=x, y=y, ax=ax)
    plt.errorbar(x, y, xerr=x_err, yerr=y_err, fmt="o", color="blue")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Call the function with test values
    stub_all_clipped_values(ax)

    # Save and print the path of the output image
    outpath = "/tmp/test_stub_all_clipped_values_with_error_bar.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
