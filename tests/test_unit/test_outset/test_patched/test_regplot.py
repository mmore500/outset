import itertools as it

from matplotlib import pyplot as plt
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.datasets import load_iris
import seaborn as sns

import outset
from outset import patched as otst_patched


# adapted from https://www.datatechnotes.com/2020/11/tsne-visualization-example-in-python.html
def test_cluster_regplot():
    iris = load_iris()
    x = iris.data
    y = iris.target
    tsne = TSNE(n_components=2, verbose=1, random_state=123)
    z = tsne.fit_transform(x)

    df = pd.DataFrame()
    df["y"] = y
    df["comp-1"] = -z[:, 0]
    df["comp-2"] = z[:, 1]

    palette = sns.color_palette("hls", 6)
    og = outset.OutsetGrid(
        data=df,
        x="comp-1",
        y="comp-2",
        col="y",
        hue="y",
        col_wrap=2,
        palette=palette,
        marqueeplot_source_kws={
            "leader_stretch": 0.07,
            "mark_retract": 0.25,
        },
        zorder=4,
    )

    og.map_dataframe(
        otst_patched.regplot,
        x="comp-1",
        y="comp-2",
        palette=palette,
    )

    og.broadcast(sns.despine)
    og.marqueeplot()

    outpath = "/tmp/test_regplot.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
