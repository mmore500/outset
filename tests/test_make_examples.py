import matplotlib.pyplot as plt
import pytest
import seaborn as sns

import outset


@pytest.mark.integration
def test_make_example_hue_col_outset():
    og = outset.OutsetGrid(
        data=sns.load_dataset("penguins").dropna(),
        x="bill_length_mm",
        y="bill_depth_mm",
        col="island",
        hue="species",
    )
    og.map_dataframe(
        sns.scatterplot, x="bill_length_mm", y="bill_depth_mm", legend=False
    )
    og.marqueeplot()
    og.add_legend()

    outpath = "/tmp/test_make_example_hue_col_outset.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
