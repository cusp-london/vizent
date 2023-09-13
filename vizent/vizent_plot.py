from __future__ import annotations
""" 
The user accessible functions of the vizent library.
"""

import warnings
import importlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
from numpy.typing import ArrayLike
from collections.abc import Sequence
from numbers import Number

from vizent.glyph_shapes import shapes, get_shape_points
from vizent.scales import *
from vizent.legend_utils import add_colorbar, format_legend




def add_point(x, y, shape, frequency, color, size, ax):
    """
    Adds a vizent glyph to an axes object

    :param x: position on the x-axis
    :type x: float
    :param y: position on the y-axis
    :type y: float
    :param shape: glyph shape design 
    :type shape: "sine", "saw", "reverse_saw", "square", "triangular", \
    "concave", "star"
    :param frequency: value to determine frequency of glyph shape
    :type frequency: float
    :param color: glyph interior colour given in rgb values between 0 and 1
    :type color: tuple(3)
    :param size: the size of the glyph in points**2
    :type size: float
    :param ax: matplotlib Axes instance on which to plot the glyph
    :type ax: matplotlib.axes.Axes
    """
    shape_points = get_shape_points(shape, frequency)

        
    # add outer circle
    outer_collection = ax.scatter(x, y, marker='o', s=(size)**2, 
                                  facecolor="black", linewidths=0)
    # add shape
    shape_collection = ax.scatter(x, y, marker=shape_points, 
                                  s=(size * (np.abs(shape_points).max()))**2, 
                                  facecolor="white", linewidths=0)
    # add inner circle
    inner_collection = ax.scatter(x, y, marker='o', s=(size*0.6)**2, 
                                  facecolor=color, linewidths=0)
                
    # Return a dict of pathcollection objects
    return dict(outer=outer_collection, shape=shape_collection, 
                inner=inner_collection)


def add_line_frequency(x_origin, y_origin, x_end, y_end, frequency, 
                       width, ax, style, freq_n, color_n, striped_length, 
                       length_type, ax_w, ax_h, zorder):
    
    ax.apply_aspect()
    # Calculate the actual size of a unit on each axis
    y_min, y_max = ax.get_ylim()
    x_min, x_max = ax.get_xlim()
    unit_size_x = ax_w / (x_max-x_min)
    unit_size_y = ax_h / (y_max-y_min)

    # Calculate line proportions
    dy = y_end - y_origin
    dx = x_end - x_origin
    length = np.sqrt(dy**2 + dx**2)
    theta = np.arctan2(dy, dx)
    proportion = 0 
    gap = 0

    if theta < 0:
        theta = 2*np.pi + theta
    if style == "set_length":
        if length_type == "units":
            proportion = striped_length / length
            gap = ((length-striped_length) / 2) / length
        elif length_type == "pixels":
            actual_length = (np.sqrt((dy*unit_size_y)**2 
                             + (dx*unit_size_x)**2))
            proportion = striped_length / actual_length
            gap = ((actual_length-striped_length) / 2) / actual_length
        elif length_type == "proportion":
            proportion = striped_length
            gap = ((1 - proportion) / 2) 
        else:
            raise ValueError("length_type is invalid")

    # A dictionary of each striped section style, the proportion of the 
    # line taken up by the striped section, how many striped sections 
    # are present, and where on the line each striped section starts
    styles = {"middle": [1/3, 1, 1/3],
              "ends": [1/4, 2, 0, 0.75],
              "source": [1/2, 1, 0],
              "destination": [1/2, 1, 0.5],
              "set_length": [proportion, 1, gap],
              "frequency": [1/3, 1, 1/3], 
              "off": [0, 0, 0]}
    
    try:
        striped_section_length = length * styles[style][0]
    except:
        raise ValueError("line style invalid")
    


    # Plot the striped section
    if np.isnan(frequency):
        stripes = 0
    else:
        stripes = 1 + (2*frequency)

    extra = 0

    if style == "frequency":
        actual_length = (np.sqrt((dy*unit_size_y)**2 + (dx*unit_size_x)**2))
        actual_striped_section_length = actual_length * styles[style][0]

        if color_n is not None:
            n_glyphs = max(freq_n, color_n)
        else:
            n_glyphs = freq_n

        legend_marker_length = ((0.875/n_glyphs) * 0.7) * ax_h 
        actual_stripes = stripes * (actual_striped_section_length
                                    /legend_marker_length)

        stripes = actual_stripes

        # Determine any partial stripes required
        if np.floor(stripes)%2 != 0:
            extra = stripes - np.floor(stripes)
    
    striped_base_lines = []
    striped_white_lines = []
    for i in range(styles[style][1]):
        x0 = x_origin + (styles[style][2+i]*length) * np.cos(theta)
        y0 = y_origin + (styles[style][2+i]*length) * np.sin(theta)
        xn = x0 + (styles[style][0]*length) * np.cos(theta)
        yn = y0 + (styles[style][0]*length) * np.sin(theta)

        # Plot a black line for the striped section
        striped_base_lines.append(
            ax.plot([x0, xn], [y0, yn], color='black', 
                               linewidth=width, solid_capstyle='butt', 
                               zorder=zorder)[0]  
        )

        # Plot white stripes
        stripe_diff_x = np.cos(theta) * (striped_section_length/stripes)
        stripe_diff_y = np.sin(theta) * (striped_section_length/stripes)
    
        for i in range(int(stripes)):
            if i % 2 != 0:
                x_0 = x0 + stripe_diff_x * i
                y_0 = y0 + stripe_diff_y * i
                x_1 = x0 + stripe_diff_x * (i+1)
                y_1 = y0 + stripe_diff_y * (i+1) 

                striped_white_lines.append(                    
                    ax.plot([x_0, x_1], [y_0, y_1], color='white', 
                            linewidth=width, solid_capstyle='butt', 
                            zorder=zorder)[0]
                )

        if style == "frequency":
            # Extra partial stripe for frequency version
            extra_length = (striped_section_length/stripes) * extra
            extra_dx = np.cos(theta) * extra_length
            extra_dy = np.sin(theta) * extra_length

            x_0 = x0 + stripe_diff_x * np.floor(stripes)
            y_0 = y0 + stripe_diff_y * np.floor(stripes)
            x_1 = x_0 + extra_dx
            y_1 = y_0 + extra_dy

            striped_white_lines.append(
                ax.plot([x_0, x_1], [y_0, y_1], color='white', 
                        linewidth=width, solid_capstyle='butt', 
                        zorder=zorder)[0]
            )
    # Return the lists of 2DLine objects
    return dict(striped_base_lines=striped_base_lines, 
                striped_white_lines=striped_white_lines)


def add_glyph_legend(ax2, color_scale, colormap, color_mapping, shape_scale, 
                     frequency_scale, shape, shape_pos, shape_neg, divergent, 
                     scale_x, scale_y, color_label, shape_label, title, size, 
                     scale_dp, label_fontsize, categorical=False):
    
    x_positions, \
    color_y_positions, \
    shape_y_positions, \
    calculated_size,\
    color_length,\
    shape_length = format_legend(ax=ax2,
                                lhs_values=color_scale, 
                                rhs_values=frequency_scale,
                                scale_y=scale_y, 
                                title=title,  
                                lhs_heading=color_label,
                                rhs_heading=shape_label, 
                                label_fontsize=label_fontsize)

    if label_fontsize is None:
        label_len = max(len("{:.{prec}f}".format(max(color_scale),prec=scale_dp)), 
                        len("{:.{prec}f}".format(max(shape_scale),prec=scale_dp)))
        label_fontsize = (0.25 * ((scale_y/3) / (label_len*0.014)))


    if size == None:
        size = calculated_size

    # Add color legend - either colorbar or points
    if categorical==True: 
        for i in range(len(color_y_positions)):
            ax2.scatter(x_positions[0], 
                        color_y_positions[i], 
                        marker='o', 
                        s=(size) ** 2, 
                        facecolor=get_color(color_scale[i], colormap,
                                                color_mapping), 
                        linewidths=0) 
            ax2.annotate("{:.{prec}f}".format(color_scale[i],prec=scale_dp), 
                            (x_positions[0] + 1.1, color_y_positions[i]), 
                            ha='center', 
                            va='center', 
                            size=label_fontsize)
    else:
        add_colorbar(ax2, color_mapping, label_fontsize)


    # Add shape legends
    for i in range(len(shape_y_positions)):
        add_point(x_positions[1], 
                  shape_y_positions[i],
                  get_shape(shape_scale[i], shape, divergent, shape_pos, 
                            shape_neg),
                  frequency_scale[i], 
                  (0.74902, 0.74902, 0.74902), 
                  size, 
                  ax2)
        ax2.annotate("{:.{prec}f}".format(shape_scale[i],prec=scale_dp), 
                     (x_positions[1] + 1.1, shape_y_positions[i]), 
                     ha='center', 
                     va='center', 
                     size=label_fontsize)


