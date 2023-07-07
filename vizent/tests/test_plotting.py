# vizent_plot
# ==============
# add_point
# add_line

# add_glyph_legend
# add_line_legend

# create_plot
# add_glyphs
# add_lines
# return_figure

# vizent_plot

import warnings
import os
import matplotlib
from matplotlib.testing.compare import compare_images
from vizent.vizent_plot import create_plot, add_point, add_line
import matplotlib.pyplot as plt

try: 
    matplotlib.use('qtagg')
except ImportError:
    warnings.warn("The default images for this test have been created "
                    "using the qtagg backend for matplotlib. This backend is"
                    " unavailable in your current python distribution. This "
                    " test may therefore fail")


def test_create_plot():

    fig, ax1, ax2, ax3, asp = create_plot(glyphs=True, 
                                          lines=True, 
                                          show_legend=True, 
                                          show_axes=True, 
                                          use_cartopy=False, 
                                          use_image=False, 
                                          image_type=None, 
                                          image_file=None, 
                                          extent=None, 
                                          scale_x=None, 
                                          scale_y=None)
    
    # check types
    assert type(fig) == matplotlib.figure.Figure
    assert type(ax1) == matplotlib.axes.Axes
    assert type(ax2) == matplotlib.axes.Axes
    assert type(ax3) == matplotlib.axes.Axes
    assert type(asp) == float

    assert asp == 1.0

    tmp_file_create_plot = 'tmp_create_plot_test.png'
    plt.savefig(os.path.join('tests', tmp_file_create_plot))

    expected = os.path.join('tests', 'default_images', 
                            'default_plot.png')
    actual = os.path.join('tests', tmp_file_create_plot)
    
    assert compare_images(expected=expected,
                actual=actual, 
                tol=0) is None

    os.remove(os.path.join('tests', tmp_file_create_plot))


def test_add_point():

    fig = plt.Figure(figsize=(6.4,4.8)) 
    ax = fig.add_subplot(111)

    return_dict = add_point(x=0, 
                            y=0,
                            shape='sine',
                            frequency=10,
                            color='y',
                            size=200,
                            ax=ax
                            )

    ax.axis('off')

    assert type(return_dict['outer']) == matplotlib.collections.PathCollection
    assert type(return_dict['shape']) == matplotlib.collections.PathCollection
    assert type(return_dict['inner']) == matplotlib.collections.PathCollection

    tmp_file_add_point = 'tmp_sine_point.png'
    fig.savefig(os.path.join('tests', tmp_file_add_point))
    expected = os.path.join('tests', 'default_images', 'default_sine.png')
    actual = os.path.join('tests', tmp_file_add_point)

    assert compare_images(expected=expected, 
                          actual=actual, 
                          tol=0) is None

    os.remove(os.path.join('tests', tmp_file_add_point))


def test_add_line():

    fig = plt.Figure(figsize=(6.4,4.8))
    ax = fig.add_subplot(111)

    return_dict = add_line(x_origin=0,
                           y_origin=0,
                           x_end=1,
                           y_end=1,
                           frequency=10,
                           color='r',
                           width=5,
                           ax=ax,
                           style='middle',
                           freq_n=None,
                           color_n=None,
                           striped_length=None,
                           length_type=None,
                           ax_w=ax.bbox.width,
                           ax_h=ax.bbox.height,
                           zorder=1)
    
    ax.axis('off')

    print(return_dict['striped_white_lines'])
    
    assert type(return_dict['main_line']) == matplotlib.lines.Line2D
    for line in return_dict['striped_base_lines']:
        assert type(line) == matplotlib.lines.Line2D
    for line in return_dict['striped_white_lines']:
        assert type(line) == matplotlib.lines.Line2D

    tmp_file_add_line = 'tmp_line.png'
    fig.savefig(os.path.join('tests', tmp_file_add_line))
    expected = os.path.join('tests', 'default_images', 'default_line.png')
    actual = os.path.join('tests', tmp_file_add_line)

    assert compare_images(expected=expected, 
                          actual=actual, 
                          tol=0) is None

    os.remove(os.path.join('tests', tmp_file_add_line))



class TestGlyphPlot():
    pass


class TestNetworkPlot():
    pass


class TestSaveFig():
    pass


class TestVizentPlot():
    pass

