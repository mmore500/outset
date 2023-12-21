import random

from keras.datasets import mnist
from matplotlib import pyplot as plt
from matplotlib.patheffects import withStroke
import numpy as np
from numpy import reshape
import pandas as pd
import pytest
from sklearn.manifold import TSNE
from sklearn.datasets import load_iris
import seaborn as sns

import outset


random.seed(4)
np.random.seed(4)


# adapted from https://stackoverflow.com/a/64554001
def jitter(values):
    return values + np.random.normal(0, 5, values.shape)


# adapted from https://www.datatechnotes.com/2020/11/tsne-visualization-example-in-python.html
@pytest.mark.integration
def test_make_logo():
    (x_train, y_train), (_, _) = mnist.load_data()
    x_train = x_train[:3000]
    y_train = y_train[:3000]
    x_mnist = reshape(
        x_train, [x_train.shape[0], x_train.shape[1] * x_train.shape[2]]
    )

    tsne = TSNE(n_components=2, verbose=1, random_state=123)
    z = tsne.fit_transform(x_mnist)
    df = pd.DataFrame()
    df["y"] = y_train
    df["comp-1"] = jitter(z[:, 0])
    df["comp-2"] = jitter(z[:, 1])

    xlim = (-60, 80)
    ylim = (-60, 60)
    og = outset.OutsetGrid(
        data=[
            ((25, -3), (33, 5)),
            ((-2.5, -26), (20, -18)),
        ],
        aspect=1.2,
        marqueeplot_kws=dict(frame_edge_kws={"linewidth": 2}),
        marqueeplot_source_kws=dict(
            frame_face_kws={"alpha": 0.2},
            leader_face_kws={"alpha": 0.0, "linestyle": (0, (1, 0.5))},
            leader_stretch=0.12,
            mark_retract=0.25,
        ),
        zorder=4,
    )
    og.broadcast_source(
        sns.scatterplot,
        data=df,
        x="comp-1",
        y="comp-2",
        hue=df.y.tolist(),
        palette=sns.color_palette("hls", 10),
        alpha=0.6,
        legend=False,
        s=30,
        ax=og.source_axes,
    )
    og.marqueeplot()
    og.broadcast_outset(
        sns.scatterplot,
        data=df,
        x="comp-1",
        y="comp-2",
        hue=df.y.tolist(),
        palette=sns.color_palette("hls", 10),
        alpha=0.6,
        legend=False,
        s=60,
    )
    og.broadcast(sns.despine)

    # Add text to the plot with outline
    for color, coord, rot, txt in (
        (
            "lightblue",
            (xlim[0] + np.ptp(xlim) * 0.3, ylim[0] + np.ptp(ylim) * 0.55),
            -20,
            "outset",
        ),
        (
            "mediumaquamarine",
            (xlim[0] + np.ptp(xlim) * 0.65, ylim[0] + np.ptp(ylim) * 0.5),
            0,
            "out",
        ),
        (
            "mediumpurple",
            (xlim[0] + np.ptp(xlim) * 0.4, ylim[0] + np.ptp(ylim) * 0.3),
            0,
            "set",
        ),
    ):
        og.broadcast_outset(
            plt.text,
            *coord,
            txt,
            clip_on=True,
            fontsize=48,
            fontstyle="italic",
            color=color,
            rotation=rot,
            path_effects=[withStroke(linewidth=20, foreground="white")],
            zorder=5,
        )
        og.source_axes.text(
            *coord,
            txt,
            fontsize=8,
            fontstyle="italic",
            color=color,
            rotation=rot,
            path_effects=[withStroke(linewidth=5, foreground="white")],
            zorder=3,
        )

    # Strip Axis Text and Labels
    for ax in og.axes.flat:
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title("")

    # Adjust Spacing
    og.fig.tight_layout(w_pad=1, h_pad=1)

    outpath = "/tmp/outset_logo.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