def add_line_legend(ax3, color_scale, colormap, color_mapping, shape_scale, 
                    frequency_scale, style, scale_x, scale_y, color_label, 
                    shape_label, title, width, scale_dp, label_fontsize, 
                    categorical=False, include_nan=False):
    
    if include_nan:
        shape_scale = [np.nan] + shape_scale
        frequency_scale = [np.nan] + frequency_scale
    
    x_positions, \
    color_y_positions, \
    shape_y_positions, \
    calculated_size, \
    color_length, \
    shape_length = format_legend(ax=ax3,
                                lhs_values=color_scale, 
                                rhs_values=shape_scale,
                                scale_y=scale_y, 
                                title=title,
                                lhs_heading=color_label,
                                rhs_heading=shape_label,
                                label_fontsize=label_fontsize,
                                lines=True)
    
    if label_fontsize is None:
        label_len = max(len("{:.{prec}f}".format(max(color_scale),prec=scale_dp)), 
                        len("{:.{prec}f}".format(max(shape_scale),prec=scale_dp)))
        label_fontsize = (0.25 * ((scale_y/3) / (label_len*0.014)))

    if width == None:
        width = calculated_size
    
    if categorical == True:
        for i in range(len(color_y_positions)):

            ax3.plot([x_positions[0], x_positions[0]],
                    [color_y_positions[i] + (color_length/2), 
                    color_y_positions[i] - (color_length/2)], 
                    color=get_color(color_scale[i], colormap, color_mapping), 
                    linewidth=width, 
                    solid_capstyle='butt',
                    zorder=0)

            ax3.annotate("{:.{prec}f}".format(color_scale[i],prec=scale_dp), 
                        (x_positions[0] + 1.1, color_y_positions[i]), 
                        ha='center', 
                        va='center', 
                        size=label_fontsize)
    else:
        add_colorbar(ax3, color_mapping, label_fontsize)

    for i in range(len(shape_y_positions)):
        add_line_frequency(x_origin=x_positions[1],
                           y_origin=shape_y_positions[i] + (shape_length/2),
                           x_end=x_positions[1], 
                           y_end=shape_y_positions[i] - (shape_length/2),
                           frequency=frequency_scale[i], 
                           width=width, 
                           ax=ax3,
                           style='set_length', 
                           freq_n=None, 
                           color_n=None, 
                           striped_length=1,
                           length_type='proportion',
                           ax_w=scale_x, 
                           ax_h=scale_y, 
                           zorder=1
                           )
        
        if shape_scale[i] is not np.nan:
            ax3.annotate("{:.{prec}f}".format(shape_scale[i],prec=scale_dp), 
                        (x_positions[1] + 1.1, shape_y_positions[i]), 
                        ha='center', 
                        va='center', 
                        size=label_fontsize)
        else: 
            ax3.annotate("No data", 
                        (x_positions[1] + 1.1, shape_y_positions[i]), 
                        ha='center', 
                        va='center', 
                        size=label_fontsize)

