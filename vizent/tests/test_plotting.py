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
import numpy as np
import pytest

from vizent.vizent_plot import create_plot, add_point, add_line, \
    add_glyph_legend, add_line_legend, add_glyphs, add_lines, return_figure, \
    vizent_plot
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

    fig, ax1, ax2, ax3, asp = create_plot(use_glyphs=True, 
                                          use_lines=True, 
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



def test_add_glyph_legend_continuous():
    
    # Color scale
    values =  (-2, 0, 1, 3, 5)
    max_val = 10
    min_val = -10
    n_colors = 4
    scale_spread = None
    color_scale_vals = [-2, 5]
    
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

    fig, ax1, ax2, ax3, asp = create_plot(use_glyphs=True, 
                                          use_lines=False, 
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
                     scale_dp=2, 
                     label_fontsize=None)

    tmp_file_glyph_legend = os.path.join(os.path.dirname(
                                         os.path.abspath(__file__)),
                                         'tmp_glyph_legend_continuous.png')
    fig.savefig(tmp_file_glyph_legend)
    expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  'default_images', 
                                  'glyph_legend_continuous.png')
    
    assert compare_images(expected=expected, 
                          actual=tmp_file_glyph_legend, 
                          tol=12) is None

    os.remove(tmp_file_glyph_legend)




def test_add_glyph_legend_discrete():
    
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

    fig, ax1, ax2, ax3, asp = create_plot(use_glyphs=True, 
                                          use_lines=False, 
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
                     scale_dp=2, 
                     label_fontsize=None, 
                     categorical=True)

    tmp_file_glyph_legend = os.path.join(os.path.dirname(
                                         os.path.abspath(__file__)),
                                         'tmp_glyph_legend_discrete.png')
    fig.savefig(tmp_file_glyph_legend)
    expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  'default_images', 
                                  'glyph_legend_discrete.png')
    
    assert compare_images(expected=expected, 
                          actual=tmp_file_glyph_legend, 
                          tol=12) is None

    os.remove(tmp_file_glyph_legend)






def test_add_line_legend():

    fig, ax1, ax2, ax3, asp = create_plot(use_glyphs=False, 
                                          use_lines=True, 
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
                    scale_dp=3, 
                    label_fontsize=None, 
                    categorical=True)
    
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


