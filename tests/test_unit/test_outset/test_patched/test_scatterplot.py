import seaborn as sns
from matplotlib.testing.decorators import check_figures_equal

from outset.patched import scatterplot


@check_figures_equal(extensions=["png"])
def test_scatterplot_without_hue(fig_test, fig_ref):
    """Test scatterplot without a hue parameter."""
    # Create the test figure
    ax_test = fig_test.subplots()
    scatterplot(
        data=sns.load_dataset("tips"), x="total_bill", y="tip", ax=ax_test
    )

    # Create the reference figure
    ax_ref = fig_ref.subplots()
    sns.scatterplot(
        data=sns.load_dataset("tips"), x="total_bill", y="tip", ax=ax_ref
    )


@check_figures_equal(extensions=["png"])
def test_scatterplot_with_hue(fig_test, fig_ref):
    """Test scatterplot with hue parameter."""
    # Create the test figure
    ax_test = fig_test.subplots()
    scatterplot(
        data=sns.load_dataset("tips"),
        x="total_bill",
        y="tip",
        hue="day",
        ax=ax_test,
    )

    # Create the reference figure
    ax_ref = fig_ref.subplots()
    sns.scatterplot(
        data=sns.load_dataset("tips"),
        x="total_bill",
        y="tip",
        hue="day",
        ax=ax_ref,
    )


@check_figures_equal(extensions=["png"])
def test_scatterplot_with_palette(fig_test, fig_ref):
    # Create the test figure
    ax_test = fig_test.subplots()
    scatterplot(
        data=sns.load_dataset("tips"),
        x="total_bill",
        y="tip",
        hue="time",
        palette="coolwarm",
        ax=ax_test,
    )

    # Create the reference figure
    ax_ref = fig_ref.subplots()
    sns.scatterplot(
        data=sns.load_dataset("tips"),
        x="total_bill",
        y="tip",
        hue="time",
        palette="coolwarm",
        ax=ax_ref,
    )


# Load an example dataset from seaborn
diamonds = sns.load_dataset("diamonds").dropna()


@check_figures_equal(extensions=["png"])
def test_scatterplot_hue_order_subset(fig_test, fig_ref):
    hue_order_subset = ["I1", "IF"]

    ax_test = fig_test.subplots()
    scatterplot(
        data=diamonds,
        x="price",
        y="carat",
        hue="clarity",
        hue_order=hue_order_subset,
        ax=ax_test,
    )

    ax_ref = fig_ref.subplots()
    sns.scatterplot(
        data=diamonds[diamonds["clarity"].isin(hue_order_subset)],
        x="price",
        y="carat",
        hue="clarity",
        hue_order=hue_order_subset,
        ax=ax_ref,
    )


@check_figures_equal(extensions=["png"])
def test_scatterplot_style_order_subset(fig_test, fig_ref):
    style_order_subset = ["I1", "IF"]

    ax_test = fig_test.subplots()
    scatterplot(
        data=diamonds,
        x="price",
        y="carat",
        style="clarity",
        style_order=style_order_subset,
        ax=ax_test,
    )

    ax_ref = fig_ref.subplots()
    sns.scatterplot(
        data=diamonds[diamonds["clarity"].isin(style_order_subset)],
        x="price",
        y="carat",
        style="clarity",
        style_order=style_order_subset,
        ax=ax_ref,
    )