def create_plot(use_glyphs=True, use_lines=True, show_legend=True, 
                show_axes=True, use_cartopy=False, cartopy_projection=None,
                use_image=False, image_type=None, image_file=None, extent=None, 
                scale_x=None, scale_y=None):
    """
    Create the figure used to plot glyphs and/or lines. This function
    must be executed first, and the output is used as an input to all
    other functions.

    :param use_glyphs: Set True if glyphs are to be plotted, defaults to True.
    :type use_glyphs: boolean, optional
    :param use_lines: Set True if lines are to be plotted, defaults to True.
    :type use_lines: boolean, optional
    :param show_legend: If True, show legends for glyphs/lines as included, \
        defaults to True.
    :type show_legend: boolean, optional
    :param show_axes: If True, show axis labels, defaults to True
    :type show_axes: boolean, optional
    :param use_cartopy: If True, use Cartopy to generate a map background. \
        Must specify extent if used. Defaults to False.
    :type use_cartopy: boolean, optional
    :param use_image: If True, use an image as a background. Must specify \
        extent if used. Defaults to False.
    :type use_image: boolean, optional
    :param image_type: Use either pre-packaged images or a user supplied image\
        as a background, defaults to None. :code:`newcastle` provides a \
        detailed 3D rendered image of Newcastle Upon Tyne (available for \
        limited coordinates). :code:`england` provides a map of England from \
        OpenStreetMap. :code:`filepath` can also be provided for any user \
        supplied image.
    :type image_type: str, optional
    :param extent: Axis limits or extent of coordinates for Cartopy. A list of\
         four values in the form: :code:`[xmin, xmax, ymin, ymax]`.
    :type extent: list, optional
    :param scale_x: Width of plot window in inches
    :type scale_x: int, optional
    :param scale_y: Height of plot window in inches
    :type scale_y: int, optional
    :return: tuple containing:
        :code:`fig` Matplotlib figure object which will contain the axes.\
        :code:`ax1` The matplotlib axes object for the main plot.\
        :code:`ax2` The matplotlib axes object used for the glyph legend.\
        :code:`ax3` The matplotlib axes object used for the line legend.\
        :code:`asp` The aspect ratio of the main plot area (necessary to \
        ensure the legends display correctly when using image or map\
        backgrounds).
    :rtype: (matplotlib.figure, matplotlib.axes.Axes, matplotlib.axes.Axes, \
        matplotlib.axes.Axes, float)
    """

    # input checking

    # scale values are numeric
    if not isinstance(scale_x, Number) and not scale_x==None:
        warnings.warn("scale_x must be numeric. Default will be used")
        scale_x = None
    if not isinstance(scale_y, Number) and not scale_y==None:
        warnings.warn("scale_y must be numeric. Default will be used")
        scale_y = None
    if scale_x is not None and scale_x <=0:
        warnings.warn("scale_x must be positive. Default will be used.")
        scale_x = None
    if scale_y is not None and scale_y <=0:
        warnings.warn("scale_y must be positive. Default will be used.")
        scale_y = None
    if scale_x is not None and scale_y is not None:
        if 3 * scale_x < 2 * scale_y:
            warnings.warn("scale_x is too small in comparison to scale_y. \
                          Default scaling will be used")
            scale_x = None
            scale_y = None
    # check extent format 
    if extent is not None:
        if not isinstance(extent, list) or len(extent) != 4:
            raise ValueError("extent must be a list of four values")
        for i in list(extent):
            if not isinstance(i, Number):
                raise ValueError("extent values must be numerical")

    # Set up the plot area 
    if use_cartopy or use_image:
        if use_cartopy: 
            try:
                importlib.import_module("cartopy")
                from vizent.background_map import get_basemap, \
                get_projected_aspects
            except ImportError:
                raise ImportError("Missing optional dependency cartopy")
        if use_image:
            try:
                importlib.import_module("PIL")
                from vizent.background_image import get_image, add_image_background, get_image_size
            except ImportError:
                raise ImportError("Missing optional dependency PIL")

        if extent == None:
            raise ValueError("If using a cartopy or image background, the "
                             "extent must be specified.")


    if use_image:
        if image_type == "newcastle":
            aspx = 1000
            aspy = 1000
        elif image_type == "england":
            aspx = 595
            aspy = 754
        else:
            try:
                aspx, aspy = get_image_size(image_file)
            except:
                warnings.warn("Image file not found or not valid. Figure will "
                              "be created without image background.")
                use_image = False
                if extent is not None:
                    aspx = extent[1] - extent[0]
                    aspy = extent[3] - extent[2]
                else:
                    aspx = 1
                    aspy = 1
    elif use_cartopy:
        if cartopy_projection is not None:
            aspx, aspy = get_projected_aspects(extent, cartopy_projection)
        else:
            aspx = extent[1] - extent[0]
            aspy = extent[3] - extent[2]
    else:
        if extent is not None:
            aspx = extent[1] - extent[0]
            aspy = extent[3] - extent[2]
        else:
            aspx = 1
            aspy = 1

    asp = aspy / aspx

    fig = plt.figure()
    
    # Create the layout for plot and legends
    if not use_image and not use_cartopy and extent == None:       
        if scale_x == None or scale_y == None:
            if use_glyphs and use_lines:
                if show_legend:
                    gs = gridspec.GridSpec(1, 3, width_ratios=[3, 1, 1]) 
                else:
                    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0, 0]) 
                ax2 = plt.subplot(gs[1])
                ax3 = plt.subplot(gs[2]) 
            else:
                if show_legend:
                    gs = gridspec.GridSpec(1, 3, width_ratios=[3, 1, 0])
                    if use_glyphs:
                        ax2 = plt.subplot(gs[1])
                        ax3 = plt.subplot(gs[2])
                    elif use_lines:
                        ax3 = plt.subplot(gs[1]) 
                        ax2 = plt.subplot(gs[2])
                else:
                    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0, 0])
                    ax2 = plt.subplot(gs[1])
                    ax3 = plt.subplot(gs[2]) 
        else:
            if use_glyphs and use_lines:
                if show_legend:
                    gs = gridspec.GridSpec(1, 3, 
                                           width_ratios=[scale_x-(2/3)*scale_y,
                                                         (1/3)*scale_y,
                                                         (1/3)*scale_y]) 
                else:
                    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0, 0]) 
                ax2 = plt.subplot(gs[1])
                ax3 = plt.subplot(gs[2]) 
            else:
                if show_legend:
                    gs = gridspec.GridSpec(1, 3, 
                                           width_ratios=[scale_x-(1/3)*scale_y,
                                                         (1/3)*scale_y, 0])
                    if use_glyphs:
                        ax2 = plt.subplot(gs[1])
                        ax3 = plt.subplot(gs[2])
                    elif use_lines:
                        ax3 = plt.subplot(gs[1]) 
                        ax2 = plt.subplot(gs[2])
                else:
                    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0, 0])
                    ax2 = plt.subplot(gs[1])
                    ax3 = plt.subplot(gs[2]) 
    else:
        if use_glyphs and use_lines:
            if show_legend:
                gs = gridspec.GridSpec(1, 3, width_ratios=[(3 / asp), 1, 1]) 
            else:
                gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0, 0]) 
            ax2 = plt.subplot(gs[1])
            ax3 = plt.subplot(gs[2]) 
        else:
            if show_legend:
                gs = gridspec.GridSpec(1, 3, width_ratios=[(3 / asp), 1, 0])
                if use_glyphs:
                    ax2 = plt.subplot(gs[1])
                    ax3 = plt.subplot(gs[2])
                elif use_lines:
                    ax3 = plt.subplot(gs[1]) 
                    ax2 = plt.subplot(gs[2])
            else:
                gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0, 0])
                ax2 = plt.subplot(gs[1])
                ax3 = plt.subplot(gs[2])

    if use_cartopy:
        ax1 = get_basemap(gs, extent, show_axes, projection=cartopy_projection)
    else:
        ax1 = plt.subplot(gs[0])
        if not show_axes:
            ax1.axis('off')
            fig.subplots_adjust(left=0.01, bottom=0.05, right=0.99, top=0.9, wspace=0.01)
        else:
            fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.9, wspace=0.01)
            
    if use_image:
        x_values=[np.average(extent[0:2])]
        y_values=[np.average(extent[2:4])]
        if image_type == "newcastle" or image_type == "england":
            extent = get_image(x_values, y_values, image_type, image_file)[1]
        try:
            add_image_background(get_image(x_values, y_values, image_type, 
                                           image_file)[0], ax1, extent) 
        except:
            warnings.warn("Image file not found or not valid. Figure will be "
                          "created without image background.")
            use_image = False

    # Work out scaling of plot window 
    if show_legend:
        if use_glyphs and not use_lines or use_lines and not use_glyphs: 
            fig_aspect = aspy / (aspx + (1/3)*aspy)
        elif use_glyphs and use_lines:
            fig_aspect = aspy / (aspx + (2/3)*aspy)
    else:
        fig_aspect = asp

    # Correction factor
    if asp == 1:
        f = 0.85
    elif asp > 1:
        f = 0.9
    elif asp < 1:
        f = 0.95
    if use_cartopy:
        f = 0.85

    if scale_x == None and scale_y == None:
        scale_x = 10
        scale_y = fig_aspect * scale_x * f
    elif scale_x == None:
        scale_x = (scale_y) / (fig_aspect*f)
    elif scale_y == None:
        scale_y = fig_aspect * scale_x * f
    
    fig.set_size_inches(scale_x, scale_y)

    ax2.axes.xaxis.set_visible(False)
    ax2.axes.yaxis.set_visible(False)
    ax3.axes.xaxis.set_visible(False)
    ax3.axes.yaxis.set_visible(False)

    if not show_legend:
        fig.delaxes(ax2)
        fig.delaxes(ax3)
    else:
        if use_lines and not use_glyphs:
            fig.delaxes(ax2)
        if use_glyphs and not use_lines:
            fig.delaxes(ax3)

    if not use_cartopy and not use_image and extent is not None:
        ax1.set_xlim(extent[0], extent[1])
        ax1.set_ylim(extent[2], extent[3])
        ax1.set_aspect('equal', 'box')
    elif not use_cartopy and not use_image and use_lines:
        # This ensures that the lengths of any frequency components of the 
        # lines don't vary with line orientation.
        ax1.set_aspect('equal', 'datalim')

    return fig, ax1, ax2, ax3, asp


