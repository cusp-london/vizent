<img align="left" width="100" height="100" src="https://github.com/cusp-london/vizent/raw/main/docs/_static/vizent_logo_thumbnail.png">

# vizent

<br/>   
 
![build](https://github.com/cusp-london/vizent/actions/workflows/unit-tests-minimal.yml/badge.svg)

> A python library for visualising bivariate data using glyphs and node-link diagrams with matplotlib

This library allows the user to create scatter plots and node-link diagrams using Visual Entropy Glyphs[1] and network edges [2]. Vizent glyphs and network edges are designed to help when you need to add an extra variable to a scatter plot, map, or graph.

Vizent glyphs are bivariate, that is they allow you to represent two variables at each point on your plot. A central colored disc is able to represent a continuous variable, an enclosing shape can represent a continuous interval or categorical variable using increasing levels of visual entropy (shape complexity). 

Vizent network edges enable additional bivariate data representation and can be used in combination with the glyphs. The edges represent data via colored edges and a visual entropy component on top of the colored edge capable of representing ordered data.

Applications for the Vizent glyphs include: 
* when you need represent uncertainty at a point or edge, eg a mean and a standard deviation
* when you need to represent derivatives at a point or edge, eg a rate and an acceleration
* any other pair of values at a point on a plot or on a network edge.

The vizent library provides an interface to matplotlib axes and figures that supports the drawing of vizent glyphs and network edges. The matplotlib artists, figures and axes objects are returned for further editing using the broader matplotlib library if required.

The library also provides functionality to plot vizent glyphs and networks edges with a map background (requires [Cartopy](https://scitools.org.uk/cartopy/docs/latest/)) or using an image provided by the user (requires [pillow](https://pillow.readthedocs.io/en/stable/)).

The [gallery](docs/_build/gallery.html) gives example plots demonstrating the library capability. A more detailed tutorial is also available [here](https://medium.com/nightingale/rising-or-falling-visualizing-the-trends-in-the-daily-covid-19-situation-e5ae3044fcef).


## Installation

vizent can be installed using [pip](https://pip.pypa.io/en/stable/)

```sh
pip install vizent
```
[vizent on PyPI](https://pypi.org/project/vizent)

Dependencies:
* matplotlib
* numpy
* scipy

Optional dependencies:
* pillow (for image backgrounds)
* cartopy (for map backgrounds)


## Using vizent

Library documentation is available at at: https://cusplondon.ac.uk/vizent

## Glyph Designs

The available glyph shape designs are shown here in full. Value increases with frequency from left (lowest) to right (highest).

### sine
![sine glyphs](https://github.com/cusp-london/vizent/raw/main/docs/_static/glyphs/sine.png "sine glyphs")
### saw
![saw glyphs](https://github.com/cusp-london/vizent/raw/main/docs/_static/glyphs/saw.png "saw glyphs")
### reverse_saw
![reverse_saw glyphs](https://github.com/cusp-london/vizent/raw/main/docs/_static/glyphs/reverse_saw.png "reverse_saw glyphs")
### square
![square glyphs](https://github.com/cusp-london/vizent/raw/main/docs/_static/glyphs/square.png "square glyphs")
### triangular
![triangular glyphs](https://github.com/cusp-london/vizent/raw/main/docs/_static/glyphs/triangular.png "triangular glyphs")
### concave
![concave glyphs](https://github.com/cusp-london/vizent/raw/main/docs/_static/glyphs/concave.png "concave glyphs")
### star
![star glyphs](https://github.com/cusp-london/vizent/raw/main/docs/_static/glyphs/star.png "star glyphs")

## Edge Designs

Default sample lines for a variety of frequency values are shown below. The left-most line is used when the data contains numpy.nan (i.e. for missing data).

![Sample lines](https://github.com/cusp-london/vizent/raw/main/docs/_static/lines_sample.png)


## Examples

### Create a basic scatterplot:

```python
from vizent import vizent_plot

x_values = [1,2,3,4,5,6,7]
y_values = [6,3,7,1,4,2,5]
color_values = [0,3,6,9,12,15,18]
shape_values= [0,1,2,3,4,5,6]
size_values = [30,60,30,45,60,30,45]

extent = [0, 9, 0, 9]

fig = vizent_plot(x_values, y_values, color_values, shape_values, size_values,
                  color_label="color", shape_label="shape", glyph_legend_title='Legend',
                  extent=extent)

fig.axes[1].set_xlabel('x')
fig.axes[1].set_ylabel('y')
```
![scatterplot image](https://github.com/cusp-london/vizent/raw/main/docs/_build/_images/gallery-basic-scatterplot_1_1.png "scatterplot image")


### Create a vizent plot with edges:

```python
import numpy as np
from vizent import vizent_plot

x_values = [0, 0, 1, 1, 0.5]
y_values = [0, 1, 0, 1, 0.5]

color_values = [-100, -10, 0.01, 100, 1000]
shape_values = [2, 1, 0, -2, -1]

edge_color_values = [-10, -5, -3, 1, 2, 4]
edge_freq_values = range(6)
color_values = [-100, -10, 0.01, 100, 1000]
shape_values = [2, 1, 0, -2, -1]

# Build a sample network based on these points
x_start = []
x_end = []
y_start = []
y_end = []
for x1,y1 in zip(x_values, y_values):
    for x2,y2 in zip(x_values, y_values):
        if x1 <= x2 and y1 <= y2:
            line_distance =  np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            if line_distance <= 1 and line_distance > 10e-5:
                x_start.append(x1)
                y_start.append(y1)
                x_end.append(x2)
                y_end.append(y2)

fig = vizent_plot(x_values=x_values,
                  y_values=y_values,
                  colour_values=color_values,
                  shape_values=shape_values,
                  size_values=[20 for i in range(len(x_values))],
                  edge_start_points=[(x,y) for x,y in zip(x_start, y_start)],
                  edge_end_points=[(x,y) for x,y in zip(x_end, y_end)],
                  edge_colors=edge_color_values,
                  edge_frequencies=edge_freq_values,
                  edge_widths=[5 for i in range(len(x_start))],
                  edge_color_n=4,
                  scale_x=15)
```
![vizent plot](https://github.com/cusp-london/vizent/raw/main/docs/_build/_images/vizent_plot_with_edges_test.png "vizent plot")


Other examples, including those using background maps for geospatial data can be found at https://cusplondon.ac.uk/vizent/gallery.

## Release History

* 1.0 First release 24/02/2021
* 1.1 Added vizent network edges 13/09/2023

## Meta

[vizent on github](https://github.com/cusp-london/vizent)

[vizent on PyPI](https://pypi.org/project/vizent)

Distributed under the MIT license. See ``LICENSE`` for more information.

Acknowledgments: The Alan Turing Institute for funding the Newcastle Seedcorn project "Automating visualization", under the EPSRC grant EP/N510129/1 and for Nick Holliman's Turing Fellowship.

[1] "Visual Entropy and the Visualization of Uncertainty", Holliman et al, arXiv:1907.12879

[2] "Visualising ordered bivariate data on node-link diagrams", O Akbulut, L McLaughlin, T Xin et al. Visual Informatics (2023) [doi:10.1016/j.visinf.2023.06.003](https://doi.org/10.1016/j.visinf.2023.06.003)