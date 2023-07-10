""" The user accessible functions of the vizent library.

This module contains the user accessible functions of the vizent 
library. These functions can be used to create a plot in up to four 
steps: preparing the plot area, adding glyphs, adding lines, and 
returning the completed plot. 

Functions:
    create_plot(glyphs=True, lines=True, show_legend=True, 
                show_axes=True, use_cartopy=False, use_image=False, 
                image_type=None, image_file=None, extent=None, 
                scale_x=None, scale_y=None)
    add_glyphs(ax, x_values, y_values, color_values, shape_values, 
               size_values, colormap="viridis", scale_diverges=None, 
               shape="sine", shape_pos="sine", shape_neg="square", 
               color_max=None, color_min=None, color_n=None, 
               color_spread=None, shape_max=None, shape_min=None, 
               shape_n=None, shape_spread=None, color_label="color", 
               shape_label="shape", legend_title="glyphs", scale_dp=2, 
               interval_type="closest", legend_marker_size="auto")
    add_lines(ax, x_starts, y_starts, x_ends, y_ends, color_values,
              freq_values, width_values, striped_length=1, 
              length_type="units", colormap="viridis", style="middle", 
              color_max=None, color_min=None, color_n=4, 
              color_spread=None, freq_max=None, freq_min=None, 
              freq_n=4, freq_spread=None, color_label="color", 
              shape_label="shape", legend_title="lines", scale_dp=2, 
              interval_type="closest", legend_marker_size="auto")
    return_figure(fig, return_type, file_name="vizent_plot_save")

Typical usage example:
    # This library requires several functions to be called sequentially.
    # First the plot area is prepared. This includes specifications
    # relating to the axes, plot area background and legends.

    axes=create_plot(use_image=True, image_file="image.jpg", 
                     extent=[0,6,0,6])

    # Next any glyphs and lines are added. This can be done in any 
    # order, glyphs will always be placed on top of lines.

    x_values = [1,4,2,3]
    y_values = [1,5,2,5]
    color_values = [1,2,3,4]
    shape_values = [1,2,3,4] 
    size_values = [30,30,30,30]

    add_glyphs(axes, x_values, y_values, color_values, shape_values, 
               size_values)

    x_starts = [2,1]
    y_starts = [2,1]
    x_ends = [4,3]
    y_ends = [5,5]
    color_values = [4,1]
    shape_values = [4,1] 
    width_values = [15,15]

    add_lines(axes, x_starts, y_starts, x_ends, y_ends, color_values, 
              shape_values, width_values)

    # Finally, the created figure is returned in the required manner.
              
    return_figure(axes, "display")
"""
import importlib
import matplotlib.pyplot as plt
from matplotlib import gridspec

from vizent.glyph_shapes import shapes, get_shape_points
from vizent.scales import *

def add_point(x, y, shape, frequency, color, size, ax):
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


def add_line(x_origin, y_origin, x_end, y_end, frequency, color, width, ax, 
             style, freq_n, color_n, striped_length, length_type, ax_w, ax_h, 
             zorder):
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
             "frequency": [1/3, 1, 1/3]}
    
    try:
        striped_section_length = length * styles[style][0]
    except:
        raise ValueError("line style invalid")
    
    # Plot main colored line
    main_line = ax.plot([x_origin, x_end], [y_origin, y_end], color=color, 
                         linewidth=width, solid_capstyle='butt', 
                         zorder=zorder)[0]

    # Plot the striped section
    stripes = 1 + (2*frequency)
    extra = 0

    if style == "frequency":
        actual_length = (np.sqrt((dy*unit_size_y)**2 + (dx*unit_size_x)**2))
        actual_striped_section_length = actual_length * styles[style][0]

        n_glyphs = max(freq_n, color_n)

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
                ax.plot([x_0, x_1], [y_0, y_1], color='white', linewidth=width, 
                        solid_capstyle='butt', zorder=zorder)[0]
            )
    # Return the lists of 2DLine objects
    return dict(main_line=main_line, striped_base_lines=striped_base_lines, 
                striped_white_lines=striped_white_lines)