def add_glyphs(ax, x_values, y_values, color_values, shape_values, 
               size_values, colormap="viridis", scale_diverges=None, 
               shape="sine", shape_pos="sine", shape_neg="square", 
               color_max=None, color_min=None, color_n=None, 
               color_spread=None, shape_max=None, shape_min=None, 
               shape_n=None, shape_spread=None, color_label="color", 
               shape_label="shape", legend_title="glyphs", scale_dp=2, 
               interval_type="closest", legend_marker_size="auto", 
               label_fontsize=None):
    """
    Add glyphs/nodes to the plot.

    :param ax: The tuple of matplotlib figure and axes objects returned by \
    :code:`create_plot()`.
    :type ax: tuple (matplotlib.figure, matplotlib.axes.Axes, \
    matplotlib.axes.Axes, matplotlib.axes.Axes, Numerical)
    :param x_values:  Positions of glyphs on the x-axis.
    :type x_values: float or array-like, shape (n,)
    :param y_values:  Positions of glyphs on the y-axis.
    :type y_values: float or array-like, shape (n,)
    :param color_values: The values to be represented by the color of each \
    glyph.
    :type color_values: float or array-like, shape (n,)
    :param shape_values: the list of values to be represented by the outer \
    shape of each glyph.
    :type shape_values: float or array-like, shape (n,)
    :param size_values: the list of values in points for the diameter of each \
    glyph.
    :type size_values: float or array-like, shape(n,)
    :param colormap: the matplotlib colormap to be used. The default is \
    :code:`viridis`.
    :type colormap: matplotlib.colors.Colormap or str, optional
    :param scale_diverges: If :code:`True`, diverging sets of glyphs are used \
    for positive and negative values. If not specified, your scale will diverge\
    if both positive and negative values are included for the shape variable.
    :type scale_diverges: boolean, optional
    :param shape: Glyph shape design to use for non-divergent scales. Default \
    :code:`'sine'`.
    :type shape: :code:`'sine'`, :code:`'saw'`, :code:`'reverse_saw'`, \
    :code:`'square'`, :code:`'triangular'`, :code:`'concave'`, :code:`'star'`.
    :param shape_pos: When using divergent scale, glyph shape design to use \
    for positive values. Options as for shape. Default :code:`'sine'`.
    :type shape_pos: :code:`'sine'`, :code:`'saw'`, :code:`'reverse_saw'`, \
    :code:`'square'`, :code:`'triangular'`, :code:`'concave'`, :code:`'star'`     
    :param shape_neg: When using divergent scale, glyph shape design to use for \
    negative values. Options as for shape. Default :code:`'square'`.
    :type shape_neg: :code:`'sine'`, :code:`'saw'`, :code:`'reverse_saw'`, \
    :code:`'square'`, :code:`'triangular'`, :code:`'concave'`, :code:`'star'`    
    :param color_max: The maximum color value in the legend.
    :type color_max: float, optional
    :param color_min: The minimum color value in the legend.
    :type color_min: float, optional
    :param color_n: The number of color values to show in the legend. If not \
    set, a colorbar will be used representing a continuous colour scale.
    :type color_n: int, optional
    :param color_spread: Range of color values in key. Only used if not \
    specifying both max and min.
    :type color_spread: float, optional
    :param shape_max: The maximum shape value in the legend.
    :type shape_max: float, optional
    :param shape_min: The minimum shape value in the legend.
    :type shape_min: float, optional
    :param shape_n: The number of shape values to show in the legend. 
    :type shape_n: int, optional
    :param shape_spread: Range of shape values in key. Only used if not \
    specifying both max and min. 
    :type shape_spread: float, optional
    :param color_label: The title for the color component of the legend. \
    Defaults to :code:`'color'`.
    :type color_label: str, optional
    :param shape_label: The title for the shape component of the legend. \
    Defaults to :code:`'shape'`. 
    :type shape_label: str, optional
    :param legend_title: The main title for the glyph legend. Defaults to \
    :code:`'glyphs'`.
    :type legend_title: str, optional
    :param scale_dp: The number of decimal places to round to for legend \
    values. Defaults to :code:`2`.
    :type scale_dp: int, optional
    :param interval_type: Defines how the shape of each glyph is determined \
    from its value. :code:`'closest'` uses the closest scale value, \
    :code:`limit` uses the highest scale value that the glyph value is greater\
    than or equal to (using absolute values for negative values). Defaults to \
    :code:`'closest'`.
    :type interval_type: (:code:`'closest'`, :code:`'limit'`)
    :param legend_marker_size: This controls the diameter of the legend glyph \
    markers. :code:`'auto'` means the diameter is calculated automatically to \
    fit. :code:`'mean'` uses the mean diameter/size value of the plotted glyphs.
    :type legend_marker_size: (:code:`'auto'`, :code:`'mean'`)
    :param label_fontsize: Fontsize for legend labels. If not set, this will \
    be estimated based on the lengths of the labels.
    :type label_fontsize: int, optional
    :return: List of length n, containing the artist objects that constitute\
    the plotted glyphs.
    :rtype: list of artists
    """

    # Check and sanitise inputs
    
    # check ax contains the figure
    if (not isinstance(ax, tuple) or 
        not isinstance(ax[0], matplotlib.figure.Figure)):
        raise TypeError("ax must be the object returned by create_plot()")

    # lists are all of same length
    if not (len(x_values) == len(y_values) == len(color_values) 
            == len(shape_values) == len(size_values)):
        raise ValueError("x_values, y_values, color_values, shape_values and "
                         "size_values must all be of the same length")
    if not len(x_values) > 0:
        raise ValueError("Empty input lists")
    # numerical values only where required
    if not all(isinstance(i, Number) for i in x_values):
        raise TypeError("x values must be numeric")
    if not all(isinstance(i, Number) for i in y_values):
        raise TypeError("y values must be numeric")
    if not all(isinstance(i, Number) for i in color_values):
        raise TypeError("color values must be numeric")
    if not all(isinstance(i, Number) for i in shape_values):
        raise TypeError("shape values must be numeric")
    if not all(isinstance(i, Number) for i in size_values):
        raise TypeError("size values must be numeric")
    for i in [color_min, color_max, color_spread, shape_min, shape_max, 
              shape_spread, color_n, shape_n]:
        if not isinstance(i, Number) and not i==None:
            raise TypeError("Scale minimum, maximum and spread values and "
                            "number of values per scale must be numerical")
    if not isinstance(scale_dp, int):
        raise TypeError("scale_dp must be int")

    # valid shape is specified
    if not shape in shapes:
        warnings.warn("'{0}' is not a supported shape. "
              "Default will be used".format(str(shape)))
        shape="sine"
    if not shape_pos in shapes:
        warnings.warn("'{0}' is not a supported shape. "
              "Default will be used".format(str(shape_pos)))
        shape_pos="sine"
    if not shape_neg in shapes:
        warnings.warn("'{0}' is not a supported shape. "
              "Default will be used".format(str(shape_neg)))
        shape_neg="square"

    if not legend_marker_size == "auto" and not legend_marker_size == "mean":
        warnings.warn("legend_marker_size type invalid, auto will be used")

    # Set default values
    if scale_diverges == None:
        scale_diverges = scale_is_divergent(shape_values) 
    # zero is the presumed meaningful middle-value.
    # for non-divergent ordinal scales that span zero (e.g. Farenheit)
    # scale_diverges needs setting to False.
    
    if color_n == None:
        categorical=False
    else:
        categorical=True
    
    if color_max == None:
        color_max = max(color_values)
    if color_min == None:
        color_min = min(color_values)   
    if shape_max == None:
        shape_max = max(shape_values)
    if shape_min == None:
        shape_min = min(shape_values) 
    if color_spread == None:
        color_spread = color_max - color_min
    if shape_spread == None:
        shape_spread = shape_max - shape_min

    # Apply a ravel in the event dataframe columns (for example) are passed
    x_values = np.ravel(x_values)
    y_values = np.ravel(y_values)
    shape_values = np.ravel(shape_values)
    color_values = np.ravel(color_values)
    size_values = np.ravel(size_values)

    # plot the points
    color_scale = get_color_scale(color_values, color_max, color_min, 
                                    color_n, color_spread)
    color_mapping = get_color_mapping(color_scale, colormap)
    shape_scale = get_shape_scale(shape_values, shape_max, shape_min, shape_n, 
                                  scale_diverges, shape_spread) 
    frequency_scale = get_frequency_scale(shape_scale, scale_diverges)

    
    artists = []
    for i in range(len(x_values)):
        artists.append(
            add_point(x_values[i], 
                      y_values[i], 
                      get_shape(shape_values[i], shape, scale_diverges, 
                                shape_pos, shape_neg),
                      get_frequency(shape_values[i], shape_scale, 
                                    frequency_scale, interval_type),
                      get_color(color_values[i], colormap, color_mapping),
                      size_values[i], 
                      ax[1])
        )

    # Add the legend
    scale_x = ax[0].get_size_inches()[0]
    scale_y = ax[0].get_size_inches()[1]
    
    if legend_marker_size == "mean":
        size = np.mean(size_values)
    else:
        size = None
    
    add_glyph_legend(ax[2], color_scale, colormap, color_mapping, 
                     shape_scale, frequency_scale, shape, shape_pos, shape_neg, 
                     scale_diverges, scale_x, scale_y, color_label, 
                     shape_label, legend_title, size, scale_dp, label_fontsize,
                     categorical)

    return artists


