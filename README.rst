.. figure:: docs/assets/outset-wordmark.png
   :target: https://github.com/mmore500/outset
   :alt: outset wordmark

|PyPi| |CI| |Deploy Sphinx documentation to Pages| |GitHub stars|

Easily indicate zoom plot areas in Matplotlib

- Free software: MIT license
- Documentation: https://mmore500.com/outset
- Repository: https://github.com/mmore500/outset


Features
--------

Install
-------

``python3 -m pip install outset``


Gallery
-------

   .. figure:: docs/assets/outset-gallery-collage.png
      :target: https://mmore500.com/outset/gallery.html
      :alt: outset gallery collage


*Find example code and visualizations* |gallery|_.

.. _gallery: https://mmore500.com/outset/gallery.html

.. |gallery| replace:: *here*

Basic Usage
-----------

Use ``outset.OutsetGrid`` to compose source plot with zoom panels on an axes grid. 
Zoom sections can be *a)* designated manually or *b)* inferred to bound data subsets.
To overlay zoom panels onto source plot, *c)* call ``outset.inset_outsets``.

a) Create ``OutsetGrid``, Explicit Zoom Areas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. code:: python

      from matplotlib import pyplot as plt
      import numpy as np
      import outset as otst
      import seaborn as sns
      i, a, b, c, d = np.arange(0.0, 2*np.pi, 0.01), 1, 7, 3, 11  # https://matplotlib.org/stable/gallery/

      # 3 axes grid: source plot and two zoom frames
      grid = otst.OutsetGrid([(-10, 8, -8, 12), (-5, 5, -1, 3)])  # frame coords
      grid.broadcast(plt.plot,  # run plotter over all axes
         np.sin(i*a)*np.cos(i*b) * 20, np.sin(i*c)*np.cos(i*d) * 20,  # line coords
         c="k", zorder=-1)  # kwargs forwarded to plt.plot

      grid.marqueeplot()  # set axlims and render marquee annotations

   ..

   .. figure:: docs/assets/usage1.png
      :alt: usage example 1 result

b) Create ``OutsetGrid``, Inferred Zoom Areas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. code:: python

      grid = otst.OutsetGrid(data=sns.load_dataset("iris").dropna(),  # facet data to create axes grid
         x="petal_width", y="petal_length",
         col="species",  # create zoom panel for each species
         hue="species",  # color marquee annotations by species
         aspect=0.6, height=3)  # adjust axes grid geometry
      grid.map_dataframe(sns.scatterplot,  # map plotter over faceted data
         x="petal_width", y="petal_length", legend=False, zorder=0)

      grid.marqueeplot()   # set axlims and render marquee annotations
      grid.add_legend()  # add figure-level legend

   ..

   .. figure:: docs/assets/usage2.png
      :alt: usage example 2 result


c) Overlay Zoom Panels as Insets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. code-block:: python

      grid = otst.OutsetGrid(data=sns.load_dataset("iris").dropna(),  # facet data to create axes grid
         x="petal_width", y="petal_length",
         col="species",  # put each species in its own outset
         hue="species",   # make different color marquees
         aspect=1.5, height=4)  # adjust axes grid geometry
      grid.map_dataframe(sns.scatterplot,  # map plotter over faceted data
         x="petal_width", y="petal_length", legend=False, zorder=0)

      grid.add_legend()  # add figure-level legend
      otst.inset_outsets(grid, insets="NW")  # inset outsets in upper-left corner
      grid.marqueeplot()  # set axlims and render marquee annotations

   ..

   .. figure:: docs/assets/usage3.png
      :alt: usage example 3 result

*See the* |quickstart|_ *for more detailed usage information.*

.. _quickstart: https://mmore500.com/outset/quickstart.html

.. |quickstart| replace:: *quickstart guide*


API Overview
------------

* |OutsetGrid|_: compose a source plot and zoom regions over it (e.g., "outsets") on a multiplot lattice

  * designate zoom regions directly, or as regions containing data subsets
  * object-oriented, "tidy data" interface a la ``seaborn.FacetGrid``

* |inset_outsets|_: rearrange an ``OutsetGrid`` to place outset zoom regions as insets over the original source axes