def add_glyph_legend(ax2, color_scale, colormap, color_mapping, shape_scale, 
                     frequency_scale, shape, shape_pos, shape_neg, divergent, 
                     scale_x, scale_y, color_label, shape_label, title, size, 
                     scale_dp):
    # TODO: Number of dps should be included in this function as a text 
    # formatting option within the legend and removed from the color scaling -
    # otherwise we might run into floating point issues.



    # Fixed positions and limits
    x_positions = [0.75, 3.25]
    y_title = 9.5
    y_subtitle = 8.9
    ymax = 10
    ymax_glyphs = 8.75
    ymin = 0

    # Calculated positions
    color_y_positions = [(x-0.5) * (ymax_glyphs/(len(color_scale))) 
                          for x in reversed(range(1, len(color_scale) + 1))]
    shape_y_positions = [(x-0.5) * (ymax_glyphs/len(frequency_scale)) 
                         for x in reversed(range(1, len(frequency_scale) + 1))]

    # Axis formatting
    ax2.set_xlim(0, 5)
    ax2.set_ylim(ymin, ymax)
    ax2.axes.xaxis.set_visible(False)
    ax2.axes.yaxis.set_visible(False)

    # Size calculations for glyphs and text
    n_glyphs = max(len(color_scale), len(shape_scale))

    y_size = (1 / (3*n_glyphs)) * scale_y
    x_size = scale_y / 12

    if size == None:
        size = (min(x_size, y_size) / 0.014)

    heading_size = min((1.5 * (scale_y/3) / (len(str(title))*0.014)), 25)
    title_size = 0.55 * ((scale_y/3) / (max(len(str(color_label)), 
                          len(str(shape_label)))*0.014))
    label_size = (0.25 * ((scale_y/3) / (max(len(str(max(color_scale))), 
                          len(str(max(shape_scale))))*0.014)))

    # Add legend title
    ax2.annotate(title, ((x_positions[0]+x_positions[1]+1) / 2, y_title), 
                 ha='center', va='center', size=heading_size)

    # Add color scale
    ax2.annotate(color_label, (x_positions[0] + 0.5, y_subtitle), ha='center', 
                   va='center', size=title_size)
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
                     size=label_size)
    # Add shape scale
    ax2.annotate(shape_label, (x_positions[1] + 0.5, y_subtitle), ha='center', 
                 va='center', size=title_size)
    for i in range(len(shape_y_positions)):
        add_point(x_positions[1], 
                  color_y_positions[i],
                  get_shape(shape_scale[i], shape, divergent, shape_pos, 
                            shape_neg),
                  frequency_scale[i], 
                  (0.74902, 0.74902, 0.74902), 
                  size, 
                  ax2)
        ax2.annotate("{:.{prec}f}".format(shape_scale[i],prec=scale_dp), 
                     (x_positions[1] + 1.1, color_y_positions[i]), 
                     ha='center', 
                     va='center', 
                     size=label_size)


def add_line_legend(ax3, color_scale, colormap, color_mapping, shape_scale, 
                    frequency_scale, style, scale_x, scale_y, color_label, 
                    shape_label, title, width, scale_dp):

    # Fixed positions and limits
    x_positions = [0.75, 3.25]
    y_title = 9.5
    y_subtitle = 8.9
    ymax = 10
    ymax_glyphs = 8.75
    ymin = 0

    # Calculated positions
    color_y_positions = [(x-0.5) * (ymax_glyphs/(len(color_scale))) 
                          for x in reversed(range(1, len(color_scale) + 1))]
    shape_y_positions = [(x-0.5) * (ymax_glyphs/len(frequency_scale)) 
                         for x in reversed(range(1, len(frequency_scale) + 1))]

    # Axis formatting
    ax3.set_xlim(0, 5)
    ax3.set_ylim(ymin, ymax)
    ax3.axes.xaxis.set_visible(False)
    ax3.axes.yaxis.set_visible(False)

    # Size calculations for lines and text
    color_length = ((ymax_glyphs-ymin) / len(color_scale))*0.7
    shape_length = ((ymax_glyphs-ymin) / len(frequency_scale))*0.7
    y_size = (1 / (2*ymax)) * scale_y
    x_size = scale_y / 12

    if width == None:
        width = 0.5 * (min(x_size, y_size)/0.014)

    heading_size = min((1.5 * (scale_y/3) / (len(str(title))*0.014)), 25)
    title_size = 0.55 * ((scale_y/3) / (max(len(str(color_label)), 
                          len(str(shape_label)))*0.014))
    label_size = (0.25 * ((scale_y/3) / (max(len(str(max(color_scale))), 
                          len(str(max(shape_scale))))*0.014)))

    # Add legend title
    ax3.annotate(title, ((x_positions[0]+x_positions[1]+1) / 2, y_title), 
                 ha='center', va='center', size=heading_size)

    # Add color scale
    ax3.annotate(color_label, (x_positions[0] + 0.5, y_subtitle), ha='center', 
                   va='center', size=title_size)
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
                     size=label_size)

    # Add shape scale
    ax3.annotate(shape_label, (x_positions[1] + 0.5, y_subtitle), ha='center', 
                 va='center', size=title_size)
    for i in range(len(shape_y_positions)):
        # Black line
        ax3.plot([x_positions[1], x_positions[1]],
                 [shape_y_positions[i] + (shape_length/2), 
                  shape_y_positions[i] - (shape_length/2)], 
                 color='black', 
                 linewidth=width, 
                 solid_capstyle='butt', 
                 zorder=0)  
        # White stripes
        stripes = 1 + (2*frequency_scale[i])
        stripe_diff_x = 0
        stripe_diff_y = shape_length / stripes
    
        for j in range(int(stripes)):
            if j%2 != 0:
                x_0 = x_positions[1] + stripe_diff_x*j
                y_0 = ((shape_y_positions[i] - (shape_length/2)) 
                       + stripe_diff_y*j)
                x_1 = x_positions[1] + stripe_diff_x*(j+1)
                y_1 = ((shape_y_positions[i] - (shape_length/2)) 
                       + stripe_diff_y*(j+1))

                ax3.plot([x_0, x_1], [y_0, y_1], color='white', 
                         linewidth=width, solid_capstyle='butt', zorder=1)
        
        ax3.annotate("{:.{prec}f}".format(shape_scale[i],prec=scale_dp), 
                     (x_positions[1] + 1.1, shape_y_positions[i]), 
                     ha='center', 
                     va='center', 
                     size=label_size)