def add_lines(ax, x_starts, y_starts, x_ends, y_ends, color_values,
              freq_values, width_values, striped_length=1, length_type="units", 
              colormap="viridis", style="middle", color_max=None, 
              color_min=None, color_n=None, color_spread=None, freq_max=None, 
              freq_min=None, freq_n=None, freq_spread=None, color_label="color", 
              frequency_label="frequency", legend_title="lines", scale_dp=2, 
              interval_type="closest", legend_marker_size="auto", zorder=0.5, 
              label_fontsize=None):
    """
    Add lines/edges to the plot.

    :param ax: The tuple of matplotlib figure and axes objects returned by \
    :code:`create_plot()`.
    :type ax: tuple (matplotlib.figure, matplotlib.axes.Axes, \
    matplotlib.axes.Axes, matplotlib.axes.Axes, Numerical)
    :param x_starts: The x coordinates of the origin points of each line
    :type x_starts: float or array-like, shape (n,)
    :param y_starts: The y coordinates of the origin points of each line
    :type y_starts: float or array-like, shape (n,)
    :param x_ends: The x coordinates of the end points of each line
    :type x_ends: float or array-like, shape (n,)
    :param y_ends: The y coordinates of the end points of each line
    :type y_ends: float or array-like, shape (n,)
    :param color_values: The values to be represented by the color of each \
    line.
    :type color_values: float or array-like, shape (n,)
    :param freq_values: The list of values to be represented by the central \
    stripe frequency.
    :type freq_values: float or array-like, shape (n,)
    :param width_values: The list of values in points for the width of each \
    line.
    :type width_values: float or array-like, shape(n,)    
    :param striped_length: if using the style :code:`'set_length'`, the length\
    of the central stripe. Units determined by :code:`length_type`. \
    Defaults to :code:`1`.
    :type striped_length: float, optional
    :param length_type: The units to be used for stripe length. \
    :code:`'units'` uses axes units, :code:`'pixels'` uses the number of \
    pixels and :code:`'proportion'` uses the proportion of the line.
    :type length_type: (:code:`'units'`, :code:`'pixels'`, \
    :code:`'proportion'`), optional
    :param colormap: the matplotlib colormap to be used. Defaults to \
    :code:`viridis`.
    :type colormap: matplotlib.colors.Colormap or str, optional
    :param style: The length and positioning style of the striped area. \
    :code:`'middle'` generates a striped area centred on the line/edge where \
    with length of striped area 1/3 of edge length. :code:`'ends'` \
    generates a striped area at each end of the line/edge with length of \
    striped area 1/4 of total edge length. :code:`'source'` \
    generates a striped area at the source of the line, 1/2 of the total edge \
    length. :code:`'destination'` generates a striped area at the line \
    destination, where the striped area is 1/2 of the total edge length. \
    :code:`'set_length'` generates a striped area at the centre of the line, \
    with the length specified by user via the :code:`striped_length` parameter,\
    :code:`'frequency'` generates a striped area at the centre of the line, \
    1/3 edge length. Instead of a set number of stripes, this uses the number \
    of stripes per unit length, matched to the legend. :code:`'off'` turns off\
     the striped area. Defaults to :code:`'middle'`.
    :type style: (:code:`'middle'`, :code:`'ends'`, :code:`'source'`, \
    :code:`'destination'`, :code:`'set_length'`, :code:`'frequency'`, \
    :code:`'off'`), optional.   
    :param color_max: The maximum color value in the legend.
    :type color_max: float, optional
    :param color_min: The minimum color value in the legend.
    :type color_min: float, optional
    :param color_n: The number of color values to show in the legend.
    :type color_n: int, optional
    :param color_spread: Range of color values in key. Only used if not \
    specifying both max and min.
    :type color_spread: float, optional    
    :param freq_max: The maximum frequency value in the legend.
    :type freq_max: float, optional
    :param freq_min: The minimum frequency value in the legend.
    :type freq_min: float, optional
    :param freq_n: The number of frequency values to show in the legend. 
    :type freq_n: int, optional
    :param freq_spread: Range of frequency values in key. Only used if not \
    specifying both max and min. 
    :type freq_spread: float, optional
    :param color_label: The title for the color component of the legend. \
    Defaults to :code:`'color'`.
    :type color_label: str, optional
    :param freq_label: The title for the frequency component of the legend. \
    Defaults to :code:`'frequency'`. 
    :type frequency_label: str, optional
    :param legend_title: The main title for the glyph legend. Defaults to \
    :code:`'lines'`.
    :type legend_title: str, optional
    :param scale_dp: The number of decimal places to round to for legend \
    values. Defaults to :code:`2`.
    :type scale_dp: int, optional
    :param interval_type: Defines how the frequency of each line is determined \
    from its value. :code:`'closest'` uses the closest scale value, \
    :code:`limit` uses the highest scale value that the frequency value is greater\
    than or equal to (using absolute values for negative values). Defaults to \
    :code:`'closest'`.
    :type interval_type: (:code:`'closest'`, :code:`'limit'`)
    :param legend_marker_size: This controls the width of the legend line \
    markers. :code:`'auto'` means the width is calculated automatically to \
    fit. :code:`'mean'` uses the mean width value of the plotted lines.
    :type legend_marker_size: (:code:`'auto'`, :code:`'mean'`)
    :return: List of length n, containing the artist objects that constitute\
    the plotted lines.
    :rtype: list of artists
    """

    # Check and sanitise inputs

    # check ax contains the figure
    if (not isinstance(ax, tuple) or 
        not isinstance(ax[0], matplotlib.figure.Figure)):
        raise TypeError("ax must be the object returned by create_plot()")

    # lists are all of correct length
    if not (len(color_values) == len(freq_values) == len(width_values) ==
            len(x_starts) == len(x_ends) == len(y_starts) == len(y_ends)):
        raise ValueError("x_starts, x_ends, y_starts, y_ends, color_values, "
                         "freq_values and width_values must all be of the "
                         "same length")
    if not len(x_starts) > 0:
        raise ValueError("Empty input lists")
    # numerical values only where required
    if not all(isinstance(i, Number) for i in x_starts):
        raise TypeError("x_starts values must be numeric")
    if not all(isinstance(i, Number) for i in x_ends):
        raise TypeError("x_ends values must be numeric")
    if not all(isinstance(i, Number) for i in y_starts):
        raise TypeError("y_starts values must be numeric")
    if not all(isinstance(i, Number) for i in y_ends):
        raise TypeError("y_ends values must be numeric")
    if not all(isinstance(i, Number) for i in color_values):
        raise TypeError("color values must be numeric")
    if not all(isinstance(i, Number) for i in freq_values):
        raise TypeError("freq values must be numeric")
    if not all(isinstance(i, Number) for i in width_values):
        raise TypeError("width values must be numeric")
    for i in [color_min, color_max, color_spread, freq_min, freq_max, 
              freq_spread, color_n, freq_n]:
        if not isinstance(i, Number) and not i==None:
            raise TypeError("Scale minimum, maximum and spread values and "
                            "number of values per scale must be numerical")
    if not isinstance(zorder, Number):
        raise TypeError("zorder must be a numerical value")
    if not isinstance(striped_length, Number):
        raise TypeError("striped_length must be a numerical value")

    if not isinstance(scale_dp, int):
        raise TypeError("scale_dp must be int")

    if not legend_marker_size == "auto" and not legend_marker_size == "mean":
        warnings.warn("legend_marker_size type invalid, auto will be used")

    # Set default values
    if color_max == None:
        color_max = max(color_values)
    if color_min == None:
        color_min = min(color_values)   
    if freq_max == None:
        freq_max = np.nanmax(freq_values)
    if freq_min == None:
        freq_min = np.nanmin(freq_values) 
    if color_spread == None:
        color_spread = color_max - color_min
    if freq_spread == None:
        freq_spread = freq_max - freq_min

    # Divergent scale is not available with the current edge design
    scale_diverges = False

    if color_n == None:
        categorical=False
    else:
        categorical=True

    # Apply a ravel in the event dataframe columns (for example) are passed
    x_starts = np.ravel(x_starts)
    x_ends = np.ravel(x_ends)
    y_starts = np.ravel(y_starts)
    y_ends = np.ravel(y_ends)
    color_values = np.ravel(color_values)
    freq_values = np.ravel(freq_values)
    width_values = np.ravel(width_values)

    # Fetch scale values
    color_scale = get_color_scale(color_values, color_max, color_min, 
                                    color_n, color_spread)
    color_mapping = get_color_mapping(color_scale, colormap)
    shape_scale = get_shape_scale(freq_values, freq_max, freq_min, freq_n, 
                                  scale_diverges, freq_spread) 
    frequency_scale = get_frequency_scale(shape_scale, scale_diverges)
    new_freq_scale = []
    for i in frequency_scale:
        if i == 0:
            new_freq_scale.append(1)
        else:
            new_freq_scale.append((i/3) * 2)
    
    # Add lines
    artists = []
    main_lines = []
    for i in range(len(x_starts)):

        main_line = ax[1].plot([x_starts[i], x_ends[i]], [y_starts[i], y_ends[i]],
                    color=get_color(color_values[i], colormap, color_mapping), 
                    linewidth=width_values[i], solid_capstyle='butt', 
                    zorder=zorder)[0]
        main_lines.append(main_line)
    
    # Store the artist object
    artists.append(dict(main_lines=main_lines))

    # This is critical for drawing with pixel length type - the aspect ratios
    # are needed for calculating the sizes of the striped sections but these 
    # are not updated from the original figure creation until something is 
    # drawn.
    ax[1].apply_aspect()

    # Get proportions of plot area, which may be required for some styles
    ax_h = ax[1].bbox.height
    ax_w = ax[1].bbox.width

    for i in range(len(x_starts)):
        artists.append(
            add_line_frequency(x_starts[i], 
                 y_starts[i],
                 x_ends[i], 
                 y_ends[i], 
                 get_frequency(freq_values[i], shape_scale, new_freq_scale, 
                               "closest"),
                 width_values[i], 
                 ax[1], 
                 style, 
                 freq_n, 
                 color_n, 
                 striped_length, 
                 length_type, 
                 ax_w, 
                 ax_h, 
                 zorder=zorder)
        )

    # Add the legend
    scale_x = ax[0].get_size_inches()[0]
    scale_y = ax[0].get_size_inches()[1]

    if legend_marker_size == "mean":
        width = np.mean(width_values)
    else:
        width = None

    if np.isnan(freq_values).any():
        include_nan=True
    else:
        include_nan=False

    add_line_legend(ax[3], color_scale, colormap, color_mapping, shape_scale, 
                    new_freq_scale, style, scale_x, scale_y, color_label, 
                    frequency_label, legend_title, width, scale_dp, 
                    label_fontsize, categorical=categorical, 
                    include_nan=include_nan)

    return artists