* |marqueeplot|_: axis-level "tidy data" interface to draw marquees framing specified subsets of data

* |draw_marquee|_: low-level interface to draw individual marquee annotations


.. |OutsetGrid| replace:: ``outset.OutsetGrid``
.. _OutsetGrid: https://mmore500.com/outset/_autosummary/outset.OutsetGrid.html

.. |inset_outsets| replace:: ``outset.inset_outsets``
.. _inset_outsets: https://mmore500.com/outset/_autosummary/outset.inset_outsets.html

.. |marqueeplot| replace:: ``outset.marqueeplot``
.. _marqueeplot: https://mmore500.com/outset/_autosummary/outset.marqueeplot.html

.. |draw_marquee| replace:: ``outset.draw_marquee``
.. _draw_marquee: https://mmore500.com/outset/_autosummary/outset.draw_marquee.html


*Read the full API documentation* |apidocs|_.

.. _apidocs: https://mmore500.com/outset/_autosummary/outset.html#module-outset

.. |apidocs| replace:: *here*

Available Styling Extensions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Callout mark glyphs:* customize marquee identifiers; pass as ``mark_glyph`` kwarg

   |MarkAlphabeticalBadges|_ | |MarkArrow|_ | |MarkInlaidAsterisk|_ | |MarkMagnifyingGlass|_ | |MarkRomanBadges|_

   .. image:: docs/assets/callout-mark-glyphs.png
      :alt: comparison of available glyphs

.. |MarkAlphabeticalBadges| replace:: ``outset.mark.MarkAlphabeticalBadges``
.. _MarkAlphabeticalBadges: https://mmore500.com/outset/_autosummary/outset.mark.MarkAlphabeticalBadges.html

.. |MarkArrow| replace:: ``outset.mark.MarkArrow``
.. _MarkArrow: https://mmore500.com/outset/_autosummary/outset.mark.MarkArrow.html

.. |MarkInlaidAsterisk| replace:: ``outset.mark.MarkInlaidAsterisk``
.. _MarkInlaidAsterisk: https://mmore500.com/outset/_autosummary/outset.mark.MarkInlaidAsterisk.html

.. |MarkMagnifyingGlass| replace:: ``outset.mark.MarkMagnifyingGlass``
.. _MarkMagnifyingGlass: https://mmore500.com/outset/_autosummary/outset.mark.MarkMagnifyingGlass.html

.. |MarkRomanBadges| replace:: ``outset.mark.MarkRomanBadges``
.. _MarkRomanBadges: https://mmore500.com/outset/_autosummary/outset.mark.MarkRomanBadges.html

*Callout tweaks:* customize how marquee callouts are shaped and positioned; pass as ``leader_tweak`` kwarg

   * |TweakReflect|_: flip callouts left-right/up-down 
   * |TweakSpreadArea|_: spread callout glyphs apart to resolve overlaps

.. |TweakReflect| replace:: ``outset.mark.TweakReflect``
.. _TweakReflect: https://mmore500.com/outset/_autosummary/outset.tweak.TweakReflect.html

.. |TweakSpreadArea| replace:: ``outset.mark.TweakSpreadArea``
.. _TweakSpreadArea: https://mmore500.com/outset/_autosummary/outset.tweak.TweakSpreadArea.html


Citation
--------

Contributing
------------

This project welcomes contributions and suggestions. Our documentation includes `detailed information to get you started <https://mmore500.com/outset/contributing.html#>`__.

.. |PyPi| image:: https://img.shields.io/pypi/v/outset.svg
   :target: https://pypi.python.org/pypi/outset
.. |CI| image:: https://github.com/mmore500/outset/actions/workflows/CI.yml/badge.svg
   :target: https://github.com/mmore500/outset/actions
.. |Deploy Sphinx documentation to Pages| image:: https://github.com/mmore500/outset/actions/workflows/sphinx.yml/badge.svg
   :target: https://github.com/mmore500/outset/actions/workflows/sphinx.yml
.. |GitHub stars| image:: https://img.shields.io/github/stars/mmore500/outset.svg?style=round-square&logo=github&label=Stars&logoColor=white
   :target: https://github.com/mmore500/outset
