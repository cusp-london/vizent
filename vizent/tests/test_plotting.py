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
import matplotlib.pyplot as plt

from vizent.vizent_plot import create_plot, add_point, add_line, \
    add_glyph_legend, add_line_legend
from vizent.scales import get_color_scale, get_shape_scale, \
    get_frequency_scale, get_color_mapping


try: 
    matplotlib.use('agg')
except ImportError:
    warnings.warn("The default images for this test have been created "
                    "using the agg backend for matplotlib. This backend is"
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

    tmp_file_create_plot = os.path.join(os.path.dirname(
                                        os.path.abspath(__file__)),
                                        'tmp_create_plot_test.png')
    
    plt.savefig(tmp_file_create_plot)

    expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  'default_images', 'default_plot.png')
    actual = tmp_file_create_plot
    
    assert compare_images(expected=expected,
                actual=actual, 
                tol=12) is None

    os.remove(tmp_file_create_plot)


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

    tmp_file_add_point =  os.path.join(os.path.dirname(
                                        os.path.abspath(__file__)),
                                       'tmp_sine_point.png')
    
    fig.savefig(tmp_file_add_point)
    expected =os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  'default_images', 'default_sine.png')
    actual = tmp_file_add_point

    assert compare_images(expected=expected, 
                          actual=actual, 
                          tol=12) is None

    os.remove(tmp_file_add_point)


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

    tmp_file_add_line = os.path.join(os.path.dirname(
                                        os.path.abspath(__file__)),
                                    'tmp_line.png')
    fig.savefig(tmp_file_add_line)
    expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  'default_images', 'default_line.png')

    assert compare_images(expected=expected, 
                          actual=tmp_file_add_line, 
                          tol=12) is None

    os.remove(tmp_file_add_line)



def test_add_glyph_legend():
    
    # Color scale
    values =  (-2, 0, 1, 3, 5)
    max_val = 10
    min_val = -10
    n_colors = 4
    scale_spread = None
    color_scale_vals = get_color_scale(values, max_val, min_val, n_colors, 
                                 scale_spread)
    
    color_mapping = get_color_mapping(color_scale_vals, 'viridis')


    # Shape scale
    values = (-7, -3, 0, 4, 5)
    max_val = None
    min_val = None
    n_shapes = 5
    scale_diverges = True
    scale_spread = None
    shape_scale_vals = get_shape_scale(values, max_val, min_val, n_shapes, 
                                 scale_diverges, scale_spread)
    
    frequency_scale = get_frequency_scale(shape_scale_vals, scale_diverges)

    fig, ax1, ax2, ax3, asp = create_plot(glyphs=True, 
                                          lines=False, 
                                          show_legend=True, 
                                          show_axes=True, 
                                          use_cartopy=False, 
                                          use_image=False, 
                                          image_type=None, 
                                          image_file=None, 
                                          extent=None, 
                                          scale_x=None, 
                                          scale_y=None)


    scale_x = fig.get_size_inches()[0]
    scale_y = fig.get_size_inches()[1]

    add_glyph_legend(ax2=ax2, 
                     color_scale=color_scale_vals, 
                     colormap='viridis', 
                     color_mapping=color_mapping,
                     shape_scale=shape_scale_vals, 
                     frequency_scale=frequency_scale, 
                     shape='sine', 
                     shape_pos='sine', 
                     shape_neg='square', 
                     divergent=True, 
                     scale_x=scale_x, 
                     scale_y=scale_y, 
                     color_label='Color', 
                     shape_label='Shape', 
                     title='Legend', 
                     size=None, 
                     scale_dp=2)

    tmp_file_glyph_legend = os.path.join(os.path.dirname(
                                         os.path.abspath(__file__)),
                                         'tmp_glyph_legend.png')
    fig.savefig(tmp_file_glyph_legend)
    expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  'default_images', 'glyph_legend.png')
    
    assert compare_images(expected=expected, 
                          actual=tmp_file_glyph_legend, 
                          tol=12) is None

    os.remove(tmp_file_glyph_legend)


def test_add_line_legend():

    fig, ax1, ax2, ax3, asp = create_plot(glyphs=False, 
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
    
    # Color scale
    values =  (-2, 0, 1, 3, 5)
    max_val = None
    min_val = None
    n_colors = 5
    scale_spread = None
    color_scale_vals = get_color_scale(values, max_val, min_val, n_colors, 
                                 scale_spread)
    
    color_mapping = get_color_mapping(color_scale_vals, 'viridis')

    # Shape scale
    values = (-7, -3, 0, 4, 5)
    max_val = 5
    min_val = -8
    n_shapes = 5
    scale_diverges = False
    scale_spread = None
    shape_scale_vals = get_shape_scale(values, max_val, min_val, n_shapes, 
                                 scale_diverges, scale_spread)
    
    frequency_scale = get_frequency_scale(shape_scale_vals, scale_diverges)

    scale_x = fig.get_size_inches()[0]
    scale_y = fig.get_size_inches()[1]

    add_line_legend(ax3=ax3, 
                    color_scale=color_scale_vals, 
                    colormap='hot', 
                    color_mapping=color_mapping, 
                    shape_scale=shape_scale_vals, 
                    frequency_scale=frequency_scale,
                    style="frequency", 
                    scale_x=scale_x, 
                    scale_y=scale_y, 
                    color_label='Color',
                    shape_label='Shape',
                    title='Legend',
                    width=None, 
                    scale_dp=3)
    
    tmp_file_line_legend = os.path.join(os.path.dirname(
                                         os.path.abspath(__file__)),
                                         'tmp_line_legend.png')
    fig.savefig(tmp_file_line_legend, dpi=300)
    
    expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  'default_images', 'line_legend.png')
    
    assert compare_images(expected=expected, 
                          actual=tmp_file_line_legend, 
                          tol=12) is None

    os.remove(tmp_file_line_legend)