def return_figure(fig, return_type, file_name="vizent_plot_save"):
    """
    Return the created figure by your chosen method 

    :param fig: The tuple of matplotlib figure and axes objects returned by \
    :code:`create_plot()`.
    :type ax: tuple (matplotlib.figure, matplotlib.axes.Axes, \
    matplotlib.axes.Axes, matplotlib.axes.Axes, Numerical)
    :param return_type: The method for return the created plot. :code:`'show'`\
    displays the figure, :code:`'save'` saves the figure without displaying, \
    :code:`'return'` returns the axes for use with Matplotlib.
    :type return_type: :code:`'show'`, :code:`'save'`, :code:`'return'`
    :param file_name: if return_type is "save", the file name for your saved \
    file. This can be any format supported by Matplotlib. If no file \
    extension is included, .png is used by default. Default is \
    :code:`'vizent_plot_save'`
    :type file_name: str, optional
    :return: Matplotlib figure, if specified
    :rtype: maptlotlib.figure or None
    """
    if return_type == "return":
        return fig[0]
    elif return_type == "save":
        try:
            dpi = matplotlib.rcParams['figure.dpi']
            plt.savefig(file_name, dpi=dpi)
        except AttributeError:
            raise AttributeError("The specified file name is invalid. File "
                                 "name must be a string with or without a "
                                 "valid image file extension")
    else:
        plt.show()
    plt.close()