def create_plot(glyphs=True, lines=True, show_legend=True, show_axes=True,
                use_cartopy=False, use_image=False, image_type=None, 
                image_file=None, extent=None, scale_x=None, scale_y=None):
    """
    Create the figure used to plot glyphs and/or lines. This function
    must be executed first, and the output is used as an input to all
    other functions.

    Parameters:
        glyphs (Boolean, default: True):
            Set True if glyphs are to be plotted.
        lines (Boolean, default: True):
            Set True if lines are to be plotted.
        show_legend (Boolean, default: True):
            If True, show legends for glyphs/lines as included. 
        show_axes (Boolean, default: True):
            If True, show axis labels.
        use_cartopy (Boolean, default: False):
            If True, use Cartopy to generate a map background. Must
            specify extent if used.
        use_image (Boolean, default: False):
            If True, use an image as a background. Must specify extent
            if used.
        image_type (str, optional):
            "newcastle": detailed 3D rendered image of Newcastle Upon
                Tyne (available for limited coordinates)
            "england": OpenStreetMap England map
            otherwise: the specified image file is used
        image_file (str, optional):
            Path to the image file to use as the background.
        extent (list of int, optional):
            Axis limits or extent of coordinates for Cartopy. A list of
            four values in the form: [xmin, xmax, ymin, ymax].  
        scale_x (int, optional):
            Width of plot window in inches.
        scale_y (int, optional):
            Height of plot window in inches.

    Returns:
        fig (matplotlib.figure):
            The matplotlib figure object which will contain the axes.
        ax1 (matplotlib.axes.SubplotBase):
            The matplotlib axes object for the main plot.
        ax2 (matplotlib.axes.SubplotBase):
            The matplotlib axes object used for the glyph legend.
        ax3 (matplotlib.axes.SubplotBase):
            The matplotlib axes object used for the line legend.
        asp (Numerical):
            The aspect ratio of the main plot area (necessary to ensure
            the legends display correctly when using image or map
            backgrounds).
    """
    # input checking

    # scale values are numeric
    if not isinstance(scale_x, (int, float)) and not scale_x==None:
        print("scale_x must be numeric. Default will be used")
        scale_x = None
    if not isinstance(scale_y, (int, float)) and not scale_y==None:
        print("scale_y must be numeric. Default will be used")
        scale_y = None
    if scale_x is not None and scale_x <=0:
        print("scale_x must be a positive value. Default will be used.")
        scale_x = None
    if scale_y is not None and scale_y <=0:
        print("scale_y must be a positive value. Default will be used.")
        scale_y = None
    # check extent format 
    if extent is not None:
        if not isinstance(extent, list) or len(extent) != 4:
            raise ValueError("extent must be a list of four values")
        for i in list(extent):
            if not isinstance(i, (int, float)):
                raise ValueError("extent values must be numerical")

    # Set up the plot area 
    if use_cartopy or use_image:
        if use_cartopy: 
            try:
                importlib.import_module("cartopy")
                import background_map     
            except ImportError:
                raise ImportError("Missing optional dependency cartopy")
        if use_image:
            try:
                importlib.import_module("PIL")
                from background_image import get_image, add_image_background, get_image_size
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
                aspx, aspy = get_image_size()
            except:
                print("Image file not found or not valid. Figure will be "
                      "created without image background.")
                use_image = False
                if extent is not None:
                    aspx = extent[1] - extent[0]
                    aspy = extent[3] - extent[2]
                else:
                    aspx = 1
                    aspy = 1
    elif use_cartopy:
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
            if glyphs and lines:
                if show_legend:
                    gs = gridspec.GridSpec(1, 3, width_ratios=[3, 1, 1]) 
                else:
                    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0, 0]) 
                ax2 = plt.subplot(gs[1])
                ax3 = plt.subplot(gs[2]) 
            else:
                if show_legend:
                    gs = gridspec.GridSpec(1, 3, width_ratios=[3, 1, 0])
                    if glyphs:
                        ax2 = plt.subplot(gs[1])
                        ax3 = plt.subplot(gs[2])
                    elif lines:
                        ax3 = plt.subplot(gs[1]) 
                        ax2 = plt.subplot(gs[2])
                else:
                    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0, 0])
                    ax2 = plt.subplot(gs[1])
                    ax3 = plt.subplot(gs[2]) 
        else:
            if glyphs and lines:
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
                    if glyphs:
                        ax2 = plt.subplot(gs[1])
                        ax3 = plt.subplot(gs[2])
                    elif lines:
                        ax3 = plt.subplot(gs[1]) 
                        ax2 = plt.subplot(gs[2])
                else:
                    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0, 0])
                    ax2 = plt.subplot(gs[1])
                    ax3 = plt.subplot(gs[2]) 
    else:
        if glyphs and lines:
            if show_legend:
                gs = gridspec.GridSpec(1, 3, width_ratios=[(3 / asp), 1, 1]) 
            else:
                gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0, 0]) 
            ax2 = plt.subplot(gs[1])
            ax3 = plt.subplot(gs[2]) 
        else:
            if show_legend:
                gs = gridspec.GridSpec(1, 3, width_ratios=[(3 / asp), 1, 0])
                if glyphs:
                    ax2 = plt.subplot(gs[1])
                    ax3 = plt.subplot(gs[2])
                elif lines:
                    ax3 = plt.subplot(gs[1]) 
                    ax2 = plt.subplot(gs[2])
            else:
                gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0, 0])
                ax2 = plt.subplot(gs[1])
                ax3 = plt.subplot(gs[2])

    if use_cartopy:
        ax1 = background_map.get_basemap(gs, extent, show_axes)
    else:
        ax1 = plt.subplot(gs[0])
                
    if use_image:
        x_values=[np.average(extent[0:2])]
        y_values=[np.average(extent[2:4])]
        if image_type == "newcastle" or image_type == "england":
            extent = get_image(x_values, y_values, image_type, image_file)[1]
        try:
            add_image_background(get_image(x_values, y_values, image_type, 
                                           image_file)[0], ax1, extent) 
        except:
            print("Image file not found or not valid. Figure will be created "
                  "without image background.")
            use_image = False

    # Work out scaling of plot window 
    if show_legend:
        if glyphs and not lines or lines and not glyphs: 
            fig_aspect = aspy / (aspx + (1/3)*aspy)
        elif glyphs and lines:
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
        if lines and not glyphs:
            fig.delaxes(ax2)
        if glyphs and not lines:
            fig.delaxes(ax3)

    if not use_cartopy and not use_image and extent is not None:
        ax1.set_xlim(extent[0], extent[1])
        ax1.set_ylim(extent[2], extent[3])
        ax1.set_aspect('equal', 'box')

    plt.tight_layout()
    
    return fig, ax1, ax2, ax3, asp              


