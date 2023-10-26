

.. image:: _static/vizent_image.png
  :height: 400
  :alt: An image showing a selection of vizent glyphs

================
vizent |release|
================

*A python library for visualising bivariate data using glyphs and node-link diagrams with matplotlib.*


This library allows the user to create scatter plots and node-link diagrams using Visual Entropy (*Viz-Ent*) glyphs [1]_ and network edges [2]_. Vizent glyphs and network edges are designed to help when you need to add an extra data variable to a scatter plot, map, or graph. 

Vizent glyphs are bivariate, that is they allow you to represent two variables at each point. A central colored disc is able to represent a continuous variable, an enclosing shape can represent a continuous interval or categorical variable using increasing levels of visual entropy (shape complexity). 

Vizent network edges enable additional bivariate data representation and can be used in combination with the glyphs. The edges represent data via colored edges and a visual entropy component on top of the colored edge capable of representing ordered data.

Applications for the Vizent glyphs and edges include: 

* when you need represent uncertainty at a point or edge, eg a mean and a standard deviation
* when you need to represent derivatives at a point or edge, eg a rate and an acceleration
* any other pair of values at a point on a plot or on a network edge.

The vizent library provides an interface to matplotlib axes and figures that supports the drawing of vizent glyphs and network edges. The matplotlib artists, figures and axes objects are returned for further editing using the broader matplotlib library if required.

The library also provides functionality to plot vizent glyphs and networks edges with a map background (requires `Cartopy <https://scitools.org.uk/cartopy/docs/latest/>`__) or using an image provided by the user (requires `pillow <https://pillow.readthedocs.io/en/stable/>`__).

The `gallery <gallery.html>`__ gives example plots demonstrating the library capability. A more detailed tutorial is also available `here <https://medium.com/nightingale/rising-or-falling-visualizing-the-trends-in-the-daily-covid-19-situation-e5ae3044fcef>`__.


.. toctree::
   :maxdepth: 2
   :caption: Contents: 
   :hidden:

   Home <self>
   Getting Started <getting_started>
   User Guide <user_guide>
   Gallery <gallery>
   Reference <vizent>

###############
Release History
###############

* 1.0 First release 24/02/2021
* 1.1 Added vizent network edges 26/10/2023

##########
References
##########

`vizent on github <https://github.com/cusp-london/vizent>`__

`vizent on PyPI <https://pypi.org/project/vizent>`__

Distributed under the MIT license. See ``LICENSE`` for more information.

Acknowledgments:  The Alan Turing Institute for funding the Newcastle Seedcorn project "Automating visualization", under the EPSRC grant EP/N510129/1 and for Nick Holliman's Turing Fellowship 2018-2024. For supporting Lucy McLaughlin's PhD, the  EPSRC Centre for Doctoral Training in Cloud Computing for Big Data EP/L015358/1. For Osman Akbulut's PhD support the Turkish Government. CUSP London, the Department of Informatics and the Faculty of NMES at King's College for supporting Dr Peter Baudains' time.  A Department of Informatics Impact Acceleration Award for summer 2023 funding to develop new Vizent test cases for Kabir Chhabra.

.. rubric:: Footnotes
.. [1] "Visual Entropy and the Visualization of Uncertainty", NS Holliman, A Coltekin, SJ Fernstad et al, `arXiv:1907.12879 <https://arxiv.org/abs/1907.12879>`__
.. [2] "Visualising ordered bivariate data on node-link diagrams", O Akbulut, L McLaughlin, T Xin et al. Visual Informatics (2023) `doi:10.1016/j.visinf.2023.06.003 <https://doi.org/10.1016/j.visinf.2023.06.003>`__





.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