def vizent_plot(x_values: ArrayLike | None=None,
                y_values: ArrayLike | None=None, 
                color_values: ArrayLike | None=None, 
                shape_values: ArrayLike | None=None, 
                size_values: ArrayLike | None=None,
                # Introduce edge variables - currently with default values of None
                edge_start_points: ArrayLike | None=None, 
                edge_end_points: ArrayLike | None=None, 
                edge_colors: ArrayLike | None=None, 
                edge_frequencies: ArrayLike | None=None, 
                edge_widths: ArrayLike | None=None,
                # Figure options
                image_file: str | None=None, 
                use_cartopy: bool | None=False,
                cartopy_projection=None,
                extent: list | None=None,
                # Glyph options
                colormap: str | matplotlib.colors.Colormap | None="viridis", 
                scale_diverges: bool | None=None, 
                shape: str | None='sine', 
                shape_pos: str | None='sine', 
                shape_neg: str | None='square', 
                color_max: float | None=None, 
                color_min: float | None=None, 
                color_n: int | None=None, 
                color_spread: float | None=None,
                shape_max: float | None=None,
                shape_min: float | None=None, 
                shape_n: int | None=None, 
                shape_spread: float | None=None, 
                interval_type: str | None="closest",
                # Glyph legend options
                color_label: str | None='color',
                shape_label: str | None='shape', 
                glyph_legend_title: str | None='glyphs',
                # Line options
                edge_striped_length: float | None=1, 
                edge_length_type: str | None='units', 
                edge_colormap: str | None='viridis', 
                edge_style: str | None='middle', 
                edge_color_max: float | None=None, 
                edge_color_min: float | None=None, 
                edge_color_n: float | None=None, 
                edge_color_spread: float | None=None, 
                edge_freq_max: float | None=None, 
                edge_freq_min: float | None=None, 
                edge_freq_n: float | None=None, 
                edge_freq_spread: float | None=None, 
                edge_interval_type: str | None='closest',
                # Edge legend options
                edge_color_label: str | None='color', 
                edge_frequency_label: str | None='frequency', 
                edge_legend_title: str | None='lines', 
                scale_dp: int | None=1, 
                label_fontsize: int | None=None,
                # Args to deprecate
                scale_x=None, # create_plot - deprecate - this should be handled outside the pure plotting function
                scale_y=None, # create_plot - deprecate - same as above
                use_image=None, # create_plot - deprecate - can be determined by whether or not an image file is supplied
                image_type=None, # create_plot - deprecate - the option to use pre-baked images is too narrow for general usage
                colour_values=None, # deprecate - renamed to color
                colour_max=None,  # glyphs - deprecate - renamed to color
                colour_min=None, # glyphs - deprecate - renamed to color
                colour_n=None,  # glyphs - deprecate - renamed to color
                colour_spread=None,  # glyphs - deprecate - renamed to color
                colour_label=None, # deprecate - renamed to color
                title=None, # deprecate - doesn't work with new spacing and can be added via mpl if needed
                show_legend=None, # deprecate - I think legends ought to be included by default with this interface
                x_label=None,  # deprecate - this can be added via the matplotlib interface directly
                y_label=None,  # deprecate - this can be added via the mpl interface directly
                show_axes=None,  # deprecate - can be handled via mpl interface directly. We'll turn off axes if images or map backgrounds are used. 
                save=None,  # deprecate - we'll return the mpl objects and then the user can save via the mpl interface
                file_name=None,  # deprecate - images can be saved by the user directly.
                return_axes=None):  # deprecate - axes should be returned and then saved if required.
    """
    Convenience function for implementing the vizent pipeline.

    :param x_values:  Positions of glyphs on the x-axis
    :type x_values: float or array-like, shape (n,), optional
    :param y_values:  Positions of glyphs on the y-axis
    :type y_values: float or array-like, shape (n,), optional
    :param color_values: The values to be represented by the color of each \
    glyph
    :type color_values: float or array-like, shape (n,), optional
    :param shape_values: the list of values to be represented by the outer \
    shape of each glyph
    :type shape_values: float or array-like, shape (n,), optional
    :param size_values: the list of values in points for the diameter of each \
    glyph
    :type size_values: float or array-like, shape(n,), optional
    :param edge_start_points: (x,y) coordinates for each line origin
    :type edge_start_points: array-like, shape(n,2), optional
    :param edge_end_points: (x,y) coordinates for each line end point
    :type edge_end_points: array-like, shape(n,2), optional
    :param edge_colors: The values to be represented by the color of each \
    line.
    :type color: float or array-like, shape (n,), optional
    :param edge_frequencies: The list of values to be represented by the central \
    stripe frequency.
    :type edge_frequencies: float or array-like, shape (n,), optional
    :param edge_widths: The list of values in points for the width of each \
    line.
    :type edge_widths: float or array-like, shape(n,), optional
    :param image_file: filepath to a user-supplied image-file to be used as a \
    background image for the plot.
    :type image_file: str, optional.
    :param use_cartopy: If True, use Cartopy to generate a map background. \
    Must specify extent if used. Defaults to False.
    :type use_cartopy: boolean, optional
    :param extent: Axis limits or extent of coordinates for Cartopy. A list of\
    four values in the form: :code:`[xmin, xmax, ymin, ymax]`.
    :param colormap: the matplotlib colormap to be used for the glyphs. \
    The default is :code:`viridis`.
    :type colormap: matplotlib.colors.Colormap or str, optional
    :param scale_diverges: If :code:`True`, diverging sets of glyphs are used \
    for positive and negative values. If not specified, your scale will diverge\
    if both positive and negative values are included for the shape variable.
    :type scale_diverges: boolean, optional
    :param shape: Glyph shape design to use for non-divergent scales. Default \
    :code:`'sine'`.
    :type shape: :code:`'sine'`, :code:`'saw'`, :code:`'reverse_saw'`, \
    :code:`'square'`, :code:`'triangular'`, :code:`'concave'`, :code:`'star'`.
    :param shape_pos: When using divergent scale, glyph shape design to use \
    for positive values. Options as for shape. Default :code:`'sine'`.
    :type shape_pos: :code:`'sine'`, :code:`'saw'`, :code:`'reverse_saw'`, \
    :code:`'square'`, :code:`'triangular'`, :code:`'concave'`, :code:`'star'`     
    :param shape_neg: When using divergent scale, glyph shape design to use for \
    negative values. Options as for shape. Default :code:`'square'`.
    :type shape_neg: :code:`'sine'`, :code:`'saw'`, :code:`'reverse_saw'`, \
    :code:`'square'`, :code:`'triangular'`, :code:`'concave'`, :code:`'star'`    
    :param color_max: The maximum color value in the glyph legend.
    :type color_max: float, optional
    :param color_min: The minimum color value in the glyph legend.
    :type color_min: float, optional
    :param color_n: The number of color values to show in the glyph legend.
    :type color_n: int, optional
    :param color_spread: Range of color values in glyph legend. Only used if not \
    specifying both max and min.
    :type color_spread: float, optional
    :param shape_max: The maximum shape value in the glyph legend.
    :type shape_max: float, optional
    :param shape_min: The minimum shape value in the glyph legend.
    :type shape_min: float, optional
    :param shape_n: The number of shape values to show in the glyph  legend. 
    :type shape_n: int, optional
    :param shape_spread: Range of shape values in glyph legend. Only used if not \
    specifying both max and min. 
    :type shape_spread: float, optional
    :param color_label: The title for the color component of the glyph legend. \
    Defaults to :code:`'color'`.
    :type color_label: str, optional
    :param shape_label: The title for the shape component of the glyph legend. \
    Defaults to :code:`'shape'`. 
    :type shape_label: str, optional
    :param glyph_legend_title: The main title for the glyph legend. Defaults to \
    :code:`'glyphs'`.
    :type glyph_legend_title: str, optional
    :param edge_striped_length: if using the style :code:`'set_length'`, the \
    length of the central stripe. Units determined by :code:`length_type`. \
    Defaults to :code:`1`.
    :type edge_striped_length: float, optional
    :param edge_length_type: The units to be used for stripe length. \
    :code:`'units'` uses axes units, :code:`'pixels'` uses the number of \
    pixels and :code:`'proportion'` uses the proportion of the line.
    :type edge_length_type: (:code:`'units'`, :code:`'pixels'`, \
    :code:`'proportion'`), optional
    :param edge_colormap: the matplotlib colormap to be used. Defaults to \
    :code:`viridis`.
    :type edge_colormap: matplotlib.colors.Colormap or str, optional
    :param edge_style: The length and positioning style of the striped area. \
    :code:`'middle'` generates a striped area centred on the line/edge where \
    with length of striped area 1/3 of edge length. :code:`'ends'` \
    generates a striped area at each end of the line/edge with length of \
    striped area 1/4 of total edge length. :code:`'source'` \
    generates a striped area at the source of the line, 1/2 of the total edge \
    length. :code:`'destination'` generates a striped area at the line \
    destination, where the striped area is 1/2 of the total edge length. \
    :code:`'set_length'` generates a striped area at the centre of the line, \
    with the length specified by user via the :code:`edge_striped_length` parameter,\
    :code:`'frequency'` generates a striped area at the centre of the line, \
    1/3 edge length. Instead of a set number of stripes, this uses the number \
    of stripes per unit length, matched to the legend. Defaults to \
    :code:`'middle'`.
    :type edge_style: (:code:`'middle'`, :code:`'ends'`, :code:`'source'`, \
    :code:`'destination'`), optional.   
    :param edge_color_max: The maximum color value in the legend.
    :type edge_color_max: float, optional
    :param edge_color_min: The minimum color value in the legend.
    :type edge_color_min: float, optional
    :param edge_color_n: The number of color values to show in the legend.
    :type edge_color_n: int, optional
    :param edge_color_spread: Range of color values in key. Only used if not \
    specifying both max and min.
    :type edge_color_spread: float, optional    
    :param edge_freq_max: The maximum frequency value in the legend.
    :type edge_freq_max: float, optional
    :param edge_freq_min: The minimum frequency value in the legend.
    :type edge_freq_min: float, optional
    :param edge_freq_n: The number of frequency values to show in the legend. 
    :type edge_freq_n: int, optional
    :param edge_freq_spread: Range of frequency values in key. Only used if not \
    specifying both max and min. 
    :type edge_freq_spread: float, optional
    :param edge_color_label: The title for the color component of the legend. \
    Defaults to :code:`'color'`.
    :type edge_color_label: str, optional
    :param edge_frequency_label: The title for the frequency component of the legend. \
    Defaults to :code:`'frequency'`. 
    :type edge_frequency_label: str, optional
    :param edge_legend_title: The main title for the glyph legend. Defaults to \
    :code:`'lines'`.
    :type edge_legend_title: str, optional
    :param scale_dp: The number of decimal places to round to for legend \
    values. Defaults to :code:`2`.
    :type scale_dp: int, optional
    :param label_fontsize: If set, will set all legend labels to this \
    fontsize. Otherwise, the fontsize will be estimated automatically based on\
    the length of the labels.
    :type label_fontize: int, optional
    :return: Matplotlib figure
    :rtype: maptlotlib.figure
    """

    # handle deprecation of arguments

    if scale_x is not None:
        msg = 'The argument scale_x is deprecated. Figure' \
               ' resizing can be accomplished via figure.set_size_inches()' \
               ' method on the returned matplotlib figure or via the' \
               ' create_plot() function in the Vizent library'
        warnings.warn(msg, DeprecationWarning, stacklevel=1)
        
    if scale_y is not None:
        msg = 'The argument scale_y is deprecated. Figure ' \
               'resizing can be accomplished via figure.set_size_inches() ' \
               'method on the returned matplotlib figure or via the '\
               'create_plot() function in the Vizent library'
        warnings.warn(msg, DeprecationWarning,stacklevel=1)

    if use_image is not None:
        msg = 'The argument use_image is deprecated. An image ' \
               'background will be used if an image_file is supplied'
        warnings.warn(msg, DeprecationWarning,stacklevel=1)    

    if image_type is not None:
        msg = 'Using packaged images as background images is ' \
              'deprecated and will be removed in a future verison. ' \
              'The image should be provided via the image_file ' \
              'argument instead.'
        warnings.warn(msg, DeprecationWarning,stacklevel=1)
     
    colour_args = [colour_values, colour_max, colour_min, colour_n, colour_spread, colour_label]
    if sum([arg is not None for arg in colour_args]) > 0:
        msg = "Arguments with using the word 'colour' are deprecated " \
              "and will be replaced by the spelling 'color' in a future "\
              "version"
        warnings.warn(msg, DeprecationWarning,stacklevel=1)
        if color_values is None:
            color_values = colour_values
        if color_max is None:
            color_max = colour_max
        if color_min is None:
            color_min = colour_min
        if color_n is None:
            color_n = colour_n
        if color_spread is None:
            color_spread = colour_spread
        if color_label is None:
            color_label = colour_label

                      
    if title is not None:        
        msg = "The title argument is deprecated and will be removed in " \
              "a future version. Figure titles should be added using " \
              "the matplotlib fig.suptitle() method."
        warnings.warn(msg, DeprecationWarning,stacklevel=1)

    if show_legend is not None:
        msg = "The show_legend argument is deprecated and will be removed in " \
              " a future version. Legends will be shown by default."
        warnings.warn(msg, DeprecationWarning,stacklevel=1)

    if x_label is not None:
        msg = "The argument x_label is deprecated and will be removed in a " \
              "future version. x_labels can be added via the matplotlib " \
              "interface, using ax.set_xlabel()."
        warnings.warn(msg, DeprecationWarning,stacklevel=1)

    if y_label is not None:
        msg = "The argument y_label is deprecated and will be removed in a " \
              "future version. y_labels can be added via the matplotlib " \
              "interface, using ax.set_ylabel()."
        warnings.warn(msg, DeprecationWarning,stacklevel=1)
    
    if show_axes is not None:
        msg = "The argument show_axes is deprecated and will be removed in a "\
              "future version. The axes will be shown by default for standard "\
              "plots and hidden for maps and background images. Axis behaviour "\
              "can be configured via the matplotlib interface, using ax.axis()"
        warnings.warn(msg, DeprecationWarning,stacklevel=1)

    if save is not None:
        msg = "The save argument is deprecated and will be removed in a future "\
              "version. The axes will always be returned and can be saved using "\
              "fig.savefig() via matplotlib."
        warnings.warn(msg, DeprecationWarning,stacklevel=1)

    if file_name is not None:
        msg = "The save functionality is deprecated and the file_name argument "\
              "will be removed in a future version. The axes will always be "\
              "returned and can be saved using fig.savefig() via matplotlib."
        warnings.warn(msg, DeprecationWarning,stacklevel=1)

    if return_axes is not None:
        msg = "The return_axes argument is deprecated and will be removed in a "\
              "future version. Axes will always be returned."
        warnings.warn(msg, DeprecationWarning,stacklevel=1)
    
    use_glyphs = (x_values is not None)
    use_lines = (edge_start_points is not None)
    
    if use_cartopy or image_file is not None:
        show_axes=False
    else:
        show_axes=True

    fig = create_plot(use_glyphs=use_glyphs, 
                      use_lines=use_lines, 
                      show_legend=True, 
                      show_axes=show_axes, 
                      use_cartopy=use_cartopy, 
                      cartopy_projection=cartopy_projection,
                      use_image=image_file is not None, 
                      image_type=None, 
                      image_file=image_file, 
                      extent=extent)

    if x_values is not None:

        add_glyphs(fig, 
                    x_values, 
                    y_values, 
                    color_values, 
                    shape_values, 
                    size_values, 
                    colormap=colormap, 
                    scale_diverges=scale_diverges, 
                    shape=shape, 
                    shape_pos=shape_pos, 
                    shape_neg=shape_neg, 
                    color_max=color_max, 
                    color_min=color_min, 
                    color_n=color_n, 
                    color_spread=color_spread, 
                    shape_max=shape_max, 
                    shape_min=shape_min, 
                    shape_n=shape_n, 
                    shape_spread=shape_spread,
                    color_label=color_label, 
                    shape_label=shape_label, 
                    scale_dp=scale_dp,
                    interval_type=interval_type, 
                    legend_title=glyph_legend_title, 
                    label_fontsize=label_fontsize)
    
    #Extract line edges
    if edge_start_points is not None:

        if not (len(edge_start_points)==len(edge_end_points)):
            #Initial check before we expand the points provided to x,y coords
            #More detailed input checking is performed in the add_lines function
            raise ValueError("edge_start_points must be the same length as " \
                            " edge_end_points")

        if np.ndim(edge_start_points) != 2 or np.ndim(edge_end_points) != 2:
            raise ValueError("Edge start points and edge end points must be "\
                             "two-dimensional.")

        x_starts = [i[0] for i in edge_start_points]
        y_starts = [i[1] for i in edge_start_points]
        x_ends = [i[0] for i in edge_end_points]
        y_ends = [i[1] for i in edge_end_points]

        add_lines(ax=fig, 
                  x_starts=x_starts, 
                  y_starts=y_starts, 
                  x_ends=x_ends, 
                  y_ends=y_ends, 
                  color_values=edge_colors,
                  freq_values=edge_frequencies, 
                  width_values=edge_widths, 
                  striped_length=edge_striped_length, 
                  length_type=edge_length_type,               
                  colormap=edge_colormap, 
                  style=edge_style, 
                  color_max=edge_color_max, 
                  color_min=edge_color_min, 
                  color_n=edge_color_n, 
                  color_spread=edge_color_spread, 
                  freq_max=edge_freq_max, 
                  freq_min=edge_freq_min, 
                  freq_n=edge_freq_n, 
                  freq_spread=edge_freq_spread,
                  color_label=edge_color_label, 
                  frequency_label=edge_frequency_label, 
                  legend_title=edge_legend_title, 
                  scale_dp=scale_dp, 
                  interval_type=edge_interval_type, 
                  legend_marker_size="auto", 
                  zorder=0.5, 
                  label_fontsize=label_fontsize)

    return fig[0]