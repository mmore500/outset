from matplotlib import pyplot as plt
import numpy as np

from outset._auxlib.calc_aspect_ import calc_aspect
from outset._auxlib.set_aspect_ import set_aspect


def test_set_aspect_square():
    plt.gca().set_ylim(0, 1)
    plt.gca().set_xlim(0, 1)
    set_aspect(plt.gca(), 0.5) == 1
    assert plt.gca().get_xlim() == (-0.5, 1.5)
    assert plt.gca().get_ylim() == (0, 1)

    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(1, 2)
    set_aspect(plt.gca(), 2) == 1
    assert plt.gca().get_xlim() == (0, 1)
    assert plt.gca().get_ylim() == (0.5, 2.5)


def test_set_aspect_tall():
    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 2)
    set_aspect(plt.gca(), 1)
    assert plt.gca().get_xlim() == (-0.5, 1.5)
    assert plt.gca().get_ylim() == (0, 2)

    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 2)
    set_aspect(plt.gca(), 4)
    assert plt.gca().get_xlim() == (0, 1)
    assert plt.gca().get_ylim() == (-1, 3)

    plt.gca().set_xlim(0, 1)
    plt.gca().set_ylim(0, 2)
    set_aspect(plt.gca(), 0.5)
    assert plt.gca().get_ylim() == (0, 2)
    assert plt.gca().get_xlim() == (-1.5, 2.5)


def test_set_aspect_wide():
    plt.gca().set_ylim(0, 1)
    plt.gca().set_xlim(0, 2)
    set_aspect(plt.gca(), 1)
    assert plt.gca().get_ylim() == (-0.5, 1.5)
    assert plt.gca().get_xlim() == (0, 2)

    plt.gca().set_ylim(0, 1)
    plt.gca().set_xlim(0, 2)
    set_aspect(plt.gca(), 1 / 4)
    assert plt.gca().get_ylim() == (0, 1)
    assert plt.gca().get_xlim() == (-1, 3)

    plt.gca().set_ylim(0, 1)
    plt.gca().set_xlim(0, 2)
    set_aspect(plt.gca(), 1 / 0.5)
    assert plt.gca().get_xlim() == (0, 2)
    assert plt.gca().get_ylim() == (-1.5, 2.5)


def test_set_aspect_square_physical():
    fig, ax = plt.subplots(figsize=(6, 9))
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 1)
    set_aspect(ax, 0.5, physical=True)
    assert np.isclose(calc_aspect(ax, physical=True), 0.5)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(1, 2)
    set_aspect(ax, 2, physical=True)
    assert np.isclose(calc_aspect(ax, physical=True), 2)


def test_set_aspect_tall_physical():
    fig, ax = plt.subplots(figsize=(6, 9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2)
    set_aspect(ax, 1, physical=True)
    assert np.isclose(calc_aspect(ax, physical=True), 1)

    fig, ax = plt.subplots(figsize=(3, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2)
    set_aspect(ax, 4, physical=True)
    assert np.isclose(calc_aspect(ax, physical=True), 4)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2)
    set_aspect(ax, 0.5, physical=True)
    assert np.isclose(calc_aspect(ax, physical=True), 0.5)


def test_set_aspect_wide_physical():
    fig, ax = plt.subplots(figsize=(6, 9))
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 2)
    set_aspect(ax, 1, physical=True)
    assert np.isclose(calc_aspect(ax, physical=True), 1)

    fig, ax = plt.subplots(figsize=(3, 6))
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 2)
    set_aspect(ax, 1 / 4, physical=True)
    assert np.isclose(calc_aspect(ax, physical=True), 0.25)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 2)
    set_aspect(ax, 1 / 0.5, physical=True)
    assert np.isclose(calc_aspect(ax, physical=True), 2)