class TestPlotWrappers:

    def setup_method(self):

        self.axes = create_plot(use_glyphs=True, 
                                use_lines=True, 
                                show_legend=True, 
                                show_axes=True, 
                                use_cartopy=False, 
                                use_image=False, 
                                image_type=None,
                                image_file=None, 
                                extent=[-0.1,1.1,-0.1,1.1], 
                                scale_x=None, 
                                scale_y=None
                                )

        self.x_values = [0, 0, 1, 1, 0.5]
        self.y_values = [0, 1, 0, 1, 0.5]


    def test_add_glyphs(self):

        color_values = [-100, -10, 0.01, 100, 1000]
        shape_values = [2, 1, 0, -2, -1]
        
        add_glyphs(ax=self.axes, 
                   x_values=self.x_values, 
                   y_values=self.y_values, 
                   color_values=color_values, 
                   shape_values=shape_values, 
                   size_values=[20 for i in range(len(self.x_values))], 
                   colormap='PuOr', 
                   scale_diverges=True,
                   shape='sine', 
                   shape_pos='sine', 
                   shape_neg='saw', 
                   color_max=200, 
                   color_min=-200, 
                   color_n=None, 
                   color_spread=None, 
                   shape_max=None, 
                   shape_min=None, 
                   shape_n=3, 
                   shape_spread=None, 
                   color_label='color', 
                   shape_label='shape', 
                   legend_title='glyphs', 
                   scale_dp=0,
                   interval_type='closest', 
                   legend_marker_size='auto', 
                   label_fontsize=7)
        

        tmp_file_glyphs = os.path.join(os.path.dirname(
                                       os.path.abspath(__file__)),
                                       'glyphs.png')
        
        self.axes[0].savefig(tmp_file_glyphs)

        expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    'default_images', 'glyphs.png')
    
        assert compare_images(expected=expected, 
                              actual=tmp_file_glyphs, 
                              tol=12) is None

        os.remove(tmp_file_glyphs)


    def test_add_lines(self):
        
        color_values = [-10, -5, -3, 1, 2, 4]
        freq_values = range(6)

        x_start = []
        x_end = []
        y_start = []
        y_end = []
        for x1,y1 in zip(self.x_values, self.y_values):
            for x2,y2 in zip(self.x_values, self.y_values):
                if x1 <= x2 and y1 <= y2:
                    line_distance =  np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                    if line_distance <= 1 and line_distance > 10e-5:
                        x_start.append(x1)
                        y_start.append(y1)
                        x_end.append(x2)
                        y_end.append(y2)


        add_lines(ax=self.axes, 
                  x_starts=x_start,
                  y_starts=y_start,
                  x_ends=x_end, 
                  y_ends=y_end, 
                  color_values=color_values,
                  freq_values=freq_values, 
                  width_values=[10 for i in range(6)], 
                  color_n=None)

        tmp_file_lines = os.path.join(os.path.dirname(
                                       os.path.abspath(__file__)),
                                       'lines.png')
        
        self.axes[0].savefig(tmp_file_lines)

        expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    'default_images', 'lines.png')
    
        assert compare_images(expected=expected, 
                              actual=tmp_file_lines, 
                              tol=12) is None

        os.remove(tmp_file_lines)


    def test_return_figure(self):
        
        tmp_file_return = os.path.join(os.path.dirname(
                                os.path.abspath(__file__)),
                                'tmp_fig_return.png')
        
        fig = return_figure(self.axes, 
                            return_type='save', 
                            file_name=tmp_file_return)
        
        expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    'default_images', 'return_fig.png')
        
        assert compare_images(expected=expected, 
                              actual=tmp_file_return, 
                              tol=12) is None
        
        os.remove(tmp_file_return)


    def test_vizent_plot_v1_0_1(self):
        color_values = [-100, -10, 0.01, 100, 1000]
        shape_values = [2, 1, 0, -2, -1]
        
        tmp_vizent_plot = os.path.join(os.path.dirname(
                                os.path.abspath(__file__)),
                                'tmp_vizent_plot.png')

        fig = vizent_plot(
                self.x_values, 
                self.y_values, 
                color_values, 
                shape_values, 
                [20 for i in range(len(self.x_values))], 
                colormap="viridis", 
                scale_x=6.4, 
                scale_y=4.8, 
                use_image=False, 
                image_type=None, 
                image_file=None, 
                use_cartopy=False, 
                extent=None, 
                scale_diverges=None, 
                shape="sine", 
                shape_pos="sine", 
                shape_neg="square", 
                colour_max=None, 
                colour_min=None, 
                colour_n=None, 
                colour_spread=None, 
                shape_max=None, 
                shape_min=None, 
                shape_n=None, 
                shape_spread=None, 
                colour_label="Color", 
                shape_label="Shape", 
                title="Glyphs", 
                x_label=None, 
                y_label=None, 
                show_axes=True,
                save=True, 
                file_name=tmp_vizent_plot, 
                return_axes=False, 
                scale_dp=1, 
                interval_type="closest", 
                show_legend=True
        )
        fig.savefig(tmp_vizent_plot)

        expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    'default_images', 'vizent_plot_test.png')
        
        assert compare_images(expected=expected, 
                              actual=tmp_vizent_plot, 
                              tol=12) is None
        
        os.remove(tmp_vizent_plot)


    def test_vizent_plot(self):
        
        edge_color_values = [-10, -5, -3, 1, 2, 4]
        edge_freq_values = range(6)
        color_values = [-100, -10, 0.01, 100, 1000]
        shape_values = [2, 1, 0, -2, -1]

        x_start = []
        x_end = []
        y_start = []
        y_end = []
        for x1,y1 in zip(self.x_values, self.y_values):
            for x2,y2 in zip(self.x_values, self.y_values):
                if x1 <= x2 and y1 <= y2:
                    line_distance =  np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                    if line_distance <= 1 and line_distance > 10e-5:
                        x_start.append(x1)
                        y_start.append(y1)
                        x_end.append(x2)
                        y_end.append(y2)

        fig = vizent_plot(x_values=self.x_values,
                    y_values=self.y_values, 
                    color_values=color_values, 
                    shape_values=shape_values,
                    size_values=[20 for i in range(len(self.x_values))],
                    edge_start_points=[(x,y) for x,y in zip(x_start, y_start)], 
                    edge_end_points=[(x,y) for x,y in zip(x_end, y_end)], 
                    edge_colors=edge_color_values,
                    edge_frequencies=edge_freq_values, 
                    edge_widths=[5 for i in range(len(x_start))],
                    edge_color_n=4, 
                    scale_x=15)
        
        tmp_vizent_plot_with_edges = os.path.join(os.path.dirname(
                                            os.path.abspath(__file__)),
                                            'tmp_vizent_plot_with_edges.png')

        fig.savefig(tmp_vizent_plot_with_edges)

        expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                'default_images', 
                                'vizent_plot_with_edges_test.png')
        
        assert compare_images(expected=expected, 
                              actual=tmp_vizent_plot_with_edges, 
                              tol=12) is None
        
        os.remove(tmp_vizent_plot_with_edges)

    

    def test_deprecation_warnings(self):

               
        edge_color_values = [-10, -5, -3, 1, 2, 4]
        edge_freq_values = range(6)
        color_values = [-100, -10, 0.01, 100, 1000]
        shape_values = [2, 1, 0, -2, -1]

        x_start = []
        x_end = []
        y_start = []
        y_end = []
        for x1,y1 in zip(self.x_values, self.y_values):
            for x2,y2 in zip(self.x_values, self.y_values):
                if x1 <= x2 and y1 <= y2:
                    line_distance =  np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                    if line_distance <= 1 and line_distance > 10e-5:
                        x_start.append(x1)
                        y_start.append(y1)
                        x_end.append(x2)
                        y_end.append(y2)

        with pytest.warns(Warning) as record:

            fig = vizent_plot(x_values=self.x_values,
                        y_values=self.y_values, 
                        color_values=color_values, 
                        shape_values=shape_values,
                        size_values=[20 for i in range(len(self.x_values))],
                        edge_start_points=[(x,y) for x,y in zip(x_start, y_start)], 
                        edge_end_points=[(x,y) for x,y in zip(x_end, y_end)], 
                        edge_colors=edge_color_values,
                        edge_frequencies=edge_freq_values, 
                        edge_widths=[5 for i in range(len(x_start))],
                        scale_x=15)
            
            if not record:
                pytest.fail("Expected a deprecation warning on the use of scale_x argument")
        