def add_glyphs(ax, x_values, y_values, color_values, shape_values, 
               size_values, colormap="viridis", scale_diverges=None, 
               shape="sine", shape_pos="sine", shape_neg="square", 
               color_max=None, color_min=None, color_n=None, 
               color_spread=None, shape_max=None, shape_min=None, 
               shape_n=None, shape_spread=None, color_label="color", 
               shape_label="shape", legend_title="glyphs", scale_dp=2, 
               interval_type="closest", legend_marker_size="auto"):
    """
    Add glyphs/nodes to the plot.

    Parameters:
        ax (tuple (matplotlib.figure, matplotlib.axes.SubplotBase, 
            matplotlib.axes.SubplotBase, matplotlib.axes.SubplotBase, 
            Numerical)): 
            This must be the tuple returned by create_plot().
        x_values (list of float): 
            The x coordinate of each glyph.
        y_values (list of float): 
            The y coordinate of each glyph.
        color_values (list of float): 
            The values to be represented by the color of each
            glyph.
        shape_values (list of float): 
            the list of values to be represented by the outer shape of
            each glyph.
        size_values (list of float): 
            the list of values in points for the diameter of each glyph.
        colormap (matplotlib.colors.Colormap, default: "viridis"): 
            the matplotlib colormap to be used.
        scale_diverges (boolean, optional):
            If True, diverging sets of glyphs are used for positive and
            negative values. If not specified, your scale will diverge
            if both positive and negative values are included for the
            shape variable.
        shape (str, default: "sine"):
            Glyph shape design to use for non-divergent scales.
                "sine"
                "saw"
                "reverse_saw"
                "square"
                "triangular"
                "concave"
                "star"
        shape_pos (str, default: "sine"):
            When using divergent scale, glyph shape design to use for 
            positive values. Options as for shape.
        shape_neg (str, default: "square"):
            When using divergent scale, glyph shape design to use for 
            negative values. Options as for shape.
        color_max (float), optional: 
            The maximum color value in the legend.
        color_min (float), optional: 
            The minimum color value in the legend.
        color_n (int), optional: 
            The number of color values to show in the legend.
        color_spread (float), optional: 
            Range of color values in key. Only used if not specifying
            both max and min.
        shape_max (float), optional: 
            The maximum shape value in the legend.
        shape_min (int), optional: 
            The minimum shape value in the legend.
        shape_n (int), optional: 
            The number of shape values to show in the legend. 
        shape_spread (float), optional:
            Range of shape values in key. Only used if not 
            specifying both max and min. 
        color_label (str, default: "color"):
            The heading for the color component of the legend.
        shape_label (str, default: "shape"):
            The heading for the shape component of the legend.
        legend_title (str, default: "glyphs"):
            The main title for the glyph legend.
        scale_dp (int, default: 2):
            The number of decimal places to round to for legend values.
        interval_type (str, default: "closest"):
            This defines how the shape of each glyph is determined:
                "closest": use the closest scale value.
                "limit": use the highest scale value that the glyph 
                    value is greater than or equal to (based on modulus
                    for negative values).
        legend_marker_size (str, default: "auto"):
            This controls the diameter of the legend glyph markers.
                "auto": diameter is calculated automatically to fit.
                "mean": use the mean diameter/size value of the plotted
                    glyphs.
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
    if not all(isinstance(i, (int, float)) for i in x_values):
        raise TypeError("x values must be numeric")
    if not all(isinstance(i, (int, float)) for i in y_values):
        raise TypeError("y values must be numeric")
    if not all(isinstance(i, (int, float)) for i in color_values):
        raise TypeError("color values must be numeric")
    if not all(isinstance(i, (int, float)) for i in shape_values):
        raise TypeError("shape values must be numeric")
    if not all(isinstance(i, (int, float)) for i in size_values):
        raise TypeError("size values must be numeric")
    for i in [color_min, color_max, color_spread, shape_min, shape_max, 
              shape_spread, color_n, shape_n]:
        if not isinstance(i, (int, float)) and not i==None:
            raise TypeError("Scale minimum, maximum and spread values and "
                            "number of values per scale must be numerical")
    if not isinstance(scale_dp, int):
        raise TypeError("scale_dp must be int")

    # valid shape is specified
    if not shape in shapes:
        print("'{0}' is not a supported shape. "
              "Default will be used".format(str(shape)))
        shape="sine"
    if not shape_pos in shapes:
        print("'{0}' is not a supported shape. "
              "Default will be used".format(str(shape_pos)))
        shape_pos="sine"
    if not shape_neg in shapes:
        print("'{0}' is not a supported shape. "
              "Default will be used".format(str(shape_neg)))
        shape_neg="square"

    if not legend_marker_size == "auto" and not legend_marker_size == "mean":
        print("legend_marker_size type invalid, auto will be used")

    # Set default values
    if scale_diverges == None:
        scale_diverges = scale_is_divergent(shape_values)
    
    if color_n == None:
        if shape_n == None:
            if scale_diverges:
                color_n = 7
            else:
                color_n = 5
        else:
            if scale_diverges:
                color_n = (2*shape_n) - 1
            else:
                color_n = shape_n     
    
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
                     shape_label, legend_title, size, scale_dp)
    return artists


def add_lines(ax, x_starts, y_starts, x_ends, y_ends, color_values,
              freq_values, width_values, striped_length=1, length_type="units", 
              colormap="viridis", style="middle", color_max=None, 
              color_min=None, color_n=4, color_spread=None, freq_max=None, 
              freq_min=None, freq_n=4, freq_spread=None, color_label="color", 
              shape_label="shape", legend_title="lines", scale_dp=2, 
              interval_type="closest", legend_marker_size="auto", zorder=0.5):
    """
    Add lines/edges to the plot.

    Parameters:
        ax (tuple (matplotlib.figure, matplotlib.axes.SubplotBase, 
            matplotlib.axes.SubplotBase, matplotlib.axes.SubplotBase, 
            Numerical)): 
            This must be the tuple returned by create_plot().
        x_starts (list of float): 
            The x coordinates of the origin points of each line.
        y_starts (list of float): 
            The y coordinates of the origin points of each line.
        x_ends(list of float): 
            The x coordinates of the end points of each line.
        y_ends(list of float): 
            The y coordinates of the end points of each line.
        color_values (list of float): 
            The values to be represented by the color of each
            line.
        freq_values (list of float): 
            the list of values to be represented by the central stripe
            frequency.
        width_values (list of float): 
            the list of values in points for the width of each line.
        striped_length (float, default: 1): 
            if using the style "set_length", the length of the central
            stripe. Units determined by length_type.
        length_type (str, default: "units"): 
            the units to be used for stripe length.
                "units": number of units on the axes.
                "pixels": number of pixels.
        colormap (matplotlib.colors.Colormap, default: "viridis"): 
            the matplotlib colormap to be used.
        style (str, default: "middle"): 
            the length and positioning style of the striped area.
                "middle": striped area centred on line/edge, length is
                    1/3 edge length.
                "ends": one striped area at each end of the line/edge,
                    each 1/4 edge length.
                "source": striped area at line source, 1/2 edge length.
                "destination": striped area at line destination, 1/2 
                    edge length.
                "set_length": striped area at line centre, length 
                    specified by user.
                "frequency": striped area at line centre, 1/3 edge 
                    length. Instead of a set number of stripes, this 
                    uses number of stripes per unit length, matched to
                    the legend.
        color_max (float), optional: 
            The maximum color value in the legend.
        color_min (float), optional: 
            The minimum color value in the legend.
        color_n (int), optional: 
            The number of color values to show in the legend.
        color_spread (float), optional: 
            Range of color values in key. Only used if not specifying
            both max and min.
        freq_max (float), optional: 
            The maximum frequency value in the legend.
        freq_min (int), optional: 
            The minimum frequency value in the legend.
        freq_n (int), optional: 
            The number of frequency values to show in the legend. 
        freq_spread (float), optional:
            Range of frequency values in key. Only used if not 
            specifying both max and min. 
        color_label (str, default: "color"):
            The heading for the color component of the legend.
        shape_label (str, default: "shape"):
            The heading for the shape/frequency component of the legend.
        legend_title (str, default: "lines"):
            The main title for the line legend.
        scale_dp (int, default: 2):
            The number of decimal places to round to for legend values.
        interval_type (str, default: "closest"):
            This defines how the frequency of each line is determined:
                "closest": use the closest scale value.
                "limit": use the highest scale value that the frequency 
                    value is greater than or equal to (based on modulus
                    for negative values).
        legend_marker_size (str, default: "auto"):
            This controls the width of the legend line markers.
                "auto": width is calculated automatically to fit.
                "mean": use the mean width value of the plotted lines.
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
    if not all(isinstance(i, (int, float)) for i in x_starts):
        raise TypeError("x_starts values must be numeric")
    if not all(isinstance(i, (int, float)) for i in x_ends):
        raise TypeError("x_ends values must be numeric")
    if not all(isinstance(i, (int, float)) for i in y_starts):
        raise TypeError("y_starts values must be numeric")
    if not all(isinstance(i, (int, float)) for i in y_ends):
        raise TypeError("y_ends values must be numeric")
    if not all(isinstance(i, (int, float)) for i in color_values):
        raise TypeError("color values must be numeric")
    if not all(isinstance(i, (int, float)) for i in freq_values):
        raise TypeError("freq values must be numeric")
    if not all(isinstance(i, (int, float)) for i in width_values):
        raise TypeError("width values must be numeric")
    for i in [color_min, color_max, color_spread, freq_min, freq_max, 
              freq_spread, color_n, freq_n]:
        if not isinstance(i, (int, float)) and not i==None:
            raise TypeError("Scale minimum, maximum and spread values and "
                            "number of values per scale must be numerical")
    if not isinstance(zorder, (int, float)):
        raise TypeError("zorder must be a numerical value")
    if not isinstance(striped_length, (int, float)):
        raise TypeError("striped_length must be a numerical value")

    if not isinstance(scale_dp, int):
        raise TypeError("scale_dp must be int")

    if not legend_marker_size == "auto" and not legend_marker_size == "mean":
        print("legend_marker_size type invalid, auto will be used")

    # Set default values
    if color_max == None:
        color_max = max(color_values)
    if color_min == None:
        color_min = min(color_values)   
    if freq_max == None:
        freq_max = max(freq_values)
    if freq_min == None:
        freq_min = min(freq_values) 
    if color_spread == None:
        color_spread = color_max - color_min
    if freq_spread == None:
        freq_spread = freq_max - freq_min

    scale_diverges = False

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

    # Get proportions of plot area, which may be required for some styles
    ax_h = ax[1].bbox.height
    ax_w = ax_h / ax[4]

    # Add lines
    artists = []
    for i in range(len(x_starts)):
        artists.append(
            add_line(x_starts[i], 
                 y_starts[i],
                 x_ends[i], 
                 y_ends[i], 
                 get_frequency(freq_values[i], shape_scale, new_freq_scale, 
                               "closest"),
                 get_color(color_values[i], colormap, color_mapping), 
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

    add_line_legend(ax[3], color_scale, colormap, color_mapping, shape_scale, 
                    new_freq_scale, style, scale_x, scale_y, color_label, 
                    shape_label, legend_title, width, scale_dp)


def return_figure(fig, return_type, file_name="vizent_plot_save"):
    """
    Return the created figure by your chosen method 

    Parameters:
        fig (tuple (matplotlib.figure, matplotlib.axes.SubplotBase, 
            matplotlib.axes.SubplotBase, matplotlib.axes.SubplotBase, 
            Numerical)): 
            This must be the tuple returned by create_plot().
        return_type (str): 
            The method for returning the created plot:
                "show": display the figure immediately
                "save": save figure without displaying
                "return": return axes for use with Matplotlib
        file_name (str, default: "vizent_plot_save"): 
            if return_type is "save", the file name for your saved file.
            This can be any format supported by Matplotlib. If no file 
            extension is included, .png is used by default.
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


def vizent_plot(x_values, y_values, color_values, shape_values, size_values, 
                colormap="viridis", scale_x=None, scale_y=None, 
                use_image=False, image_type=None, image_file=None, 
                use_cartopy=False, extent=None, scale_diverges=None, 
                shape="sine", shape_pos="sine", shape_neg="square", 
                color_max=None, color_min=None, color_n=None, 
                color_spread=None, shape_max=None, shape_min=None, 
                shape_n=None, shape_spread=None, color_label="temperature", 
                shape_label="variance", title=None, x_label=None, 
                y_label=None, show_axes=True, save=False, 
                file_name="saved_plot.png", return_axes=False, 
                scale_dp=1, interval_type="closest", show_legend=True):
    """
    Draws a scatter plot of the provided points. 
    Each point is displayed as a Visual Entropy glyph. 

    It will continue to work, but will not include new features for example
    visualisation of node-link diagrams.

    Parameters:
        x_values (list of floats): list of x coordinates
        y_values (list of floats): list of y coordinates
        color_values (list of floats): list of values to be 
                                        represented by color
        shape_values (list of floats): list of values to be 
                                       represented by shape
        size_values (list of floats): list of values for 
                                      diameter of glyphs in 
                                      points.
        colormap (colormap or registered colormap name): 
                             Optional. Default is metoffice 
                             color scheme. Use any matplotlib 
                             colormap.        
        scale_x (float): Optional. Defines x size of plot window
                         in inches.
        scale_y (float): Optional. Defines y size of plot window
                         in inches.       
        use_image (bool): Optional. If True, plot on an image 
                          background.        
        image_type (str): Optional. Use preset image type. 
                          "newcastle" for detailed 3d render
                          of newcastle (use eastings and
                          northings for x and y), "england" 
                          for OSM england map (use grid ref)
        image_file (str): Optional. Use any image file. Please
                          specify absolute path. You must
                          also specify the extent.
        use_cartopy (bool): Optional. Plot the points on
                            Cartopy map. 
        extent (list of floats): Optional. Axis limits or 
                                 extent of coordinates for 
                                 Cartopy. A list of four 
                                 values: [xmin, xmax, ymin, 
                                 ymax]   
        scale_diverges (bool): Optional. If True, diverging 
                               sets of glyphs are used for 
                               positive and negative values.
        shape (str): Optional. Glyph shape design to use.
                     Use shape_pos and shape_neg for 
                     divergent scale. Default is sine.
        shape_pos (str): Optional. When using divergent
                         scale, glyph shape design to use
                         for positive values.
        shape_neg (str): Optional. When using divergent
                         scale, glyph shape design to use
                         for negative values.
        color_max (float): Optional. Maximum value to use
                            for color in key.
        color_min (float): Optional. Minimum value to use
                            for color in key.
        color_n (int): Optional. Number of color values
                        to be shown in key.
        color_spread (float): Optional. Total range of 
                               color values in key. Only
                               use if not specifying max
                               and min.
        shape_max (float): Optional. Maximum value to use
                           for shape in key.
        shape_min (float): Optional. Minimum value to use
                           for shape in key.
        shape_n (int): Optional. Number of shape values
                       to be shown in key. If using a
                       diverging scale, this is the 
                       number of positive values 
                       including zero. Negative values 
                       will reflect positive values.
        shape_spread (float): Optional. Total range of 
                              shape values in key. Only
                              use if not specifying max
                              and min.
        color_label (str): Optional. Text label for color
                            values in key.
        shape_label (str): Optional. Text label for shape
                           values in key.
        title (str): Optional. Title for the plot.
        x_label (str): Optional. Label for x axis. Not shown 
                       for image plots.
        y_label (str): Optional. Label for y axis. Not shown 
                       for image plots.
        show_axes (bool): Optional. If axes are not wanted,
                          e.g. for image plots, set to False.
        save (bool): Optional. If True, save the plot as png.
        file_name (str): Optional. If save, name of saved file.
        return_axes (bool): Optional. If True, the function 
                            will return fig, ax1. These can be
                            used to add more MatPlotLib 
                            elements, such as lines, text 
                            boxes.
        scale_dp (int): Optional. The number of decimal places
                        that scale values should be rounded to. 
        interval_type (str): Optional. This defines how the 
                             shape of each glyph is 
                             classified:
                                "closest": use the closest 
                                           scale value
                                "limit": use the highest scale 
                                         value that the glyph 
                                         value is greater than 
                                         or equal to (based on 
                                         modulus for negative 
                                         values)
        show_legend (bool): Optional. Specify whether or not
                            to display the legend to the 
                            right of the plot.
    """
    fig = create_plot(glyphs=True, lines=False, show_legend=show_legend, 
                     show_axes=show_axes, use_cartopy=use_cartopy, 
                     use_image=use_image, image_type=image_type, 
                     image_file=image_file, extent=extent, 
                     scale_x=scale_x, scale_y=scale_y)

    add_glyphs(fig, x_values, y_values, color_values, shape_values, 
               size_values, colormap=colormap, scale_diverges=scale_diverges, 
               shape=shape, shape_pos=shape_pos, shape_neg=shape_neg, 
               color_max=color_max, color_min=color_min, color_n=color_n, 
               color_spread=color_spread, shape_max=shape_max, 
               shape_min=shape_min, shape_n=shape_n, shape_spread=shape_spread,
               color_label=color_label, shape_label=shape_label, 
               scale_dp=scale_dp, interval_type=interval_type, 
               legend_title=None)

    # Do we want to turn this into a proper wrapper function and add in the 
    # line functionality as well?

    # add_lines(ax, x_starts, y_starts, x_ends, y_ends, color_values,
    #           freq_values, width_values, striped_length=1, 
    #           length_type="units", colormap="viridis", style="middle", 
    #           color_max=None, color_min=None, color_n=4, 
    #           color_spread=None, freq_max=None, freq_min=None, 
    #           freq_n=4, freq_spread=None, color_label="color", 
    #           shape_label="shape", legend_title="lines", scale_dp=2, 
    #           interval_type="closest", legend_marker_size="auto")
    
    if title is not None:
        delim_title = title.split("\n")
        max_length = max(len(line) for line in delim_title)
        font_size = min(18, 1.5*(scale_x/(max_length*0.014)))
        plt.suptitle(title, fontsize=font_size, fontweight="bold")
    
    
    fig[1].set_xlabel(x_label)
    fig[1].set_ylabel(y_label)
    
    if return_axes:
        return_figure(fig, 'return', file_name=file_name)
    elif save:
        return_figure(fig, 'save', file_name=file_name)
    else:
        return_figure(fig, None, file_name=file_name)
        
