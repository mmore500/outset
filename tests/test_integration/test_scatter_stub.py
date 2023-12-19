from matplotlib import pyplot as plt
import pandas as pd
import pytest
import seaborn as sns
import outset


@pytest.mark.integration
def test_scatter_stub():
    tips = sns.load_dataset("tips")
    outlier = pd.DataFrame(
        {
            "total_bill": [
                tips["total_bill"].mean(),
                tips["total_bill"].mean() * 8,
            ],
            "tip": [101, 200],
            "sex": [tips["sex"].mode()[0]] * 2,
            "smoker": [tips["smoker"].mode()[0]] * 2,
            "day": [tips["day"].mode()[0]] * 2,
            "time": [tips["time"].mode()[0]] * 2,
            "size": [tips["size"].mode()[0]] * 2,
        },
    )

    # Append the outlier to the original dataset
    extended_tips = pd.concat([tips, outlier], ignore_index=True)

    # Create the scatter plot
    ax = sns.scatterplot(
        data=extended_tips,
        x="total_bill",
        y="tip",
        hue="size",
        size="size",
        sizes=(20, 200),
        legend="full",
    )
    sns.despine(ax=ax)

    plt.errorbar(
        extended_tips["total_bill"],
        extended_tips["tip"],
        yerr=0.2,
        fmt="none",
        ecolor="gray",
        alpha=0.5,
    )

    outset.stub.rescale_clip_outliers(ax, outset.stub.CalcBoundsIQR(5))
    ax.set_xlim(0, ax.get_xlim()[1])
    ax.set_ylim(0, ax.get_ylim()[1])

    outset.stub.stub_all_clipped_values(ax)

    outpath = "/tmp/test_scatter_stub.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
